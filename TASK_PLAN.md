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

### Task 1.1: Configuration Module ✅
- [x] Create `app/config.py` with env loading
- [x] Add structured logging setup
- [x] Update `.env.example`

### Task 1.2: Base Classes & Exceptions ✅
- [x] Create abstract interfaces for Speech, LLM, RAG
- [x] Define custom exception hierarchy
- [x] Add type hints

---

## Phase 2: Core AI Pipeline
**Branch:** `feature/core-pipeline`

### Task 2.1: Speech Module (Bhashini) ✅
- [x] Implement `BhashiniClient` class
- [x] ASR (speech-to-text) for Marathi/Hindi
- [x] TTS (text-to-speech) for Marathi
- [x] Error handling + retries

### Task 2.2: LLM Integration (Sarvam-M + Gemini) ✅
- [x] Implement `LLMService` with LangChain (Sarvam-M primary, Gemini fallback)
- [x] Create prompt templates (`modules/prompts.py`)
- [x] Add conversation memory (10-turn window)

### Task 2.3: RAG Pipeline ✅
- [x] Document loader for Markdown
- [x] ChromaDB vector store setup
- [x] Retrieval chain with multilingual embeddings

### Task 2.4: Pipeline Integration ✅
- [x] Connect Speech → LLM → RAG
- [x] Create unified `QueryPipeline` class
- [x] End-to-end voice + text pipelines

---

## Phase 3: Knowledge Base
**Branch:** `feature/knowledge-base`

### Task 3.1: Scheme Data Collection ✅
- [x] 5 central schemes (PM Kisan, Ayushman, PM Awas, MGNREGA, Ujjwala)
- [x] 4 Maharashtra schemes (MJPJAY, Shetkari Samman, Ladki Bahin, Gharkul)
- [x] Structured Markdown with source citations & verification dates

### Task 3.2: Eligibility Engine ✅
- [x] `UserProfile` dataclass with demographics, economic, social fields
- [x] Rule-based eligibility checker for all 9 schemes
- [x] Confidence scoring + criteria tracking (met/unmet/missing)

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
| 1. Setup | ✅ Complete | 2/2 |
| 2. Core AI | ✅ Complete | 4/4 |
| 3. Knowledge | ✅ Complete | 2/2 |
| 4. UI | ⏳ Pending | 0/3 |
| 5. Quality | ⏳ Pending | 0/3 |
| 6. Deploy | ⏳ Pending | 0/2 |

**Total: 8/16 tasks complete**

---

## Execution Rules

1. Wait for **"Next Task"** command
2. Auto commit + push after each task
3. CI must pass before next task
4. Update this tracker after each task
