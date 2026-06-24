# 4-Layer AI Agent Architecture Diagram

## System Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER (Web Browser)                          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Vercel AI SDK Chat Interface                                       │  │
│  │ - Real-time token streaming via Server-Sent Events (SSE)          │  │
│  │ - Generative UI renderer: Dynamic React components                │  │
│  │ - Example: DosageTable, InteractionChart, ApprovalWorkflow        │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────┬──────────────────────────────────┘
                                          │
                    ┌─────────────────────▼──────────────────────┐
                    │ POST /api/chat + Authorization Header      │
                    │ Bearer {Okta JWT with vendor_id claim}     │
                    └─────────────────────┬──────────────────────┘
                                          │
┌─────────────────────────────────────────▼──────────────────────────────────┐
│                    LAYER 1: FRONTEND API GATEWAY                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Next.js /api/chat Route (app/api/chat/route.ts)                    │  │
│  │ ├─ Extract Authorization header                                    │  │
│  │ ├─ Call streamText() with LLM model                               │  │
│  │ ├─ Return ReadableStream (tokens streamed in real-time)           │  │
│  │ └─ Pipe through toAIStreamResponse()                              │  │
│  │                                                                    │  │
│  │ POST /api/gen-ui Route                                            │  │
│  │ ├─ Receive query + vendorId                                       │  │
│  │ ├─ Call generateObject() with component schema                    │  │
│  │ └─ Return structured component definition (type + props)          │  │
│  └────────────────────────┬────────────────────────────────────────────┘  │
│                           │                                                 │
│                           │ Forward Identity + Token                        │
│                           ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Identity Forwarding Middleware                                      │  │
│  │ ├─ Extract Okta JWT from Authorization header                     │  │
│  │ ├─ Validate signature with Okta JWKS endpoint                     │  │
│  │ ├─ Extract claims: sub (user_id), email, custom:vendor_id        │  │
│  │ ├─ Add forwarding headers for downstream services:               │  │
│  │ │  ├─ X-User-ID: {sub}                                           │  │
│  │ │  ├─ X-Vendor-ID: {vendor_id}                                   │  │
│  │ │  ├─ X-Forwarded-Auth: {token}                                  │  │
│  │ │  └─ X-Forwarded-Email: {email}                                 │  │
│  │ └─ Call Cedar policy engine for authorization check               │  │
│  └────────────────────────┬────────────────────────────────────────────┘  │
└──────────────────────────▼─────────────────────────────────────────────────┘
                                                       │
            ┌──────────────▼──────────────┐
            │ Cedar Policy Decision Point │
            │ Action: ViewVendorData      │
            │ Principal: User::{user_id}  │
            │ Resource: Vendor::{vendor_id}
            │ Decision: Allow/Deny        │
            └──────────────┬──────────────┘
                                                       │
        (Allow: Continue)  │  (Deny: Return 403)
                                                       │
