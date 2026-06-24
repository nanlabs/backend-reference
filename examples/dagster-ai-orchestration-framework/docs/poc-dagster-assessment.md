# POC Dagster: 4-Layer AI Agent Architecture Assessment

**Date**: June 24, 2026  
**Repository**: `poc-dagster`  
**Current Status**: ⚠️ **Incomplete** - Data orchestration POC, NOT an AI Agent framework  
**Language**: English  
**Perspective**: Opinionated gap analysis for production AI agent deployment

---

## Executive Summary

**What This POC Is**: A professional Dagster data pipeline with advanced orchestration patterns (partitioning, sensors, asset checks, environment switching).

**What This POC Is NOT**: An AI agent framework. It lacks every layer of the 4-Layer AI Agent Stack you specified.

**Completeness Score**: **18% of target architecture** ❌

---

## Architecture Gap Analysis

### Layer 1: Frontend (Vercel AI SDK + Next.js) — **0% IMPLEMENTED**

**Target**: 
- ✅ Token streaming for real-time chat responses
- ✅ Generative UI (Gen UI) → React components with interactive charts, dosage tables
- ✅ Chat interface with message history management

**Current State**: 
- ❌ **ZERO implementation**
- Only a Nextra documentation site (static Next.js + docs theme, no interactivity)
- No Vercel AI SDK integration
- No streaming infrastructure
- No React component generation
- No chat UI

**Gap**: **100% missing**

**What Needs to Be Built**:
```typescript
// Example: Token streaming with Vercel AI SDK (NOT in poc-dagster)
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();
  
  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
    // This is what's missing: real-time token streaming to client
  });
  
  return result.toAIStream(); // Returns SSE stream
}

// Gen UI Example: Dynamic React component rendering (NOT in poc-dagster)
function DosageTable({ data }) {
  return (
    <div className="interactive-chart">
      {/* Live dosage calculations rendered as React component */}
      <ResponsiveContainer data={data} />
    </div>
  );
}
```

**Missing Dependencies**:
- `ai` package (Vercel AI SDK)
- `react-markdown`
- `recharts` or `plotly.js` (for Gen UI charts)
- Server-sent events (SSE) infrastructure
- WebSocket or polling for real-time updates

---

### Layer 2: Orchestration (LangGraph) — **0% IMPLEMENTED**

**Target**:
- ✅ Agent logic with centralized State, Nodes (functions), conditional routing
- ✅ Decision-making loops (Agent → Tool → State Update → Agent)
- ✅ Checkpoints for pauseable workflows (e.g., human approval gates)
- ✅ Memory management and context persistence

**Current State**:
- ❌ **NO LangGraph integration**
- ❌ **NO Agent state machine**
- ❌ **NO tool execution loop**
- ✅ Dagster has **scheduling + sensors**, but these are pipeline triggers, NOT agent loops

**Why Dagster ≠ LangGraph**:
| Aspect | Dagster | LangGraph | Agent Need? |
|--------|---------|-----------|------------|
| **Purpose** | Data pipeline orchestration | Agentic loop orchestration | Agent |
| **Trigger** | Schedule/sensor/manual | User message/tool result | Agent |
| **State** | Asset lineage + metadata | Conversation + context dict | Agent |
| **Loop** | Linear DAG (assets → assets) | Cyclical (Agent → Tool → State → Agent) | Agent |
| **Loops Per Run** | 1 | N (multiple tool calls) | Agent |
| **Tool Calls** | Not designed for this | Native tool_call nodes | Agent |

**Gap**: **100% missing**

**What Needs to Be Built**:
```python
# Example: LangGraph Agent State (NOT in poc-dagster)
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list  # Chat history
    context: dict   # Vendor data + permissions
    tools_used: list
    human_approval_pending: bool

def agent_node(state: AgentState) -> AgentState:
    """LLM decides: take action or ask user?"""
    # This cyclical thinking is MISSING in poc-dagster
    # Dagster runs "asset A → asset B → asset C" once
    # Agents need "think → act → think → act" loops per message
    pass

def human_approval_gate(state: AgentState) -> str:
    """Checkpoint: pause if sensitive action."""
    if state.tool_name == "execute_payment":
        return "approval_pending"
    return "continue"

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_execution_node)
graph.add_conditional_edges("agent", human_approval_gate)
graph.add_edge(START, "agent")
```

**Missing Dependencies**:
- `langgraph`
- `langchain` (for tool definitions)
- `anthropic` or `openai` LLM client (already exists? not found)
- Checkpoint persistence (Redis, PostgreSQL, or LangGraph Cloud)
- Human-in-the-loop framework

