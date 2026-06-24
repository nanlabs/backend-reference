# POC-Dagster: Decision Framework & Archival Guidance

## Executive Summary

**Current State**: `poc-dagster` is a **production-grade Dagster data pipeline POC**, not an AI agent framework.

**Assessment**: The repository demonstrates excellent orchestration patterns but is fundamentally incompatible with a 4-layer AI agent architecture.

**Overall Completeness Score**: **18%** (Layer 4 data patterns only; Layers 1-3 absent entirely)

**Recommendation**: **ARCHIVE** (with caveats for preservation)

---

## Three Decision Paths

### PATH 1: ARCHIVE ✅ (Recommended)

#### Rationale
- `poc-dagster` serves its original purpose: a reference implementation of production-grade Dagster patterns
- Repurposing as AI agent infrastructure would create architectural tension (linear DAGs vs. cyclical loops)
- Starting fresh avoids coupling issues and technical debt
- Clear separation of concerns: data orchestration vs. agent orchestration

#### What This Means
- Mark repository as `archived` on GitHub
- Preserve as reference for future Dagster implementations
- Document lessons learned in architecture wiki
- Create new repository for 4-layer agent stack

#### Archival Checklist
```
□ Final documentation update (add note: "Archived as reference POC")
□ Create GitHub Release with final version tag (v1.0-final)
□ Enable "Archive" setting in repository settings
□ Update README with archival note and migration path to new agent repo
□ Notify stakeholders: poc-dagster role is complete, agent stack is new initiative
□ Commit final state with descriptive commit message:
  "Archive poc-dagster: completed Dagster POC reference implementation"
□ Pin relevant documentation to Confluence/Wiki for future reference
□ Create quick-start guide for anyone referencing this POC:
  - Where to find Dagster patterns (definitions.py)
  - Where to find test patterns (test_pipeline.py)
  - Link to new agent repo for next phase
```

#### Timeline
- **Immediate** (1-2 hours):
  - Add archival note to README
  - Create final documentation
  - Tag release
  - Notify team
- **Complete**: Repository marked archived, documentation preserved

#### Migration Path to New Agent Stack
1. **New Repository**: `ai-agent-platform` or `poc-agent-orchestration`
2. **Initial Commit**: Copy Layer 1-5 blueprints from this assessment
3. **Setup**: Install dependencies, structure project
4. **Phase 1**: Implement Layer 1 (Frontend) + Layer 2 (LangGraph)
5. **Phase 2**: Integrate Layer 3 (Identity/Cedar) + Layer 4 (MCP/Embeddings)
6. **Phase 3**: Implement Layer 5 (Validation) + integration tests
7. **Phase 4**: User testing and hardening
8. **Timeline**: 7-11 weeks total

---

### PATH 2: START FRESH (Recommended Alternative)

Use this if stakeholders want a cleaner slate with no dependencies on existing code.

#### Setup Steps

1. **Create new repository**
   ```bash
   git init poc-agent-orchestration
   cd poc-agent-orchestration
   ```

2. **Initialize Python project** (Layer 2-5 backend)
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install langgraph langchain openai duckdb pydantic fastapi uvicorn
   pip install sentence-transformers torch PyPDF2 opencv-python pytesseract
   ```

3. **Initialize Next.js project** (Layer 1 frontend)
   ```bash
   npx create-next-app@latest agent-frontend --typescript --tailwind
   npm install ai @ai-sdk/openai @vercel/ai
   ```

4. **Project Structure**
   ```
   poc-agent-orchestration/
   ├── backend/
   │   ├── agent/
   │   │   ├── graph.py           # LangGraph state machine
   │   │   ├── checkpoints.py     # Persistence layer
   │   │   └── mcp_integration.py # MCP bridge
   │   ├── middleware/
   │   │   └── identity_forwarding.py  # Okta + Cedar
   │   ├── embeddings/
   │   │   └── multimodal_processor.py # PDFs + images + video
   │   ├── mcp_server/
   │   │   └── server.py          # MCP vendor data server
   │   ├── validation/
   │   │   ├── prompt_evals.py    # Prompt testing
   │   │   └── workflow_validation.py
   │   ├── main.py                # FastAPI app
   │   └── requirements.txt
   │
   ├── frontend/
   │   ├── app/
   │   │   ├── api/
   │   │   │   ├── chat/route.ts  # Streaming endpoint
   │   │   │   └── gen-ui/route.ts
   │   │   ├── components/
   │   │   │   ├── GenUIRenderer.tsx
   │   │   │   ├── DosageTable.tsx
   │   │   │   ├── InteractionChart.tsx
   │   │   │   └── ApprovalWorkflow.tsx
   │   │   └── page.tsx
   │   ├── package.json
   │   └── tsconfig.json
   │
   ├── docker-compose.yml         # Local dev: Lambda, Cedar, MCP
   ├── README.md
   └── .github/
       └── workflows/
           ├── test.yml           # Run eval suite
           └── deploy.yml         # AWS Lambda deployment
   ```

5. **Phase Implementation Order**
   - **Week 1-2**: Layer 2 (LangGraph core agent loop)
   - **Week 2-3**: Layer 1 (Frontend streaming chat)
   - **Week 3-4**: Layer 4 (MCP + DuckDB integration)
   - **Week 4-5**: Layer 3 (Identity forwarding + Cedar)
   - **Week 5-6**: Layer 4 (Multimodal embeddings)
   - **Week 6-8**: Layer 5 (Validation framework)
   - **Week 8-11**: Integration, testing, hardening

---

### PATH 3: EXPAND (Not Recommended)

Use this **only if** you have strong architectural constraints forcing reuse of Dagster infrastructure.

#### Why Not Recommended
- **Architectural Mismatch**: Dagster = linear DAGs; Agent = cyclical loops
- **Coupling Risk**: LangGraph checkpointing ≠ Dagster assets/sensors
- **Tech Debt**: Integration layer becomes complex maintenance burden
- **Performance**: Unnecessary overhead from Dagster when not needed

#### If You Must Expand

1. **Create New Module**: `src/poc_dagster/agent/`
   ```
   src/poc_dagster/
   ├── orchestration/     # Existing Dagster patterns
   ├── agent/             # NEW: LangGraph code
   │   ├── graph.py
   │   ├── checkpoints.py
   │   └── tools.py
   └── data/              # Existing DuckDB patterns
   ```

2. **Shared Data Layer**
   - Reuse DuckDB fixtures from `tests/test_pipeline.py`
   - MCP server queries same DuckDB database
   - LangGraph tools invoke DuckDB queries with vendor boundaries

3. **Integration Points**
   ```python
   # src/poc_dagster/agent/tools.py
   from poc_dagster.orchestration.resources import duckdb_resource
   
   def query_vendor_data(vendor_id: str, query: str):
       db = duckdb_resource.get_engine()
       # Use same DuckDB connection as Dagster assets
       return db.execute(query).fetchall()
   ```

4. **Risks to Accept**
   - Mixed concerns in single repository
   - Deployment complexity (Dagster scheduler + Lambda agent runtime)
   - Testing becomes harder (Dagster asset tests + LangGraph state tests)
   - Operational burden: two distinct systems to manage

5. **Success Criteria**
   - ✓ LangGraph executes independently of Dagster
   - ✓ Shared data layer doesn't break either system
   - ✓ Vendor isolation enforced in both contexts
   - ✓ Test suite covers both systems separately

---

## Comparison Matrix

| Dimension | Archive | Start Fresh | Expand |
|-----------|---------|-------------|--------|
| **Timeline** | 2-3 hours | 7-11 weeks | 8-13 weeks |
| **Risk Level** | Low | Medium | High |
| **Maintenance** | Zero | Medium | High |
| **Architectural Clarity** | High | High | Low |
| **Code Reuse** | Patterns only | None | DuckDB only |
| **Deployment Simplicity** | N/A | Medium | Complex |
| **Future Flexibility** | High | High | Low |
| **Cost to Pivot** | Low | Low | Medium-High |
| **Recommendation** | ✅ YES | ✅ YES | ❌ NO |

---

## Preservation Strategy (For Path 1: Archive)

If archiving, preserve these artifacts for future reference:

### 1. Document the POC
Create `ARCHIVE_README.md`:
```markdown
# POC-Dagster Archive