┌──────────────────────────▼──────────────────────────────────────────────────┐
│                    LAYER 2: ORCHESTRATION (LangGraph)                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ LangGraph Agent Loop (Cyclical)                                     │ │
│  │                                                                      │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │ AgentState (TypedDict)                                      │   │ │
│  │  │ ├─ messages: List[BaseMessage] (accumulate with operator)  │   │ │
│  │  │ ├─ vendor_id: str (immutable - enforced boundary)          │   │ │
│  │  │ ├─ context: dict (vendor data context from MCP)           │   │ │
│  │  │ ├─ approval_status: str (awaiting_approval/executing)     │   │ │
│  │  │ └─ checkpoint_id: str (for resumption)                    │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  │                          │                                          │ │
│  │  ┌───────────────────────▼────────────────────────────────────┐   │ │
│  │  │ Node 1: agent_node (THINK)                                │   │ │
│  │  │ ├─ Input: Current state + messages history               │   │ │
│  │  │ ├─ LLM invocation with tool_choice="auto"               │   │ │
│  │  │ ├─ Output: Response with tool_calls (if needed)         │   │ │
│  │  │ └─ Checkpoint ID: decision_{message_count}              │   │ │
│  │  └───────────────────────┬────────────────────────────────────┘   │ │
│  │                          │                                          │ │
│  │                    [Conditional Router]                            │ │
│  │                    Has tool_calls?                                 │ │
│  │                    YES → execute_tools  NO → END                  │ │
│  │                          │                  │                      │ │
│  │  ┌───────────────────────▼────────────────┐ │                     │ │
│  │  │ Node 2: tool_execution_node (EXECUTE)  │ │                     │ │
│  │  │ ├─ Input: tool_calls from LLM          │ │                     │ │
│  │  │ ├─ VENDOR BOUNDARY CHECK:              │ │                     │ │
│  │  │ │  validate_vendor_access(            │ │                     │ │
│  │  │ │    vendor_id, tool_name)             │ │                     │ │
│  │  │ ├─ Execute allowed tools via MCP       │ │                     │ │
│  │  │ ├─ Collect results                     │ │                     │ │
│  │  │ └─ Return tool responses               │ │                     │ │
│  │  └───────────────────────┬────────────────┘ │                     │ │
│  │                          │                  │                      │ │
│  │  ┌───────────────────────▼────────────────────────────────────┐   │ │
│  │  │ Node 3: approval_node (CHECKPOINT)                        │   │ │
│  │  │ ├─ Pause execution                                        │   │ │
│  │  │ ├─ Save checkpoint to database                           │   │ │
│  │  │ ├─ Status: awaiting_approval                            │   │ │
│  │  │ ├─ Wait for human approval via API                       │   │ │
│  │  │ └─ Resume with approval_decision injected               │   │ │
│  │  └───────────────────────┬────────────────────────────────────┘   │ │
│  │                          │                                          │ │
│  │                    [Loop Back to agent_node]                       │ │
│  │                                                                      │ │
│  │  Graph compiled with SqliteSaver checkpointer:                     │ │
│  │  ├─ Persistence layer for graph state                             │ │
│  │  ├─ Thread ID tracking for multiple conversations                 │ │
│  │  └─ Recovery from failures                                         │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  Integration Points with Other Layers:                                     │
│  ├─ Call MCP servers (Layer 4) from tool_execution_node                   │
│  ├─ Forward X-Vendor-ID headers to enforce boundaries                     │
│  └─ Store checkpoints in database with identity context                  │
└──────────────────────────┬──────────────────────────────────────────────────┘
                                                       │
        ┌──────────────────▼──────────────────┐
        │ Tool Call to MCP + Identity Headers │
        │ Headers: X-Vendor-ID, X-User-ID    │
        └──────────────────┬──────────────────┘
                                                       │
┌──────────────────────────▼──────────────────────────────────────────────────┐
│                    LAYER 3: RUNTIME (AWS AgentCore Lambda)                     │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ AWS Lambda Handler                                                  │ │
│  │ ├─ Runtime: nodejs / python / custom                              │ │
│  │ ├─ AgentCore: AWS managed runtime for agent execution             │ │
│  │ ├─ Input: API Gateway event with identity context               │ │
│  │ └─ Output: Agent response (streamed to Layer 1)                 │ │
│  │                                                                    │ │
│  │ Identity Context Binding:                                        │ │
│  │ ├─ Extract from API Gateway authorizer:                         │ │
│  │ │  ├─ event.requestContext.authorizer.claims['sub']            │ │
│  │ │  └─ event.requestContext.authorizer.claims['vendor_id']      │ │
│  │ ├─ Bind to AgentCore runtime:                                   │ │
│  │ │  └─ AgentCore(identity_context={user_id, vendor_id, token})  │ │
│  │ └─ Automatic enforcement: all operations scoped to vendor_id   │ │
│  │                                                                    │ │
│  │ Policy Engine Integration:                                       │ │
│  │ ├─ Enforce Cedar policies at runtime                            │ │
│  │ ├─ policy_engine: AgentPolicyEngine.CEDAR                       │ │
│  │ └─ Every tool execution checked before execution               │ │
│  │                                                                    │ │
│  │ Data Source Configuration:                                       │ │
│  │ ├─ DataSource.DUCKDB (structured vendor data)                   │ │
│  │ ├─ DataSource.MCP (protocol-based access)                       │ │
│  │ └─ DataSource.EMBEDDINGS (multimodal context)                   │ │
│  │                                                                    │ │
│  │ Monitoring & Tracing:                                           │ │
│  │ ├─ AWS CloudWatch Logs (Lambda execution logs)                  │ │
│  │ ├─ X-Ray Tracing (distributed tracing across layers)           │ │
│  │ └─ Metrics: execution time, error rate, vendor isolation        │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────────────────┘
                                                       │
            ┌──────────────▼──────────────┐
            │ Query Results (JSON) to     │
            │ Data Layer (MCP)            │
            └──────────────┬──────────────┘
                                                       │
