# Dagster AI Orchestration Framework

Reference implementation for building 4-layer AI Agent platforms with production-ready templates and architecture documentation.

## Contents

- **architecture-diagram.md** - System architecture and data flow
- **implementation-blueprint.md** - Production code templates for all layers
- **docs/README.md** - Quick reference guide

## Quick Start

1. Review `docs/README.md` for orientation
2. Study `architecture-diagram.md` to understand system design
3. Use `implementation-blueprint.md` as your implementation guide

## Architecture Overview

5-layer stack:

- Layer 1: Frontend (Vercel AI SDK + Next.js)
- Layer 2: Orchestration (LangGraph)
- Layer 3: Runtime (Okta + Cedar)
- Layer 4: Data (MCP + Embeddings)
- Layer 5: Validation (Prompt evals)

All layers maintain vendor isolation and identity context propagation.

## Key Features

- Production-grade architecture patterns
- Vendor isolation at every layer
- Cedar policy engine integration
- Checkpoint-based state management
- Multimodal data processing

## References

- [Vercel AI SDK](https://sdk.vercel.ai/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Cedar Policy Language](https://www.cedarpolicy.com/)
