# 🗣️ Vernacular Voice Assistant for Maharashtra Government Services

> **Project Name:** Sahayyak (सहाय्यक) - "The Helper"

---

## Problem Statement

- 90% of Maharashtra's rural population prefers Marathi over English
- 20,000+ government schemes exist, but citizens don't know eligibility
- Digital divide prevents access to online portals
- Existing solutions don't cover Maharashtra-specific schemes

---

## Core Features

### 1. Voice-First Interface
| Feature | Description |
|---------|-------------|
| Marathi Speech Recognition | Dialect support (Varhadi, Konkani-Marathi) |
| Hindi Support | Bilingual seamless switching |
| Natural Voice Responses | Regional accent TTS |
| Web + Mobile Ready | Browser-based with mic access |

### 2. Government Scheme Assistant
| Feature | Description |
|---------|-------------|
| Eligibility Checker | Personalized eligibility assessment |
| Scheme Discovery | "What schemes am I eligible for?" |
| Application Guidance | Step-by-step form help |
| Document Checklist | Required papers list |

### 3. Maharashtra-Specific Integrations
| Integration | Data Provided |
|-------------|---------------|
| MahaDBT Portal | State scheme applications |
| Bhulekh (7/12, 8A) | Land record queries |
| MSAMB Mandi | Live agricultural prices |
| IMD Weather | Crop advisory |

### 4. Scheme Coverage

**Central Schemes:** PM Kisan, Ayushman Bharat, PM Awas, MGNREGA, PM Fasal Bima

**Maharashtra State Schemes:**
- Ladki Bahin Yojana (₹1500/month)
- Mahatma Phule Shetkari Karj Mukti
- Shravan Bal Yojana
- Sanjay Gandhi Niradhar Yojana
- Gharkul Yojana
- Mukhyamantri Solar Pump Yojana

### 5. Current Affairs Integration
- Auto-updated knowledge base (new schemes)
- Budget announcement processing
- Seasonal crop advisories
- Application deadline warnings

---

## Technical Architecture

```
User Voice → Bhashini ASR → Intent Detection (Gemini)
                                    ↓
                           RAG Retrieval (ChromaDB)
                                    ↓
                           Response Generation
                                    ↓
                           Bhashini TTS → Voice Output
```

### Detailed Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│              Streamlit/Gradio Web Application                │
│                    (Voice Recording UI)                      │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   SPEECH PROCESSING                          │
│  ┌─────────────────┐    ┌─────────────────────────────────┐  │
│  │   Bhashini ASR  │ OR │    OpenAI Whisper (Local)       │  │
│  │  (Marathi/Hindi)│    │    (Fallback option)            │  │
│  └─────────────────┘    └─────────────────────────────────┘  │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  LANGUAGE UNDERSTANDING                      │
│  ┌─────────────────┐    ┌─────────────────────────────────┐  │
│  │ Intent Detection│    │   Entity Extraction             │  │
│  │   (Gemini LLM)  │    │   (District, Age, Category)     │  │
│  └─────────────────┘    └─────────────────────────────────┘  │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  KNOWLEDGE RETRIEVAL (RAG)                   │
│  ┌─────────────────┐    ┌─────────────────────────────────┐  │
│  │    ChromaDB     │    │   Government Scheme PDFs        │  │
│  │  Vector Store   │←───│   Eligibility Rules Database    │  │
│  └─────────────────┘    └─────────────────────────────────┘  │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                 RESPONSE GENERATION                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Gemini LLM (Response in Marathi)           │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   SPEECH SYNTHESIS                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Bhashini TTS (Marathi Voice)               │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack (All FREE)

| Component | Technology | Cost |
|-----------|------------|------|
| Frontend | Streamlit/Gradio | FREE |
| Speech-to-Text | Bhashini API | FREE (10K/month) |
| LLM | Gemini API (free tier) | FREE |
| Vector DB | ChromaDB | FREE |
| Text-to-Speech | Bhashini TTS | FREE |
| Deployment | HuggingFace Spaces | FREE |

**Total Project Cost: ₹0**

---

## Data Sources (All Free)

