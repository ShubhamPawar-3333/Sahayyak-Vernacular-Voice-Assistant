# Implementation Plan: Sahayyak Voice Assistant

## Project Structure

```
Sahayyak-Vernacular-Voice-Assistant/
├── app/
│   ├── __init__.py
│   ├── main.py              # Streamlit app entry point
│   ├── config.py            # Configuration & env vars
│   └── utils.py             # Helper functions
├── modules/
│   ├── __init__.py
│   ├── speech.py            # Bhashini ASR/TTS client
│   ├── llm.py               # Gemini LLM integration
│   ├── rag.py               # RAG pipeline with ChromaDB
│   └── eligibility.py       # Scheme eligibility engine
├── data/
│   ├── schemes/             # Scheme documents (MD/PDF)
│   └── vectordb/            # ChromaDB persistence
├── docs/                    # Documentation
├── tests/                   # Unit tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## Weekly Milestones

### Week 1: Foundation
- [ ] Initialize Python project with dependencies
- [ ] Implement Bhashini API client (ASR + TTS)
- [ ] Test speech-to-text with Marathi sample

### Week 2: AI Core
- [ ] Integrate Gemini API for response generation
- [ ] Build RAG pipeline with ChromaDB
- [ ] Implement intent and entity extraction

### Week 3: Knowledge Base
- [ ] Collect and structure 12 scheme documents
- [ ] Build eligibility checking logic
- [ ] Test end-to-end query flow

### Week 4: User Interface
- [ ] Build Streamlit voice interface
- [ ] Add conversation history display
- [ ] Implement audio playback

### Week 5: Deploy & Polish
- [ ] Deploy to HuggingFace Spaces
- [ ] Create demo video
- [ ] Write README and documentation

---

## Dependencies

```
streamlit>=1.30.0
langchain>=0.1.0
langchain-google-genai>=1.0.0   # Gemini via LangChain
langchain-community>=0.0.20     # Vector store integrations
chromadb>=0.4.0
requests>=2.31.0
python-dotenv>=1.0.0
pydub>=0.25.1
langsmith>=0.1.0                # LLMOps: Tracing & Eval (optional)
```

---

## Verification

### Test 1: Voice Flow
```bash
streamlit run app/main.py
# Say: "PM Kisan बद्दल सांगा"
# Expected: Marathi audio response with scheme info
```

### Test 2: Eligibility
```bash
# Say: "मी शेतकरी आहे, 2 एकर जमीन"
# Expected: List of 5+ eligible schemes
```

---

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Bhashini API down | Whisper fallback |
| Gemini rate limit | Request queuing |
| Poor ASR accuracy | Retry + confirmation |
