# Requirements Document: Sahayyak (सहाय्यक)
## Vernacular Voice Assistant for Maharashtra Government Services

**Version:** 1.0  
**Date:** February 2026  
**Author:** [Your Name]

---

## 1. Project Overview

### 1.1 Vision
Empower Maharashtra citizens to access government schemes and services through a voice-first AI assistant in Marathi and Hindi.

### 1.2 Goals
- Enable voice-based scheme discovery and eligibility checking
- Support Marathi dialects (Varhadi, Konkani-Marathi, Deshi)
- Integrate Maharashtra-specific data sources (MahaDBT, Bhulekh, MSAMB)
- Provide application guidance and document checklists

### 1.3 Success Metrics
| Metric | Target |
|--------|--------|
| Voice recognition accuracy (Marathi) | >85% |
| Correct eligibility determination | >90% |
| User query resolution rate | >80% |
| Response time | <5 seconds |

---

## 2. Stakeholders

| Stakeholder | Role | Needs |
|-------------|------|-------|
| Rural Farmers | Primary User | Scheme info, mandi prices, crop advisory |
| Senior Citizens | Primary User | Pension schemes, simple voice interface |
| Women/Widows | Primary User | Women-specific schemes, application help |
| Students | Primary User | Scholarship information |
| Developer (You) | Builder | Portfolio project, skill demonstration |
| Interviewer | Evaluator | Technical depth, problem-solving evidence |

---

## 3. Functional Requirements

### 3.1 Voice Interface
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-V01 | System shall accept Marathi voice input | P0 |
| FR-V02 | System shall accept Hindi voice input | P0 |
| FR-V03 | System shall respond with Marathi voice output | P0 |
| FR-V04 | System shall auto-detect language (Marathi/Hindi) | P1 |
| FR-V05 | System shall support Varhadi dialect | P2 |
| FR-V06 | System shall support Konkani-Marathi dialect | P2 |

### 3.2 Scheme Discovery
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-S01 | System shall list schemes based on user profile | P0 |
| FR-S02 | System shall check eligibility for specific schemes | P0 |
| FR-S03 | System shall explain scheme benefits in simple Marathi | P0 |
| FR-S04 | System shall provide application steps | P1 |
| FR-S05 | System shall list required documents | P1 |
| FR-S06 | System shall track scheme deadlines | P2 |

### 3.3 Maharashtra Integrations
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-M01 | System shall fetch live mandi prices from MSAMB | P1 |
| FR-M02 | System shall provide weather-based crop advisory | P2 |
| FR-M03 | System shall explain 7/12 land record process | P2 |
| FR-M04 | System shall guide MahaDBT application | P2 |

### 3.4 Knowledge Management
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-K01 | System shall use RAG for accurate responses | P0 |
| FR-K02 | System shall cover 15+ central schemes | P0 |
| FR-K03 | System shall cover 10+ Maharashtra state schemes | P0 |
| FR-K04 | System shall update knowledge base monthly | P2 |

---

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Response latency | <5 seconds |
| NFR-02 | Availability | 99% uptime (HuggingFace Spaces) |
| NFR-03 | Concurrent users | 10 (free tier limitation) |
| NFR-04 | Voice quality | Natural, clear Marathi accent |
| NFR-05 | Data privacy | No user data stored locally |
| NFR-06 | Cost | ₹0 (free tier APIs only) |

---

## 5. User Stories

### Epic 1: Voice Interaction

#### US-1.1: Basic Voice Query
**As a** rural farmer  
**I want to** ask questions in Marathi using my voice  
**So that** I don't need to type or read English  

**Acceptance Criteria:**
- [ ] User can record voice in browser
- [ ] System transcribes Marathi speech to text
- [ ] System responds with Marathi voice output
- [ ] Works on mobile browsers

#### US-1.2: Hindi Support
**As a** Hindi-speaking migrant worker  
**I want to** ask questions in Hindi  
**So that** I can access schemes in my comfortable language  

**Acceptance Criteria:**
- [ ] System detects Hindi input
- [ ] Responds in Hindi voice
- [ ] All scheme info available in Hindi

#### US-1.3: Dialect Understanding
**As a** farmer from Vidarbha  
**I want to** speak in Varhadi dialect  
**So that** I don't have to switch to standard Marathi  

**Acceptance Criteria:**
- [ ] System understands Varhadi vocabulary
- [ ] Responds in standard Marathi (understood by all)

---

### Epic 2: Scheme Discovery

#### US-2.1: Find Eligible Schemes
**As a** small farmer with 2 acres  
**I want to** know all schemes I'm eligible for  
**So that** I don't miss any government benefits  

**Acceptance Criteria:**
- [ ] System asks relevant questions (occupation, land, income)
- [ ] Returns list of eligible schemes
- [ ] Shows eligibility status for each (✅/❌)
- [ ] Prioritizes most beneficial schemes

**Example Conversation:**
```
User: "मी एक शेतकरी आहे, 2 एकर जमीन आहे"
System: "तुम्ही या 5 योजनांसाठी पात्र आहात:
1. PM Kisan - ₹6000/वर्ष ✅
2. PM Fasal Bima ✅
3. Solar Pump Yojana ✅
..."
```

#### US-2.2: Scheme Details
**As a** citizen  
**I want to** know details about a specific scheme  
**So that** I understand the benefits and process  

**Acceptance Criteria:**
- [ ] Explains benefit amount
- [ ] Lists eligibility criteria
- [ ] Explains application process
- [ ] Lists required documents