| Source | URL | Data |
|--------|-----|------|
| MyScheme | myscheme.gov.in | Central schemes |
| MahaDBT | mahadbt.maharashtra.gov.in | State schemes |
| GR Portal | gr.maharashtra.gov.in | Government resolutions |
| Bhulekh | bhulekh.mahabhumi.gov.in | Land records |
| MSAMB | msamb.com | Mandi prices |
| IMD Pune | imdpune.gov.in | Weather data |
| PRS India | prsindia.org | Policy analysis |

---

## Unique Differentiators vs Existing Solutions

| Aspect | Jugalbandi/KissanAI | Your Project |
|--------|---------------------|--------------|
| Focus | Generic India | Maharashtra-specific |
| Dialects | Standard only | Varhadi, Konkani support |
| State Integration | Central only | MahaDBT, Bhulekh, MSAMB |
| Source Code | Proprietary | Open-source, documented |
| Schemes Covered | 171 only | Deep Maharashtra coverage |

---

## Sample Conversations

### Example 1: Scheme Discovery (Marathi)
```
User: "मी एक शेतकरी आहे, 2 एकर जमीन आहे, मला कोणत्या योजना मिळू शकतात?"
(I am a farmer with 2 acres, what schemes can I get?)

System: "तुम्ही या 5 योजनांसाठी पात्र आहात:
1. PM Kisan - ₹6000/वर्ष ✅
2. Kisan Credit Card ✅
3. PM Fasal Bima ✅
4. Solar Pump Yojana ✅
5. Magel Tyala Sheti Talab ✅

कोणत्या योजनेबद्दल अधिक माहिती हवी?"
```

### Example 2: Mandi Price Query
```
User: "आज पुण्यात कांदा किती चालला?"
(What's onion price in Pune today?)

System: "पुणे गुलटेकडी मंडी मध्ये आज कांदा ₹1800-2200 प्रति क्विंटल आहे.
कालच्या तुलनेत 5% कमी आहे. नाशिक ला ₹2000 मिळेल."
```

### Example 3: Widow Scheme Query
```
User: "मी विधवा आहे, मला कोणती मदत मिळू शकते?"
(I am a widow, what help can I get?)

System: "तुमच्यासाठी या योजना आहेत:
1. Sanjay Gandhi Niradhar Yojana - ₹1500/महिना
2. Ladki Bahin Yojana - ₹1500/महिना
3. PM Awas Yojana - घरासाठी अनुदान
4. Widow Pension - राज्य निवृत्तीवेतन

अर्ज कसा करायचा ते सांगू?"
```

---

## Skills Demonstrated

| Skill | How This Project Shows It |
|-------|---------------------------|
| LLM Integration | Gemini API for reasoning & generation |
| RAG Pipeline | ChromaDB + document retrieval |
| Speech AI | Complete ASR + TTS pipeline |
| System Design | Multi-component architecture |
| Regional NLP | Low-resource language handling |
| Full Stack | Frontend + Backend + Deployment |
| Domain Expertise | Government schemes knowledge |
| Current Affairs | Auto-updating knowledge base |

---

## Target Companies

### Indian Companies (Perfect Fit)
- Google India
- Microsoft India (Azure AI)
- Amazon India (Alexa)
- Flipkart
- Sarvam AI
- Krutrim (Ola)
- ShareChat

### Global Companies with India Focus
- Meta (WhatsApp)
- Apple (Siri India)
- Cohere
- Anthropic
- Hugging Face

---

## Implementation Timeline

| Week | Milestone |
|------|-----------|
| **1-2** | MVP: Voice interface + 5 major schemes |
| **3** | Add 10+ schemes + MahaDBT integration |
| **4** | Mandi prices + weather + land records |
| **5** | Polish UI + demo video + HuggingFace deployment |

---

## Project Links (To Be Updated)

- **GitHub:** [TBD]
- **Live Demo:** [TBD on HuggingFace Spaces]
- **Demo Video:** [TBD]

---

## Contact

**Developer:** [Your Name]
**LinkedIn:** [Your LinkedIn]
**Email:** [Your Email]