**Status**: Archived - Reference Implementation

## Why Archived
- Completed its purpose as Dagster reference POC
- Next phase requires AI agent framework (LangGraph), not data orchestration
- Starting fresh avoids architectural coupling

## What to Learn From This
- Production-grade Dagster patterns (auto-discovery, resource injection)
- Advanced testing patterns for data pipelines
- Environment-aware configuration management

## See Also
- New agent stack: [poc-agent-orchestration](link-to-new-repo)
- Dagster architecture guide: (internal wiki link)
```

### 2. Reference Preserved Code
Key files to save as templates:

**Resource Injection Pattern** (definitions.py, lines 29-68)
- Use as template for future Dagster projects
- Demonstrates environment-aware setup without singletons

**Test Patterns** (test_pipeline.py, all 428 lines)
- High-quality pytest fixtures
- Data quality validation examples
- Partition testing approach

### 3. Migration Documentation
Create transition guide:
```
POC-Dagster Archival → Agent Stack Bootstrap

1. Where: poc-dagster (archived reference)
2. Next: poc-agent-orchestration (new agent implementation)
3. Reusable patterns:
   - DuckDB schema from poc-dagster/data/ → new agent's data layer
   - Test patterns from poc-dagster/tests/ → new agent's validation layer
4. Reference architecture: See assessment document (internal)
```

---

## Final Recommendation

### ✅ **ARCHIVE** 

**Rationale Summary**:
1. **Clear Separation**: Dagster POC served its purpose; agent framework is distinct
2. **Risk Mitigation**: Start fresh avoids architectural debt
3. **Timeline**: Archival takes 2-3 hours; expansion risks 8-13 weeks with technical debt
4. **Preservation**: Key patterns documented and available for reference
5. **Stakeholder Clarity**: Explicit archival signals phase transition to team

**Action Items (Next 24 Hours)**:
- [ ] Decide: Archive or Start Fresh?
- [ ] If Archive: Update README, tag release, notify team
- [ ] If Start Fresh: Create new repo, begin Phase 1 (Layer 2 + Layer 1)
- [ ] Start Agent Stack Blueprint Immediately: Use implementation-blueprint.md as template

**Timeline to Production**:
- **Archival Path**: 2-3 hours (archive) + 7-11 weeks (build new) = ~11 weeks
- **Fresh Start Path**: 7-11 weeks total
- **Expansion Path**: 8-13 weeks (not recommended due to coupling risk)

---

## Questions for Stakeholders

Before deciding, confirm answers:

1. **Technical Governance**
   - Should poc-dagster remain as Dagster reference? (→ Archive)
   - Or must new agent code live in poc-dagster? (→ Expand)

2. **Timeline Pressure**
   - Can we afford 7-11 weeks for clean implementation? (→ Fresh/Archive)
   - Must we accelerate by reusing existing infrastructure? (→ Expand)

3. **Operational Model**
   - Will you run data pipelines (Dagster) and agents (LangGraph) separately? (→ Archive/Fresh)
   - Or must they co-manage same compute? (→ Expand)

4. **Team Preferences**
   - Maintain single repository? (→ Expand)
   - Or prefer separation of concerns? (→ Archive/Fresh)

