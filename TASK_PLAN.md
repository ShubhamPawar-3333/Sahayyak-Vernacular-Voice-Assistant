# Sahayyak - Task Plan

## Git Strategy
```
main ──────────────────────────●  (release)
develop ●───●───●───●───●───●──●  (integration)
        └───┴───┴───┴───┴───┘
            feature branches
```

**Workflow:** Task → Auto commit/push → CI runs → "Next Task"

---

## Phase 1: Setup & Infrastructure
**Branch:** `develop`

### Task 1.1: Configuration Module
- [ ] Create `app/config.py` with env loading
- [ ] Add structured logging setup
- [ ] Update `.env.example`

### Task 1.2: Base Classes & Exceptions
- [ ] Create abstract interfaces for Speech, LLM, RAG
- [ ] Define custom exception hierarchy
- [ ] Add type hints

---

## Phase 2: Core AI Pipeline
**Branch:** `feature/core-pipeline`

### Task 2.1: Speech Module (Bhashini)
- [ ] Implement `BhashiniClient` class
- [ ] ASR (speech-to-text) for Marathi/Hindi
- [ ] TTS (text-to-speech) for Marathi
- [ ] Error handling + retries

### Task 2.2: LLM Integration (Gemini)
- [ ] Implement `LLMService` with LangChain
- [ ] Create prompt templates
- [ ] Add conversation memory

### Task 2.3: RAG Pipeline
- [ ] Document loader for Markdown
- [ ] ChromaDB vector store setup
- [ ] Retrieval chain with citations

### Task 2.4: Pipeline Integration
- [ ] Connect Speech → LLM → RAG
- [ ] Create unified `QueryPipeline` class
- [ ] End-to-end test

---

## Phase 3: Knowledge Base
**Branch:** `feature/knowledge-base`

### Task 3.1: Scheme Data Collection
- [ ] 5 central schemes (PM Kisan, Ayushman, etc.)
- [ ] 7 Maharashtra schemes
- [ ] Structured Markdown format

### Task 3.2: Eligibility Engine
- [ ] User profile model
- [ ] Rule-based eligibility checker
- [ ] Integration with RAG

---

## Phase 4: User Interface
**Branch:** `feature/ui`

### Task 4.1: Streamlit Base
- [ ] Main app with page config
- [ ] Voice recording component
- [ ] Audio playback

### Task 4.2: Chat Interface
- [ ] Conversation display
- [ ] Session state management
- [ ] Scheme result cards

### Task 4.3: Polish & Branding
- [ ] Loading states
- [ ] Error handling UI
- [ ] Styling + logo

---

## Phase 5: Quality & LLMOps
**Branch:** `feature/quality`

### Task 5.1: Test Suite
- [ ] Unit tests for all modules
- [ ] Evaluation dataset (30 test queries)
- [ ] 80%+ code coverage

### Task 5.2: CI/CD Pipeline
- [ ] GitHub Actions workflow
- [ ] Lint + test on push
- [ ] Coverage reporting

### Task 5.3: LangSmith Integration
- [ ] Tracing configuration
- [ ] Prompt versioning
- [ ] Evaluation runs

---

## Phase 6: Deployment
**Branch:** `release/v1.0`

### Task 6.1: HuggingFace Deployment
- [ ] Space configuration
- [ ] Secrets setup
- [ ] Auto-deploy from main

### Task 6.2: Documentation & Demo
- [ ] Final README
- [ ] Architecture diagram
- [ ] Demo video recording

---

## Progress Tracker

| Phase | Status | Tasks |
|-------|--------|-------|
| 1. Setup | 🟡 In Progress | 0/2 |
| 2. Core AI | ⏳ Pending | 0/4 |
| 3. Knowledge | ⏳ Pending | 0/2 |
| 4. UI | ⏳ Pending | 0/3 |
| 5. Quality | ⏳ Pending | 0/3 |
| 6. Deploy | ⏳ Pending | 0/2 |

**Total: 16 tasks**

---

## Execution Rules

1. Wait for **"Next Task"** command
2. Auto commit + push after each task
3. CI must pass before next task
4. Update this tracker after each task