---

### Layer 3: Runtime & Infra (AWS AgentCore + Identity Forwarding) — **0% IMPLEMENTED**

**Target**:
- ✅ Identity Forwarding: Securely pass user token (Okta/AD) end-to-end
- ✅ Serverless execution (AWS Lambda → agent logic)
- ✅ Governance with Cedar: External security policies for agent actions
- ✅ Data access scoping: Agent only reads/writes permitted data per vendor/seller

**Current State**:
- ❌ **NO Identity Forwarding**
- ❌ **NO Okta/Active Directory integration**
- ❌ **NO Cedar policies**
- ❌ **NO serverless runtime**
- ✅ Dagster has environment switching (local/prod) but NO identity context
- Local dev: mock tokens, no security model

**Gap**: **100% missing**

**What Needs to Be Built**:
```python
# Example: Identity Forwarding (NOT in poc-dagster)
from aws_lambda_powertools import Logger
from functools import wraps
import jwt

logger = Logger()

def forward_user_identity(handler):
    """Decorator: Extract Okta token, validate, pass through request context."""
    @wraps(handler)
    async def wrapper(event, context):
        # 1. Extract user token from Authorization header
        auth_header = event.get("headers", {}).get("Authorization", "")
        token = auth_header.replace("Bearer ", "")
        
        # 2. Validate token with Okta JWKS
        try:
            decoded = jwt.decode(
                token,
                key=fetch_okta_jwks(),
                algorithms=["RS256"]
            )
            user_id = decoded["sub"]
            vendor_id = decoded.get("vendor_id")  # Custom claim
        except jwt.InvalidTokenError:
            return {"statusCode": 401, "body": "Unauthorized"}
        
        # 3. Inject identity into Lambda context (not standard event)
        context.user_id = user_id
        context.vendor_id = vendor_id
        
        # 4. Pass through to agent → tool execution
        # Agent now knows: "This is vendor_123, only access their data"
        return await handler(event, context)
    
    return wrapper

@forward_user_identity
async def agent_handler(event, context):
    # context.user_id, context.vendor_id available
    # All downstream queries scoped to this vendor
    pass

# Example: Cedar Policy (NOT in poc-dagster)
cedar_policy = """
permit(
    principal == User::"user@vendor123.okta.com",
    action == Action::"execute_order_analysis",
    resource == OrderData::"vendor123_orders"
)
when {
    context.requested_month == resource.data_month &&
    principal.approval_level >= 2
};

deny(
    principal,
    action == Action::"modify_pricing",
    resource == PricingTable::*
)
when {
    principal.department != "Admin"
};
"""
```

**Missing Infrastructure**:
- Okta/AD OIDC integration
- AWS Lambda for serverless execution
- Cedar CLI + policy engine integration
- API Gateway + request interceptors
- Secret management (AWS Secrets Manager)
- Identity context propagation to downstream services

---

### Layer 4: Data Layer (MCP + Multimodal Embeddings) — **40% IMPLEMENTED**

**Target**:
- ✅ Model Context Protocol (MCP): Unified agent ↔ database connector
- ✅ Multimodal embeddings: Process PDFs (patents), screenshots, video fragments
- ✅ Semantic search: Query source documents by meaning, not SQL
- ✅ RAG pipeline: Retrieve relevant context for agent reasoning

**Current State**:
- ❌ **NO MCP integration** (modern standard for agent-db connections)
- ❌ **NO multimodal embeddings**
- ❌ **NO RAG pipeline**
- ✅ **Partial**: Dagster has DuckDB resources + asset-based data processing
- ✅ **Partial**: Basic ETL patterns (assets, transformations, checks)

**Gap**: **65% missing**

**What's Working**:
```python
# This EXISTS in poc-dagster (assets_etl.py)
@dg.asset
def customers(duckdb: DuckDBResource) -> None:
    duckdb.execute("""
        CREATE TABLE customers AS
        SELECT * FROM raw_customers
    """)

# But this does NOT exist:
# 1. MCP server exposing this table to LLM
# 2. Vector embeddings of customer notes
# 3. Semantic search: "Find customers with payment issues"
```

