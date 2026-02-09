# Bhashini API Research Document

## Overview
Bhashini is India's government AI platform for multilingual services (22+ Indian languages including Marathi).

---

## 1. Registration & Authentication

### Step 1: Register
- Go to: https://bhashini.gov.in
- Create account with email
- Verify email to activate

### Step 2: Generate API Key
- Login → "My Profile" section
- Click "Generate" button
- App name: use lowercase with underscores (e.g., `sahayyak_voice_assistant`)
- Limit: 5 API keys per account

### Step 3: Get Credentials
You'll receive 3 values:
| Credential | Purpose |
|------------|---------|
| `userid` | User identifier |
| `UlcaApiKey` | ULCA platform authentication |
| `InferenceApiKey` | Inference service authentication |

---

## 2. API Architecture

### 3-Step API Flow
```
1. Pipeline Search (Optional)
   → Find available models for task (ASR/TTS/Translation)
   → Returns: pipelineId

2. Pipeline Config (Required)
   → Configure specific pipeline
   → Returns: serviceId, callbackUrl

3. Pipeline Compute (Required)  
   → Send input (audio/text)
   → Returns: output (text/audio)
```

### Endpoints
| Endpoint | Purpose |
|----------|---------|
| `/ulca/v1/search` | Search available pipelines |
| `/ulca/v1/getConfig` | Get pipeline configuration |
| `{callbackUrl}/compute` | Execute ASR/TTS/Translation |

---

## 3. Supported Languages

Marathi service IDs are available for:
- **ASR (Speech-to-Text)**: ✅ Supported
- **TTS (Text-to-Speech)**: ✅ Supported
- **Translation (Marathi ↔ Hindi/English)**: ✅ Supported

Model providers include: AI4Bharat, IIT Madras, CDAC

---

## 4. Python Implementation

### Dependencies
```
pip install requests
```

### Sample Code Structure
```python
import requests
import base64

# Authentication
AUTH_HEADERS = {
    "userID": "your_user_id",
    "ulcaApiKey": "your_ulca_key",
    "Authorization": "your_inference_key"
}

# Step 1: Get Pipeline Config
def get_pipeline_config(source_lang, target_lang, task):
    payload = {
        "pipelineTasks": [{"taskType": task, "config": {...}}],
        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }
    response = requests.post(
        "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline",
        json=payload,
        headers=AUTH_HEADERS
    )
    return response.json()

# Step 2: ASR (Speech-to-Text)
def speech_to_text(audio_base64, source_lang="mr"):
    config = get_pipeline_config(source_lang, "en", "asr")
    callback_url = config["pipelineInferenceAPIEndPoint"]["callbackUrl"]
    
    payload = {
        "pipelineTasks": [{
            "taskType": "asr",
            "config": {"language": {"sourceLanguage": source_lang}}
        }],
        "inputData": {"audio": [{"audioContent": audio_base64}]}
    }
    response = requests.post(callback_url, json=payload, headers=AUTH_HEADERS)
    return response.json()["pipelineResponse"][0]["output"][0]["source"]

# Step 3: TTS (Text-to-Speech)
def text_to_speech(text, target_lang="mr"):
    config = get_pipeline_config("en", target_lang, "tts")
    callback_url = config["pipelineInferenceAPIEndPoint"]["callbackUrl"]
    
    payload = {
        "pipelineTasks": [{
            "taskType": "tts",
            "config": {"language": {"sourceLanguage": target_lang}}
        }],
        "inputData": {"input": [{"source": text}]}
    }
    response = requests.post(callback_url, json=payload, headers=AUTH_HEADERS)
    return response.json()["pipelineResponse"][0]["audio"][0]["audioContent"]
```

---

## 5. Pricing & Limits

| Tier | Cost | Limits |
|------|------|--------|
| **PoC/Development** | FREE | Unspecified (for testing only) |
| **TTS Subscription** | ₹250/month | 50,000 chars/day |
| **Enterprise** | Contact sales | Custom limits |

**For portfolio project:** FREE tier is sufficient for development and demos.

---

## 6. Alternative: OpenAI Whisper (Backup)

If Bhashini has issues, use local Whisper:
```python
pip install openai-whisper

import whisper
model = whisper.load_model("base")
result = model.transcribe("audio.mp3", language="mr")
print(result["text"])
```

---

## 7. Key Takeaways for Sahayyak

| Decision | Choice |
|----------|--------|
| Primary ASR/TTS | Bhashini API |
| Backup ASR | Whisper (local) |
| Marathi support | ✅ Full support |
| Cost | FREE for PoC |
| Registration | Required (Meity email may take 1-2 days) |

---

## 8. Next Steps

1. [ ] Register on bhashini.gov.in
2. [ ] Generate API keys
3. [ ] Test ASR with Marathi audio sample
4. [ ] Test TTS with Marathi text
5. [ ] Document service IDs for Marathi
