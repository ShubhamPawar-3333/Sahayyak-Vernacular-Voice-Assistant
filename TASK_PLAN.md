# Sahayyak - Detailed Task Plan

## Git Branching Strategy

```
main          ─────●─────────────────────────────────●───── Production
                   │                                 │
develop       ─────●───●───●───●───●───●───●───●────●───── Integration
                   │   │   │   │   │   │   │   │
feature/*     ─────●   │   │   │   │   │   │   │
                       │   │   │   │   │   │   │
                   feat/speech  feat/rag  feat/ui  ...
```

**Branches:**
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches (merged to develop)
- `hotfix/*` - Critical fixes (merged to main + develop)

---

## Phase 0: Project Foundation
**Branch:** `develop` (initial setup)

### Task 0.1: Repository Setup
- [ ] Create GitHub repo "Sahayyak-Vernacular-Voice-Assistant"
- [ ] Initialize with README, .gitignore, LICENSE
- [ ] Create develop branch
- [ ] Set up branch protection rules

### Task 0.2: Project Structure
- [ ] Create folder structure
- [ ] Add requirements.txt
- [ ] Add .env.example
- [ ] Add pyproject.toml (for tools config)
- [ ] Set up pre-commit hooks (black, isort, flake8)

### Task 0.3: Development Environment
- [ ] Create virtual environment setup script
- [ ] Add Makefile for common commands
- [ ] Configure VS Code settings (.vscode/)

---

## Phase 1: Core Infrastructure
**Branch:** `feature/core-infrastructure`

### Task 1.1: Configuration Module
- [ ] Create config.py with environment variable loading
- [ ] Create .env.example with all required variables
- [ ] Add logging configuration

### Task 1.2: Base Classes & Interfaces
- [ ] Define abstract base classes for speech, LLM, RAG
- [ ] Create custom exception classes
- [ ] Set up type hints throughout

---

## Phase 2: Speech Module
**Branch:** `feature/speech-module`

### Task 2.1: Bhashini Client Implementation
- [ ] Implement BhashiniClient class
- [ ] Add pipeline config fetching
- [ ] Add ASR (speech-to-text) method
- [ ] Add TTS (text-to-speech) method
- [ ] Add error handling & retries

### Task 2.2: Whisper Fallback
- [ ] Implement WhisperClient as fallback
- [ ] Create SpeechService facade (auto-fallback)

### Task 2.3: Speech Module Tests
- [ ] Unit tests for BhashiniClient
- [ ] Integration tests with sample audio
- [ ] Mock tests for API failures

---

## Phase 3: LLM Module
**Branch:** `feature/llm-module`

### Task 3.1: Gemini Integration via LangChain
- [ ] Implement GeminiLLM class using langchain-google-genai
- [ ] Add prompt templates for different intents
- [ ] Implement conversation memory

### Task 3.2: Intent & Entity Extraction
- [ ] Create intent classifier chain
- [ ] Create entity extractor chain
- [ ] Define schema for user profile entities

### Task 3.3: LLM Module Tests
- [ ] Unit tests with mocked LLM
- [ ] Test prompt templates
- [ ] Test conversation memory

---

## Phase 4: RAG Pipeline
**Branch:** `feature/rag-pipeline`

### Task 4.1: Document Processing
- [ ] Create document loader for scheme PDFs/Markdown
- [ ] Implement text chunking with overlap
- [ ] Add metadata extraction

### Task 4.2: Vector Store Setup
- [ ] Initialize ChromaDB with persistence
- [ ] Create embedding pipeline using LangChain
- [ ] Implement document ingestion

### Task 4.3: Retrieval Chain
- [ ] Build retrieval chain with reranking
- [ ] Create RAG query method
- [ ] Add source citation

### Task 4.4: RAG Tests
- [ ] Test document ingestion
- [ ] Test retrieval accuracy
- [ ] Benchmark retrieval speed

---

## Phase 5: Knowledge Base
**Branch:** `feature/knowledge-base`

### Task 5.1: Scheme Data Collection
- [ ] Collect 5 central scheme documents
- [ ] Collect 7 Maharashtra scheme documents
- [ ] Structure in consistent Markdown format

### Task 5.2: Eligibility Engine
- [ ] Define eligibility rules schema
- [ ] Implement rule-based eligibility checker
- [ ] Create user profile model

### Task 5.3: Knowledge Base Tests
- [ ] Test eligibility logic
- [ ] Validate scheme data completeness

---

## Phase 6: API Layer (Optional)
**Branch:** `feature/api-layer`

### Task 6.1: FastAPI Backend
- [ ] Create FastAPI app structure
- [ ] Implement /chat endpoint (text)
- [ ] Implement /voice endpoint (audio)
- [ ] Add request/response schemas

### Task 6.2: API Documentation
- [ ] Configure Swagger/OpenAPI docs
- [ ] Add endpoint descriptions
- [ ] Create Postman collection

---

## Phase 7: User Interface
**Branch:** `feature/ui`

### Task 7.1: Streamlit Base Setup
- [ ] Create main.py with page config
- [ ] Implement voice recording component
- [ ] Add audio playback

### Task 7.2: Chat Interface
- [ ] Build conversation display
- [ ] Add session state management
- [ ] Create scheme result cards

### Task 7.3: UI Polish
- [ ] Add loading states
- [ ] Implement error messages
- [ ] Add branding/styling

---

## Phase 8: LLMOps & Observability
**Branch:** `feature/llmops`

### Task 8.1: LangSmith Integration
- [ ] Configure LangSmith tracing
- [ ] Add prompt versioning
- [ ] Set up evaluation datasets

### Task 8.2: Logging & Monitoring
- [ ] Add structured logging
- [ ] Create log aggregation
- [ ] Add basic metrics

---

## Phase 9: Testing & Quality
**Branch:** `feature/testing`

### Task 9.1: Test Suite Completion
- [ ] Achieve 80%+ code coverage
- [ ] Add end-to-end tests
- [ ] Create test fixtures

### Task 9.2: CI/CD Pipeline
- [ ] Set up GitHub Actions workflow
- [ ] Add lint/format checks
- [ ] Add test automation
- [ ] Add coverage reporting

---

## Phase 10: Deployment
**Branch:** `feature/deployment`

### Task 10.1: HuggingFace Spaces Setup
- [ ] Create Space configuration
- [ ] Configure secrets
- [ ] Deploy application

### Task 10.2: Documentation
- [ ] Write comprehensive README
- [ ] Create user guide
- [ ] Add architecture diagram
- [ ] Record demo video

### Task 10.3: Release
- [ ] Merge to main
- [ ] Create GitHub release
- [ ] Tag version 1.0.0

---

## Execution Rules

1. **One task at a time** - Wait for "Next Task" command
2. **Git workflow per task:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/task-name
   # ... do work ...
   git add .
   git commit -m "feat: description"
   git push origin feature/task-name
   # Create PR → Merge to develop
   ```
3. **Code review** - Each task produces working, tested code
4. **Documentation** - Update README/docs with each feature

---

## Current Status

| Phase | Status |
|-------|--------|
| Phase 0 | ⏳ Pending |
| Phase 1 | ⏳ Pending |
| Phase 2 | ⏳ Pending |
| Phase 3 | ⏳ Pending |
| Phase 4 | ⏳ Pending |
| Phase 5 | ⏳ Pending |
| Phase 6 | ⏳ Pending |
| Phase 7 | ⏳ Pending |
| Phase 8 | ⏳ Pending |
| Phase 9 | ⏳ Pending |
| Phase 10 | ⏳ Pending |