**What Needs to Be Built**:
```python
# Example: MCP Server for agent ↔ database (NOT in poc-dagster)
from mcp.server.fastmcp import FastMCP

app = FastMCP("vendor_data_server")

@app.resource_template("/database/tables/{table_name}")
def get_table_schema(table_name: str) -> dict:
    """MCP resource: Expose table schema to agent."""
    return {
        "type": "table",
        "name": table_name,
        "schema": fetch_schema_from_duckdb(table_name),
        "sample_rows": 5
    }

@app.tool()
def query_table(table_name: str, filters: dict) -> list:
    """MCP tool: Agent can query tables."""
    sql = build_safe_query(table_name, filters)
    return duckdb.execute(sql).fetchall()

# Example: Multimodal Embeddings (NOT in poc-dagster)
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import base64

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_patent_pdf(pdf_path: str):
    """Process patent PDF → chunks → embeddings → vector DB."""
    # 1. Extract text from PDF
    reader = PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages)
    
    # 2. Chunk into semantic units
    chunks = [text[i:i+512] for i in range(0, len(text), 256)]
    
    # 3. Generate embeddings
    embeddings = embedding_model.encode(chunks)
    
    # 4. Store in vector DB (e.g., Qdrant, Pinecone)
    vector_db.upsert(
        ids=[f"patent_chunk_{i}" for i in range(len(chunks))],
        vectors=embeddings,
        metadata={"source": pdf_path, "type": "patent"}
    )

def ingest_screenshot(image_b64: str, vendor_id: str):
    """Process screenshot → OCR → embeddings → RAG index."""
    # Extract text via vision model
    ocr_text = vision_model.extract_text(base64.b64decode(image_b64))
    
    # Generate multimodal embedding (understands images + text)
    embedding = multimodal_model.encode(image_b64, ocr_text)
    
    # Store for RAG retrieval
    rag_index.add(embedding, metadata={
        "vendor_id": vendor_id,
        "type": "screenshot",
        "timestamp": datetime.now()
    })
```

**Missing Dependencies**:
- `mcp` package (Model Context Protocol)
- `sentence-transformers` (embeddings)
- `langchain` or `llama-index` (RAG frameworks)
- Vector database client (`qdrant-client`, `pinecone`, etc.)
- Vision model for multimodal processing (Claude Vision, GPT-4V)
- PDF extraction (`PyPDF2`, `pdfplumber`)
- Video processing library (if supporting video fragments)

---

### Extra: Validation & Testing — **45% IMPLEMENTED**

**Target**:
- ✅ Prompt testing framework (evaluate LLM behavior against expectations)
- ✅ Workflow testing (simulate agent decision loops)
- ✅ Integration testing (end-to-end: message → agent → tool → response)
- ✅ Data quality checks (validation of transformations)
- ✅ Performance benchmarks (latency, token usage)

**Current State**:
- ✅ **STRONG**: Unit tests for Dagster assets (428 lines, pytest)
- ✅ **STRONG**: Data quality checks (asset checks, uniqueness, PK validation)
- ✅ **STRONG**: Partitioned dataset validation
- ❌ **MISSING**: LLM/prompt testing framework
- ❌ **MISSING**: Agent workflow simulation
- ❌ **MISSING**: Chat message handling tests
- ❌ **MISSING**: Token counting/cost estimation

**Gap**: **55% missing** (data layer tested, agent layer untested)

**What's Working**:
```python
# This EXISTS in poc-dagster (test_pipeline.py)
def test_clean_tasks_asset():
    """Verify ClickUp task cleaning logic."""
    # Mock resources, materialize asset, validate schema
    context = build_asset_context(resources={"clickup_api": mock_api})
    result = clean_tasks(context)
    assert result.shape == (expected_rows, expected_cols)

# Asset checks (in assets_heavy_analytics.py)
@dg.asset_check(asset=enriched_customer_order_history)
def check_enrichment_fan_out(context, enriched_customer_order_history):
    """Detect JOIN row multiplication issues."""
    orders_per_customer = (
        enriched_customer_order_history.groupby("customer_id").size()
    )
    assert orders_per_customer.max() <= 50  # Business rule
```

