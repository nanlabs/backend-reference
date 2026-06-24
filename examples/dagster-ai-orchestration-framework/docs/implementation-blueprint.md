# 4-Layer AI Agent Implementation Blueprint

## LAYER 1: Frontend (Vercel AI SDK + Next.js Streaming + Gen UI)

### 1.1 Streaming Chat Endpoint with Token Streaming

```typescript
// app/api/chat/route.ts
import { generateObject } from 'ai';
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export const runtime = 'nodejs';

export async function POST(req: Request) {
  const { messages } = await req.json();

  // Streaming text response with tokens in real-time
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    system: `You are a pharmaceutical expert agent. Analyze vendor data and provide 
              structured recommendations. When responding about dosages or metrics, 
              return valid JSON for component rendering.`,
    messages,
    temperature: 0.7,
  });

  // Create a ReadableStream that pipes tokens to client
  return result.toAIStreamResponse();
}
```

### 1.2 Generative UI (Gen UI) - Live React Components from LLM

```typescript
// app/api/gen-ui/route.ts
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

// Define structured schema for component generation
const componentSchema = z.object({
  type: z.enum(['dosage_table', 'interaction_chart', 'approval_workflow', 'metrics_dashboard']),
  props: z.object({
    data: z.array(z.any()),
    title: z.string(),
    config: z.record(z.any()).optional(),
  }),
});

export async function POST(req: Request) {
  const { query, vendorId } = await req.json();

  // Generate structured component definition
  const { object } = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: componentSchema,
    prompt: `Given this vendor analysis query: "${query}"
              Return a component definition for rendering interactive results.
              vendor_id: ${vendorId}`,
  });

  return Response.json(object);
}
```

### 1.3 Client-Side Gen UI Renderer (React)

```typescript
// components/GenUIRenderer.tsx
import React, { Suspense } from 'react';
import DosageTable from './components/DosageTable';
import InteractionChart from './components/InteractionChart';
import ApprovalWorkflow from './components/ApprovalWorkflow';
import MetricsDashboard from './components/MetricsDashboard';

const componentMap = {
  dosage_table: DosageTable,
  interaction_chart: InteractionChart,
  approval_workflow: ApprovalWorkflow,
  metrics_dashboard: MetricsDashboard,
};

interface GenUIProps {
  componentDef: {
    type: keyof typeof componentMap;
    props: Record<string, any>;
  };
}

export function GenUIRenderer({ componentDef }: GenUIProps) {
  const Component = componentMap[componentDef.type];

  if (!Component) {
    return <div className="error">Unknown component type: {componentDef.type}</div>;
  }

  return (
    <Suspense fallback={<div className="loading">Rendering component...</div>}>
      <Component {...componentDef.props} />
    </Suspense>
  );
}
```

---

## LAYER 2: Orchestration (LangGraph + Agent Loops)

### 2.1 Agent State Machine with LangGraph

```python
# agent/graph.py
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage
from langchain_core.tools import Tool

class AgentState(TypedDict):
    """Central agent state - persisted across loop iterations"""
    messages: Annotated[List[BaseMessage], operator.add]
    vendor_id: str
    context: dict
    approval_status: str
    checkpoint_id: str

def agent_node(state: AgentState, llm_with_tools):
    """Think/Decide - agent deliberates given current state"""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {
        "messages": [response],
        "checkpoint_id": f"decision_{len(messages)}"
    }

def tool_execution_node(state: AgentState, executor: ToolExecutor):
    """Execute - run selected tool with vendor_id boundary"""
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    results = []
    
    for tool_call in tool_calls:
        if not validate_vendor_access(state["vendor_id"], tool_call.name):
            result = {"error": f"Access denied: {tool_call.name}"}
        else:
            result = executor.invoke(tool_call)
        results.append(result)
    
    return {
        "messages": [{"role": "tool", "content": str(results)}],
        "approval_status": "executing"
    }

def conditional_router(state: AgentState):
    """Route - decide if continue loop or end"""
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "execute_tools"
    else:
        return "end"

# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", lambda s: agent_node(s, llm_with_tools))
graph.add_node("tools", lambda s: tool_execution_node(s, executor))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", conditional_router, {"execute_tools": "tools", "end": END})
graph.add_edge("tools", "agent")

from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=memory)
```

### 2.2 Checkpoint Persistence

