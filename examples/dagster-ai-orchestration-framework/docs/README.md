# Dagster AI Orchestration Framework - Reference Implementation

Production-ready templates and architecture documentation for building a 4-layer AI Agent platform with Dagster data orchestration as the foundation.

---

## 📁 Contents

### 1. **README.md** (this file)
Quick reference guide for the framework components.

### 2. **architecture-diagram.md**
Complete system architecture visualization showing:
- 5-layer architecture (Frontend → Orchestration → Runtime → Data → Validation)
- Data flow from client request to response
- Vendor isolation boundaries
- Security checkpoints and policy enforcement
- Checkpoint/approval gate state machine

### 3. **implementation-blueprint.md**
Production-ready code templates for all 5 layers:
- **Layer 1**: Vercel AI SDK streaming chat endpoint + Gen UI React renderer
- **Layer 2**: LangGraph cyclical agent loop + checkpoint persistence
- **Layer 3**: Okta JWT extraction + Cedar policy engine integration
- **Layer 4**: MCP server for vendor-scoped queries + multimodal embeddings
- **Layer 5**: Prompt testing framework (evals) + workflow validation

All code is copy-paste-ready and follows best practices.

---

## 🎯 Use Cases

### For Architects
1. Review `architecture-diagram.md` to understand the 5-layer model
2. Check `implementation-blueprint.md` for concrete patterns

### For Implementation Teams
1. Start with `implementation-blueprint.md`
2. Reference `architecture-diagram.md` for integration points
3. Adapt templates to your specific requirements

### For Reference
- Use as a template for building AI agent platforms
- Reference for data layer integration patterns
- Model for vendor isolation and security boundaries

---

## 🚀 Key Features

- ✅ Production-grade architecture patterns
- ✅ Vendor isolation enforced at every layer
- ✅ Security boundaries with Cedar policy engine
- ✅ Checkpoint-based workflow state management
- ✅ Multimodal data processing (text, images, video)
- ✅ Type-safe implementation examples

---

## 📊 Architecture Overview

```text
┌─ Layer 1: Frontend (Vercel AI SDK + React)
├─ Layer 2: Orchestration (LangGraph state machine)
├─ Layer 3: Runtime (AWS Lambda + Identity + Cedar)
├─ Layer 4: Data (MCP + DuckDB + Embeddings)
└─ Layer 5: Validation (Prompt evals + Testing)
```

All layers maintain vendor isolation and identity context propagation.

---

## 🔗 References

- **architecture-diagram.md**: System integration details
- **implementation-blueprint.md**: Code templates and patterns

For questions about specific layers or patterns, refer to the implementation-blueprint.md code examples.