**What Needs to Be Built**:
```python
# Example: Prompt Testing Framework (NOT in poc-dagster)
from promptfoo import Eval
from datetime import datetime

prompt_tests = [
    {
        "description": "Agent respects vendor data boundary",
        "prompt": "Show me all vendor orders",
        "context": {"vendor_id": "vendor_123"},
        "expected": {
            "contains": ["vendor_123"],
            "not_contains": ["vendor_124", "vendor_456"],  # Other vendors
            "structured": {"vendor_count": 1}
        }
    },
    {
        "description": "Agent asks for clarification on ambiguous request",
        "prompt": "Update pricing",
        "context": {"user_role": "analyst"},
        "expected": {
            "contains": ["clarify", "confirm", "permission"],
            "action": "human_approval_required"
        }
    }
]

# Run evaluations
evaluator = Eval(
    prompts=["gpt-4-turbo", "claude-3-opus"],
    test_cases=prompt_tests,
    metrics=["similarity", "safety", "vendor_boundary_compliance"]
)
results = evaluator.run()

# Example: Agent Workflow Testing (NOT in poc-dagster)
from langgraph.checkpoint.memory import MemorySaver

def test_agent_approval_gate():
    """Verify agent pauses for sensitive actions."""
    checkpointer = MemorySaver()
    
    # Simulate message: "Execute $10M order"
    initial_input = {
        "messages": [{"role": "user", "content": "Execute $10M order"}],
        "vendor_id": "vendor_123"
    }
    
    # Step 1: Agent decides action
    output1 = graph.invoke(initial_input, {"configurable": {"thread_id": "test1"}})
    assert output1["state"] == "awaiting_approval"
    
    # Step 2: Human approves
    output1["messages"].append({"role": "user", "content": "Approved"})
    
    # Step 3: Agent continues
    output2 = graph.invoke(output1, {"configurable": {"thread_id": "test1"}})
    assert output2["state"] == "order_executed"

# Example: Token counting for cost estimation (NOT in poc-dagster)
from anthropic import Anthropic

def test_token_efficiency():
    """Ensure agent prompts stay under token budget."""
    client = Anthropic()
    
    large_context = load_vendor_data_1mb()  # 1MB of context
    
    response = client.messages.count_tokens(
        model="claude-3-5-sonnet",
        messages=[{"role": "user", "content": large_context}]
    )
    
    assert response.input_tokens < 50000  # Stay in reasonable range
    estimated_cost = (response.input_tokens / 1_000_000) * 3.0  # $3 per 1M input tokens
    print(f"Estimated cost: ${estimated_cost:.4f}")
```

**Missing Testing Tools**:
- `promptfoo` (prompt evaluation framework)
- `langgraph` checkpoint testing utilities
- `anthropic` or `openai` token counting APIs
- `pytest-asyncio` (for async agent testing)
- Cost tracking/estimation libraries

---

## Completeness Scorecard

| Layer | Aspect | Status | % Complete | Critical Gap |
|-------|--------|--------|------------|--------------|
| **Layer 1: Frontend** | Streaming | ❌ | 0% | ⚠️ CRITICAL |
| | Gen UI | ❌ | 0% | ⚠️ CRITICAL |
| | Chat UI | ❌ | 0% | ⚠️ CRITICAL |
| **Layer 2: Orchestration** | Agent loop | ❌ | 0% | ⚠️ CRITICAL |
| | State management | ❌ | 0% | ⚠️ CRITICAL |
| | Checkpoints/gates | ❌ | 0% | ⚠️ CRITICAL |
| | Tool execution | ❌ | 0% | ⚠️ CRITICAL |
| **Layer 3: Runtime/Infra** | Identity forwarding | ❌ | 0% | ⚠️ CRITICAL |
| | Cedar policies | ❌ | 0% | ⚠️ CRITICAL |
| | Serverless infra | ❌ | 0% | ⚠️ CRITICAL |
| **Layer 4: Data Layer** | MCP integration | ❌ | 0% | ⚠️ CRITICAL |
| | Multimodal embeddings | ❌ | 0% | ⚠️ CRITICAL |
| | RAG pipeline | ❌ | 0% | ⚠️ CRITICAL |
| | ETL + transforms | ✅ | 75% | ⚠️ Missing advanced patterns |
| | Data quality checks | ✅ | 85% | Minor |
| **Extra: Validation** | Prompt testing | ❌ | 0% | ⚠️ CRITICAL |
| | Agent workflow testing | ❌ | 0% | ⚠️ CRITICAL |
| | Unit tests (data) | ✅ | 90% | None |
| | Asset checks | ✅ | 85% | None |

**Overall**: **18% Complete** ⚠️

---

## Opinionated Recommendations

### ✅ What the POC Gets Right

1. **Dagster Foundation**: Excellent data orchestration layer. The auto-discovery pattern, environment switching, and resource injection are production-ready.

2. **Testing Discipline**: Strong pytest coverage for data assets. This is rare and valuable.

3. **Documentation**: Exceptional educational material (Nextra hub, learning progression). This is reusable for agent documentation.

4. **In-Database Processing**: Correct philosophy — push compute down to DuckDB, not Python loops.

5. **Partitioned Incremental Processing**: Professional pattern for handling growing datasets efficiently.

### ❌ What's Fundamentally Missing

**This is NOT an AI Agent framework.** It's a data pipeline POC. To build the 4-layer AI agent stack you described, you need:

1. **Immediate Priority (Layer 2)**: Build LangGraph agent with state machine, tool definitions, and checkpoints. This is the *heart* of the system.