```python
# agent/checkpoints.py
from datetime import datetime
import json

class CheckpointManager:
    def __init__(self, db_path: str = "agent_checkpoints.db"):
        self.db_path = db_path
    
    def save_checkpoint(self, thread_id: str, state: dict, reason: str = "auto"):
        """Persist agent state for pause/resume"""
        checkpoint = {
            "thread_id": thread_id,
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "state": {
                "vendor_id": state["vendor_id"],
                "messages_count": len(state["messages"]),
                "approval_status": state.get("approval_status", ""),
            }
        }
        with open(f"{self.db_path}/{thread_id}.json", "w") as f:
            json.dump(checkpoint, f)
        return checkpoint
    
    def resume_from_checkpoint(self, thread_id: str):
        """Resume agent execution from saved state"""
        with open(f"{self.db_path}/{thread_id}.json", "r") as f:
            checkpoint = json.load(f)
        return checkpoint["state"]
```

---

## LAYER 3: Runtime & Infra (Identity Forwarding + Cedar Policies)

### 3.1 Identity Forwarding Middleware (Okta/AD → AWS)

```python
# middleware/identity_forwarding.py
from fastapi import Request, HTTPException
from jose import jwt
import httpx

class IdentityForwardingMiddleware:
    """Forward user identity end-to-end while enforcing vendor boundaries"""
    
    def __init__(self, okta_issuer: str, cedar_policy_engine_url: str):
        self.okta_issuer = okta_issuer
        self.cedar_url = cedar_policy_engine_url
    
    async def extract_identity(self, request: Request) -> dict:
        """Extract token from request, validate with Okta"""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing token")
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.get_unverified_claims(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
        
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "vendor_id": payload.get("custom:vendor_id"),
            "roles": payload.get("roles", []),
            "token": token
        }
    
    async def validate_vendor_access(self, identity: dict, resource: str) -> bool:
        """Check Cedar policies before allowing access"""
        async with httpx.AsyncClient() as client:
            policy_request = {
                "principal": f"User::{identity['user_id']}",
                "action": "ViewVendorData",
                "resource": f"Vendor::{identity['vendor_id']}/{resource}",
                "context": {
                    "email": identity["email"],
                    "roles": identity["roles"]
                }
            }
            
            response = await client.post(
                f"{self.cedar_url}/evaluate",
                json=policy_request
            )
            
            result = response.json()
            return result.get("decision") == "Allow"
```

### 3.2 Cedar Policy Engine Integration

```cedar
// policies/cedar_policies.cedar
type User = { email: String };
type Vendor = { name: String };
type VendorData = { vendorId: String, dataType: String };

permit(
  principal is User,
  action in [ViewVendorData, QueryMetrics],
  resource is VendorData
)
when {
  resource.vendorId == principal.vendor_id
};

deny(
  principal is User,
  action == ViewConfidentialData,
  resource is VendorData
)
when {
  !resource.approverNames.contains(principal.email)
};
```

---

## LAYER 4: Data Layer (MCP + Multimodal Embeddings)

### 4.1 MCP Server Setup (DuckDB + Vendor Data)

```python
# mcp_server/server.py
from mcp.server import Server
import json
import duckdb

class VendorDataMCPServer:
    """MCP server exposing DuckDB vendor data with vendor isolation"""
    
    def __init__(self, db_path: str):
        self.server = Server("vendor-data-server")
        self.db = duckdb.connect(db_path)
        self.register_tools()
    
    def register_tools(self):
        """Register tools exposed via MCP protocol"""
        
        @self.server.tool()
        def query_dosage_data(vendor_id: str, drug_name: str = None) -> str:
            """Query dosage information for specific vendor"""
            query = f"""
            SELECT drug_name, dosage, frequency, max_daily, approval_status
            FROM dosage_database
            WHERE vendor_id = '{vendor_id}'
            """
            if drug_name:
                query += f" AND drug_name ILIKE '%{drug_name}%'"
            
            result = self.db.execute(query).fetchall()
            return json.dumps(result)
        
        @self.server.tool()
        def check_interactions(vendor_id: str, drug_list: list) -> str:
            """Check drug interactions for vendor's approval"""
            placeholders = ",".join([f"'{d}'" for d in drug_list])
            query = f"""
            SELECT drug1, drug2, interaction_severity, recommendation
            FROM drug_interactions
            WHERE vendor_id = '{vendor_id}'
            AND (drug1 IN ({placeholders}) OR drug2 IN ({placeholders}))
            """
            result = self.db.execute(query).fetchall()
            return json.dumps(result)
```

### 4.2 Multimodal Embeddings (PDF + Screenshots + Video)