┌──────────────────────────▼──────────────────────────────────────────────────┐
│                LAYER 4: DATA LAYER (MCP + Multimodal)                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ MCP Server (Model Context Protocol)                                 │ │
│  │                                                                      │ │
│  │ Tools Exposed:                                                      │ │
│  │ ├─ query_dosage_data(vendor_id, drug_name?)                        │ │
│  │ │  └─ DuckDB Query: SELECT FROM dosage_database WHERE vendor_id   │ │
│  │ ├─ check_interactions(vendor_id, drug_list)                        │ │
│  │ │  └─ DuckDB Query: SELECT FROM drug_interactions                 │ │
│  │ └─ get_vendor_approvals(vendor_id, status?)                        │ │
│  │    └─ DuckDB Query: SELECT FROM vendor_approvals WHERE vendor_id  │ │
│  │                                                                      │ │
│  │ Vendor Boundary Enforcement:                                       │ │
│  │ ├─ Accept X-Vendor-ID header                                       │ │
│  │ ├─ Inject into all queries as WHERE vendor_id = {X-Vendor-ID}    │ │
│  │ └─ Reject requests without valid vendor_id                        │ │
│  └─────────────────────┬──────────────────────────────────────────────┘ │
│                        │                                                  │
│  ┌─────────────────────▼──────────────────────────────────────────────┐ │
│  │ DuckDB Data Store (Vendor-Scoped Views)                           │ │
│  │ ├─ dosage_database (indexed on vendor_id)                         │ │
│  │ ├─ drug_interactions (indexed on vendor_id)                       │ │
│  │ ├─ vendor_approvals (indexed on vendor_id)                        │ │
│  │ └─ All queries filtered by WHERE vendor_id = {boundary}          │ │
│  └─────────────────────┬──────────────────────────────────────────────┘ │
│                        │                                                  │
│  ┌─────────────────────▼──────────────────────────────────────────────┐ │
│  │ Multimodal Embeddings Index                                        │ │
│  │                                                                     │ │
│  │ Input Sources:                                                    │ │
│  │ ├─ Patent PDFs (PyPDF2 extraction)                               │ │
│  │ │  └─ Extract text per page + store as documents                │ │
│  │ ├─ Screenshots (Tesseract OCR)                                   │ │
│  │ │  └─ OCR text + visual embedding via CLIP                     │ │
│  │ └─ Video Frames (OpenCV + Tesseract)                            │ │
│  │    └─ Sample frames + OCR + visual embeddings                  │ │
│  │                                                                     │ │
│  │ Processing Pipeline:                                             │ │
│  │ ├─ Text embedding: all-MiniLM-L6-v2 (semantic text)            │ │
│  │ ├─ Image embedding: clip-vit-b-32 (vision-language)            │ │
│  │ ├─ Unified vector store indexed for cosine similarity           │ │
│  │ └─ Search function: search_across_modalities(query, top_k=5)   │ │
│  │                                                                     │ │
│  │ Agent Integration:                                               │ │
│  │ ├─ RAG Step: Retrieve context before agent reasoning            │ │
│  │ ├─ Inject into system prompt: "Relevant vendor context: {...}"  │ │
│  │ └─ Improves decision quality without increasing vendor access  │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────────────────┘
                                                       │
                ┌──────────▼──────────┐
                │ Query Results (JSON) │
                └──────────┬───────────┘
                                                       │