2. **Then (Layer 1)**: Add Next.js + Vercel AI SDK streaming frontend with Gen UI.

3. **Then (Layer 3)**: Implement identity forwarding + Cedar policies.

4. **Then (Layer 4)**: Integrate MCP for agent ↔ database communication, add RAG.

### 🎯 Refactoring Path

**Option A: Keep Dagster for data layer ONLY**
```
Frontend (Vercel AI) 
    ↓ (HTTP/MCP)
LangGraph Agent (orchestration + tools)
    ↓ (MCP server)
Dagster Pipelines (data transformations)
    ↓
DuckDB / Data Lake (persistence)
```

**Option B: Replace with LangGraph for everything** (risky, might lose Dagster's strengths)
```
Frontend (Vercel AI)
    ↓
LangGraph + LangChain tools (agent loop)
    ↓
Direct SQL queries (no Dagster orchestration)
```

**Recommendation**: **Option A** — Keep Dagster for scheduled/reactive data work, add LangGraph for agent logic.

---

## Implementation Roadmap (If Converting to AI Agent System)

### Phase 1: Foundation (2–3 weeks)
- [ ] Add LangGraph + Claude/GPT integration
- [ ] Build basic agent loop (message → tool → response)
- [ ] Define 5–10 core tools (vendor data queries, order execution, analysis)
- [ ] Implement checkpoints (persistent conversation memory)

### Phase 2: Frontend (1–2 weeks)
- [ ] Replace Nextra docs with Next.js chat UI
- [ ] Add Vercel AI SDK streaming integration
- [ ] Build Gen UI components (dosage tables, charts as React components)

### Phase 3: Security (2–3 weeks)
- [ ] Okta/AD OIDC integration
- [ ] Identity forwarding middleware
- [ ] Cedar policy engine integration
- [ ] Vendor data scoping enforcement

### Phase 4: Data Integration (1–2 weeks)
- [ ] MCP server for agent ↔ Dagster pipeline communication
- [ ] Vector embeddings for RAG (patents, screenshots)
- [ ] Semantic search over multimodal sources

### Phase 5: Validation (1 week)
- [ ] Prompt testing framework
- [ ] Agent workflow simulations
- [ ] End-to-end integration tests
- [ ] Cost tracking and optimization

**Total Effort**: 7–11 weeks for production-ready system

---

## Examples: What Complete System Would Look Like

### Example 1: Vendor Queries Generative UI
```typescript
// Agent response: structured data + React component
{
  "type": "generative_ui",
  "component": <DosageTable data={agent_output.dosage_data} />,
  "reasoning": "Vendor received 5 new orders with high margin potential",
  "next_action": "Execute 3 low-risk orders? (Approve/Deny)"
}
```

### Example 2: Identity Boundary Enforcement
```python
# User: vendor_seller_123 from Okta
# Agent: "Show me all orders"
# Result: Only vendor_seller_123's orders returned (via Cedar policy)

# Attempt by vendor_seller_123 to see competitor data:
# Agent: "I cannot access other vendors' data (policy: vendor_isolation)"
```

### Example 3: Checkpoint/Approval Gate
```
User: "Execute $100K pricing adjustment"
    ↓
Agent: "This requires approval. You have authority level 2, 
        threshold is level 3. Request escalation? (Y/N)"
        [Paused checkpoint]
    ↓
Manager approval received
    ↓
Agent: "Escalation approved. Executing pricing adjustment... Done."
```

### Example 4: MCP + RAG Integration
```
User: "Do we have any patent conflicts with this product?"
    ↓
Agent: "Searching patent database via MCP..."
    ↓
MCP queries vector DB: embeddings similar to new product
    ↓
MCP retrieves top-3 patents + risk assessment from PDFs
    ↓
Agent: "Found 2 potential conflicts in patents US10123456 and US10654321.
        Risk level: medium. I recommend legal review."
```

---

## Conclusion

**poc-dagster** is an **excellent data orchestration POC**, but it is **not** an AI Agent framework. It demonstrates professional Dagster patterns that would serve as the data layer of a larger agent system, but you would need to build Layers 1–3 from scratch.

**Decision Point**: Do you want to:
1. **Expand this into a full AI agent system** (7–11 week effort, major rewrite)
2. **Keep this as reference documentation** for future Dagster projects (current state is valuable)
3. **Archive and start fresh** with LangGraph + Next.js as the primary framework

**Recommendation**: Archive with praise for Dagster mastery. This repo demonstrates advanced patterns but isn't the foundation for agent systems. Start a new `ai-agent-stack` repo with LangGraph as the core.