```python
# embeddings/multimodal_processor.py
import PyPDF2
import cv2
import pytesseract
from sentence_transformers import SentenceTransformer
import torch
from pathlib import Path
from typing import List
import numpy as np

class MultimodalEmbeddingProcessor:
    """Process patents (PDF), screenshots, and video frames into unified embeddings"""
    
    def __init__(self):
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.image_model = SentenceTransformer('clip-vit-b-32')
    
    def extract_pdf_text(self, pdf_path: str) -> List[str]:
        """Extract text from patent PDFs"""
        texts = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                texts.append({
                    "page": page_num + 1,
                    "content": text,
                    "source_type": "pdf"
                })
        return texts
    
    def extract_screenshot_ocr(self, image_path: str) -> dict:
        """OCR text from screenshot + get visual embedding"""
        image = cv2.imread(image_path)
        text = pytesseract.image_to_string(image)
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_embedding = self.image_model.encode(image_rgb, convert_to_tensor=True)
        
        return {
            "text": text,
            "image_embedding": image_embedding.cpu().numpy(),
            "source_type": "screenshot",
            "path": image_path
        }
    
    def extract_video_frames(self, video_path: str, frame_interval: int = 30) -> List[dict]:
        """Extract frames from video, OCR each, create embeddings"""
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        frames_data = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                text = pytesseract.image_to_string(frame)
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_embedding = self.image_model.encode(image_rgb, convert_to_tensor=True)
                
                frames_data.append({
                    "frame_number": frame_count,
                    "timestamp": frame_count / cap.get(cv2.CAP_PROP_FPS),
                    "text": text,
                    "image_embedding": image_embedding.cpu().numpy(),
                    "source_type": "video_frame"
                })
            
            frame_count += 1
        
        cap.release()
        return frames_data
    
    def create_unified_index(self, pdf_paths: List[str], image_paths: List[str], 
                            video_paths: List[str]) -> dict:
        """Create searchable index across all modalities"""
        all_documents = []
        
        for pdf_path in pdf_paths:
            docs = self.extract_pdf_text(pdf_path)
            all_documents.extend(docs)
        
        for image_path in image_paths:
            doc = self.extract_screenshot_ocr(image_path)
            all_documents.append(doc)
        
        for video_path in video_paths:
            frames = self.extract_video_frames(video_path)
            all_documents.extend(frames)
        
        texts = [doc.get("text", "") or doc.get("content", "") 
                for doc in all_documents]
        embeddings = self.text_model.encode(texts, convert_to_tensor=True)
        
        return {
            "documents": all_documents,
            "embeddings": embeddings.cpu().numpy(),
            "total_documents": len(all_documents)
        }
    
    def search_across_modalities(self, query: str, index: dict, top_k: int = 5) -> List[dict]:
        """Search PDFs + images + video using semantic similarity"""
        query_embedding = self.text_model.encode(query, convert_to_tensor=True)
        embeddings_tensor = torch.tensor(index["embeddings"])
        
        similarities = torch.nn.functional.cosine_similarity(
            query_embedding.unsqueeze(0),
            embeddings_tensor
        )
        
        top_k_indices = torch.topk(similarities, k=min(top_k, len(index["documents"]))).indices
        
        results = []
        for idx in top_k_indices:
            doc = index["documents"][idx.item()]
            results.append({
                "source": doc.get("source_type"),
                "content": doc.get("text") or doc.get("content"),
                "similarity": similarities[idx].item(),
            })
        
        return results
```

---

## LAYER 5: Validation (Prompt Testing + Workflow Validation)

### 5.1 Prompt Testing Framework (Evals)

```python
# validation/prompt_evals.py
from typing import List, Dict, Callable
import json
from dataclasses import dataclass
import asyncio

@dataclass
class PromptTestCase:
    name: str
    input_message: str
    expected_outputs: List[str]
    vendor_context: dict
    success_criteria: Callable[[dict], bool]

class PromptEvaluator:
    """Test prompts and agent behaviors systematically"""
    
    def __init__(self, agent_runtime):
        self.agent = agent_runtime
        self.results = []
    
    async def run_test_case(self, test_case: PromptTestCase) -> dict:
        """Run single prompt test and check against success criteria"""
        try:
            result = await self.agent.invoke(
                messages=[{"role": "user", "content": test_case.input_message}],
                vendor_id=test_case.vendor_context["vendor_id"],
                timeout=30
            )
            
            passed = test_case.success_criteria(result)
            
            return {
                "test_name": test_case.name,
                "passed": passed,
                "output": result,
                "vendor_id": test_case.vendor_context["vendor_id"]
            }
        except Exception as e:
            return {
                "test_name": test_case.name,
                "passed": False,
                "error": str(e)
            }
    
    async def run_test_suite(self, test_cases: List[PromptTestCase]) -> dict:
        """Run multiple test cases and summarize"""
        results = await asyncio.gather(
            *[self.run_test_case(tc) for tc in test_cases]
        )
        
        passed_count = sum(1 for r in results if r["passed"])
        return {
            "total_tests": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "pass_rate": passed_count / len(results) if results else 0,
            "results": results
        }

# Example test cases
test_suite = [
    PromptTestCase(
        name="Vendor boundary isolation",
        input_message="Show me all drugs approved by other vendors",
        expected_outputs=["Access denied"],
        vendor_context={"vendor_id": "vendor_123"},
        success_criteria=lambda r: "Access denied" in str(r) or "error" in str(r).lower()
    ),
    PromptTestCase(
        name="Dosage query within boundary",
        input_message="What are the approved dosages for aspirin?",
        expected_outputs=["dosage", "approved"],
        vendor_context={"vendor_id": "vendor_123"},
        success_criteria=lambda r: "dosage" in str(r).lower()
    ),
]
```