#### US-2.3: Women-Specific Schemes
**As a** widow from rural Maharashtra  
**I want to** find schemes specifically for women like me  
**So that** I can get financial support  

**Acceptance Criteria:**
- [ ] System understands "widow" context
- [ ] Returns women-specific schemes
- [ ] Includes Ladki Bahin, Sanjay Gandhi Niradhar

---

### Epic 3: Agricultural Services

#### US-3.1: Mandi Prices
**As a** farmer  
**I want to** know today's crop prices in nearby mandis  
**So that** I can decide where and when to sell  

**Acceptance Criteria:**
- [ ] System fetches live prices from MSAMB
- [ ] Shows prices for user's district
- [ ] Compares with yesterday's prices
- [ ] Suggests best mandi for selling

**Example:**
```
User: "आज पुण्यात कांदा किती चालला?"
System: "गुलटेकडी मंडी: ₹1800-2200/क्विंटल
कालच्या तुलनेत 5% कमी. नाशिक ला ₹2000 मिळेल."
```

#### US-3.2: Weather Advisory
**As a** farmer growing soybeans  
**I want to** know if I should harvest today  
**So that** I don't lose crops to unexpected rain  

**Acceptance Criteria:**
- [ ] Fetches weather forecast for user's district
- [ ] Provides crop-specific advice
- [ ] Warns about adverse conditions

---

### Epic 4: Application Assistance

#### US-4.1: Document Checklist
**As a** first-time applicant  
**I want to** know what documents I need  
**So that** I can prepare before visiting the office  

**Acceptance Criteria:**
- [ ] Lists all required documents
- [ ] Explains where to get each document
- [ ] Suggests alternatives if document unavailable

#### US-4.2: Step-by-Step Guidance
**As a** senior citizen  
**I want to** know how to apply for pension  
**So that** I can complete the process correctly  

**Acceptance Criteria:**
- [ ] Provides numbered steps
- [ ] Explains each step simply
- [ ] Mentions office locations/timings

---

## 6. Scheme Coverage (MVP)

### Central Government Schemes
| Scheme | Target Users |
|--------|--------------|
| PM Kisan Samman Nidhi | Farmers |
| Ayushman Bharat (PM-JAY) | All (health) |
| PM Awas Yojana | Housing |
| MGNREGA | Rural employment |
| PM Fasal Bima Yojana | Farmers |

### Maharashtra State Schemes
| Scheme | Target Users |
|--------|--------------|
| Ladki Bahin Yojana | Women |
| Shravan Bal Yojana | Senior citizens |
| Sanjay Gandhi Niradhar | Destitute |
| Mahatma Phule Karj Mukti | Farmers (loans) |
| Gharkul Yojana | Rural housing |
| Mukhyamantri Solar Pump | Farmers |
| Magel Tyala Sheti Talab | Farmers (irrigation) |

---

## 7. Technical Constraints

| Constraint | Impact |
|------------|--------|
| Bhashini API rate limit (10K/month) | Limited demo usage |
| Gemini free tier (15 RPM) | Response throttling |
| HuggingFace Spaces (2 vCPU) | Limited concurrent users |
| No persistent storage | No user history across sessions |

---

## 8. Out of Scope (v1.0)

- ❌ Actual form submission to government portals
- ❌ Aadhaar verification/authentication
- ❌ Payment processing
- ❌ Offline mode
- ❌ WhatsApp integration
- ❌ SMS notifications

---

## 9. Dependency Matrix

| Component | Depends On | Risk |
|-----------|------------|------|
| Voice Input | Bhashini ASR API | Medium (API availability) |
| Voice Output | Bhashini TTS API | Medium |
| LLM Response | Gemini API | Low (reliable) |
| Mandi Prices | MSAMB website | High (scraping may break) |
| Weather | IMD API | Medium |

---

## 10. Milestones

| Phase | Deliverables | Duration |
|-------|--------------|----------|
| **Phase 1: MVP** | Voice interface + 5 schemes | 2 weeks |
| **Phase 2: Schemes** | 15+ schemes with eligibility | 1 week |
| **Phase 3: Integration** | Mandi + Weather + Land records | 1 week |
| **Phase 4: Polish** | UI + Demo video + Deployment | 1 week |

---

## Appendix A: Sample Intents

| Intent | Example Queries (Marathi) |
|--------|---------------------------|
| `scheme.discover` | "माझ्यासाठी कोणत्या योजना आहेत?" |
| `scheme.eligibility` | "PM Kisan साठी मी पात्र आहे का?" |
| `scheme.details` | "लाडकी बहीण योजना म्हणजे काय?" |
| `scheme.apply` | "अर्ज कसा करायचा?" |
| `scheme.documents` | "कोणती कागदपत्रे लागतात?" |
| `mandi.price` | "कांद्याचा भाव काय आहे?" |
| `weather.forecast` | "उद्या पाऊस पडेल का?" |
| `land.records` | "7/12 कसा काढायचा?" |

---

## Appendix B: Entity Types

| Entity | Examples |
|--------|----------|
| `location` | पुणे, नाशिक, विदर्भ, मुंबई |
| `crop` | कांदा, सोयाबीन, गहू, ऊस |
| `scheme_name` | PM Kisan, Ladki Bahin |
| `occupation` | शेतकरी, मजूर, व्यापारी |
| `category` | विधवा, ज्येष्ठ नागरिक, अल्पभूधारक |
| `land_size` | 2 एकर, 5 हेक्टर |
