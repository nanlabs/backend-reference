# Reference Guide

This directory contains documentation for the Dagster AI Orchestration Framework.

## Files

- **README.md** - This file
- **architecture-diagram.md** - System architecture visualizations
- **implementation-blueprint.md** - Production code templates

## Getting Started

1. Start with `architecture-diagram.md` to understand system design
2. Review `implementation-blueprint.md` for code examples
3. Adapt templates to your requirements

## Architecture Layers

The framework uses a 5-layer architecture:

- **Layer 1**: Frontend (Vercel AI SDK + React)
- **Layer 2**: Orchestration (LangGraph state machine)
- **Layer 3**: Runtime (AWS Lambda + Okta + Cedar)
- **Layer 4**: Data (MCP + DuckDB + Embeddings)
- **Layer 5**: Validation (Prompt evals + Testing)

Each layer maintains vendor isolation and identity context propagation.

## Key Patterns

### Vendor Isolation

Multi-tenant safety enforced through:

- Request scoping in frontend
- State partitioning in orchestration
- JWT claims in runtime
- Query filtering in data layer

### Identity Forwarding

Stateless JWT propagation through request headers.

### Checkpoint Management

State persistence for fault tolerance and human approval gates.

### Multimodal Embeddings

Semantic search across PDFs, screenshots, and video frames.

## Implementation Timeline

Building from scratch:

- Weeks 1-2: Layer 2 + Layer 1
- Weeks 3-5: Layer 3 + Gen UI
- Weeks 6-8: Layer 4 (MCP + Embeddings)
- Weeks 9-11: Layer 5 (Validation)

Total: 7-11 weeks to production