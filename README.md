# Sahayyak (सहाय्यक) - Vernacular Voice Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain](https://img.shields.io/badge/LangChain-powered-green.svg)](https://langchain.com/)

> Voice-first AI assistant helping Maharashtra citizens access government schemes in Marathi and Hindi.

## 🎯 Problem

- 90% of Maharashtra's rural population prefers Marathi over English
- 20,000+ government schemes exist, but citizens don't know their eligibility
- Digital divide prevents access to online portals

## 🚀 Solution

A voice-enabled assistant that:
- Accepts voice queries in **Marathi/Hindi**
- Checks **eligibility** for government schemes
- Provides **step-by-step guidance** for applications
- Integrates **Maharashtra-specific** services (MahaDBT, Mandi prices)

## 🏗️ Architecture

```
Voice → Bhashini ASR → LangChain + Gemini → RAG → Response → Bhashini TTS → Voice
```

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| Speech | Bhashini API (ASR/TTS) |
| LLM | Google Gemini via LangChain |
| RAG | ChromaDB + LangChain |
| UI | Streamlit |
| Observability | LangSmith |

## 🛠️ Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Sahayyak-Vernacular-Voice-Assistant.git
cd Sahayyak-Vernacular-Voice-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run application
streamlit run app/main.py
```

## 📁 Project Structure

```
├── app/                    # Streamlit application
├── modules/                # Core modules (speech, llm, rag)
├── data/                   # Scheme documents & vector store
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `BHASHINI_USER_ID` | Bhashini platform user ID |
| `BHASHINI_ULCA_API_KEY` | ULCA API key |
| `BHASHINI_INFERENCE_KEY` | Inference API key |
| `GOOGLE_API_KEY` | Gemini API key |
| `LANGSMITH_API_KEY` | LangSmith API key (optional) |

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions welcome! Please read the contributing guidelines first.

---

**Built with ❤️ for Maharashtra**