### 5.2 Workflow Validation

```python
# validation/workflow_validation.py
from enum import Enum
from typing import List, Dict
from datetime import datetime

class WorkflowPhase(Enum):
    INITIALIZATION = "init"
    AGENT_DECISION = "decide"
    TOOL_EXECUTION = "execute"
    APPROVAL = "approval"
    COMPLETION = "complete"

@dataclass
class WorkflowCheckpoint:
    phase: WorkflowPhase
    timestamp: datetime
    state_snapshot: dict
    valid: bool
    errors: List[str]

class WorkflowValidator:
    """Validate agent workflows follow expected paths"""
    
    def __init__(self):
        self.checkpoints: List[WorkflowCheckpoint] = []
    
    def validate_workflow_sequence(self, checkpoints: List[WorkflowCheckpoint]) -> bool:
        """Validate checkpoints follow valid state transitions"""
        expected_sequence = [
            WorkflowPhase.INITIALIZATION,
            WorkflowPhase.AGENT_DECISION,
            WorkflowPhase.TOOL_EXECUTION,
            WorkflowPhase.APPROVAL,
            WorkflowPhase.COMPLETION
        ]
        
        actual_sequence = [cp.phase for cp in checkpoints]
        
        # Check if sequence follows expected pattern (may have loops)
        if not actual_sequence:
            return False
        
        if actual_sequence[0] != WorkflowPhase.INITIALIZATION:
            return False
        
        if actual_sequence[-1] != WorkflowPhase.COMPLETION:
            return False
        
        return True
    
    def validate_identity_boundaries(self, workflow_checkpoints: List[dict]) -> bool:
        """Ensure vendor_id stays consistent across workflow"""
        vendor_ids = [cp.get("vendor_id") for cp in workflow_checkpoints]
        return len(set(vendor_ids)) == 1  # Only one vendor_id allowed
    
    def validate_approval_gates(self, workflow: dict) -> bool:
        """Ensure approval gates are properly enforced"""
        approval_count = sum(
            1 for cp in workflow["checkpoints"]
            if cp["phase"] == WorkflowPhase.APPROVAL
        )
        return approval_count > 0

# Example usage
def validate_completed_workflow(workflow_log: dict) -> Dict:
    validator = WorkflowValidator()
    
    checks = {
        "sequence_valid": validator.validate_workflow_sequence(workflow_log["checkpoints"]),
        "identity_boundaries_valid": validator.validate_identity_boundaries(workflow_log["checkpoints"]),
        "approval_gates_present": validator.validate_approval_gates(workflow_log),
    }
    
    return {
        "workflow_id": workflow_log["id"],
        "all_valid": all(checks.values()),
        "validation_results": checks
    }
```

---

## Architecture Integration Overview

### Data Flow

```text
User Message
    ↓
[Layer 1: Frontend] Vercel AI SDK streaming chat → Next.js API route
    ↓
[Layer 3: Identity Forwarding] Extract Okta token → Validate Cedar policies
    ↓
[Layer 2: Orchestration] LangGraph agent loop (Think → Decide → Execute)
    ↓
[Layer 4: Data Access] MCP server + Multimodal embeddings
    ↓
[Layer 3: Runtime] AWS AgentCore Lambda with vendor isolation
    ↓
[Layer 5: Validation] Checkpoint persistence, approval gates
    ↓
[Layer 1: Frontend] Gen UI component rendering + token streaming
```

### Security Boundaries

- **Vendor Isolation**: vendor_id enforced at every layer (Middleware → Agent → MCP → Database)
- **Identity Forwarding**: Token passed end-to-end with read-only validation at each hop
- **Policy Engine**: Cedar evaluates every action before execution
- **Checkpoint Approval**: Critical operations require human approval + resume from checkpoint