┌──────────────────────────▼──────────────────────────────────────────────────┐
│               LAYER 1: FRONTEND RESPONSE STREAMING                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ SSE Stream Response (app/api/chat/route.ts)                         │ │
│  │ ├─ Token-by-token streaming for real-time UI updates              │ │
│  │ ├─ Format: data: {token}\n\n                                      │ │
│  │ └─ Client receives and appends to chat immediately                │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │ Gen UI Component Rendering                                          │ │
│  │ ├─ When response contains structured component definition          │ │
│  │ ├─ GenUIRenderer matches componentDef.type → React component     │ │
│  │ ├─ Examples:                                                       │ │
│  │ │  ├─ type: "dosage_table" → DosageTable component              │ │
│  │ │  ├─ type: "interaction_chart" → InteractionChart component    │ │
│  │ │  ├─ type: "approval_workflow" → ApprovalWorkflow component    │ │
│  │ │  └─ type: "metrics_dashboard" → MetricsDashboard component    │ │
│  │ └─ Components receive props from LLM (live interactive rendering)│ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  Result: User sees streaming text + embedded live React components         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Security Boundaries

```text
┌──────────────────────────────────────────────────────────────────┐
│                    VENDOR ISOLATION BOUNDARY                     │
│                                                                  │
│  vendor_id = "vendor_123" (immutable across entire flow)        │
│                                                                  │
│  ┌─ Layer 1 (Frontend API Gateway)                              │
│  │  ├─ Extract vendor_id from Okta JWT custom claim             │
│  │  └─ Identity Forwarding Middleware:                          │
│  │     └─ Validate with Cedar: Principal can access Resource    │
│  │        Resource scoped to Vendor::{vendor_id}                │
│  │                                                               │
│  ├─ Layer 2 (LangGraph Orchestration)                           │
│  │  └─ AgentState.vendor_id = immutable field                   │
│  │     All tool calls validated against this                    │
│  │                                                               │
│  ├─ Layer 3 (Runtime - AWS AgentCore Lambda)                    │
│  │  └─ AgentCore identity_context binding                       │
│  │     All operations automatically scoped                      │
│  │                                                               │
│  └─ Layer 4 (Data Layer - MCP + DuckDB)                         │
│     ├─ X-Vendor-ID header required for all requests             │
│     └─ Query WHERE vendor_id = {X-Vendor-ID}                   │
│        Injection attempts rejected                              │
│                                                                  │
│  ⚠️  NO CROSS-VENDOR DATA ACCESS POSSIBLE                       │
│     ✓  Vendor A cannot query Vendor B data                      │
│     ✓  Vendor A cannot access Vendor B documents                │
│     ✓  Vendor A cannot execute Vendor B-scoped tools            │
└──────────────────────────────────────────────────────────────────┘
```

## Checkpoint & Approval Gate Flow

```text
Agent Loop Iteration 1
├─ Agent decides: "Need human approval for drug X"
├─ Creates tool call to request_approval(drug_x)
│
Approval Node (Checkpoint)
├─ Save state to database:
│  ├─ thread_id: "conv_123"
│  ├─ checkpoint_id: "approval_step_5"
│  ├─ state_snapshot: {messages, vendor_id, context}
│  └─ timestamp: 2024-01-15T10:30:00Z
│
├─ Status: "awaiting_approval"
├─ Wait for human decision
│
Human Approves (POST /agent/resume)
├─ Load checkpoint from database
├─ Inject approval_decision into message stream
├─ Append: {"role": "user", "content": "Approved"}
│
Agent Loop Iteration 2 (Resumed)
├─ Continue with next_node(state + approval_decision)
└─ Complete workflow or request another approval
```

---