"""
Bhashini API client for Speech-to-Text (ASR) and Text-to-Speech (TTS).
Supports Marathi and Hindi with dialect awareness.
"""

import base64
import time
from typing import Optional

import requests

from app.base import BaseSpeechService, SynthesisResult, TranscriptionResult
from app.config import BhashiniConfig, get_config
from app.exceptions import ASRError, SpeechAPIConnectionError, TTSError
from app.logging_config import get_logger

logger = get_logger("speech.bhashini")

# Bhashini API endpoints
PIPELINE_CONFIG_URL = (
    "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
)


class BhashiniClient(BaseSpeechService):
    """
    Client for Bhashini speech APIs.

    Supports:
    - ASR (Automatic Speech Recognition) for Marathi/Hindi
    - TTS (Text-to-Speech) for Marathi/Hindi
    """

    def __init__(self, config: Optional[BhashiniConfig] = None):
        self.config = config or get_config().bhashini
        self._pipeline_cache: dict = {}

        if not self.config.is_configured():
            logger.warning(
                "Bhashini API keys not configured. "
                "Speech features will not work."
            )

    # --- Public API ---

    def speech_to_text(
        self, audio: bytes, language: str = "mr"
    ) -> TranscriptionResult:
        """
        Convert speech audio to text using Bhashini ASR.

        Args:
            audio: Raw audio bytes (WAV format preferred).
            language: Source language code ('mr' or 'hi').

        Returns:
            TranscriptionResult with transcribed text.

        Raises:
            ASRError: If transcription fails.
        """
        try:
            logger.info(f"Starting ASR for language: {language}")

            # Get pipeline config for ASR
            callback_url, service_id = self._get_pipeline(
                task_type="asr", source_lang=language
            )

            # Encode audio to base64
            audio_b64 = base64.b64encode(audio).decode("utf-8")

            # Build payload
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {
                            "language": {"sourceLanguage": language},
                            "serviceId": service_id,
                        },
                    }
                ],
                "inputData": {"audio": [{"audioContent": audio_b64}]},
            }

            # Make API call
            response = self._make_request(callback_url, payload)

            # Extract text from response
            text = (
                response.get("pipelineResponse", [{}])[0]
                .get("output", [{}])[0]
                .get("source", "")
            )

            if not text:
                raise ASRError("Empty transcription result from Bhashini")

            logger.info(f"ASR complete: '{text[:50]}...'")

            return TranscriptionResult(
                text=text, language=language, confidence=0.85
            )

        except ASRError:
            raise
        except Exception as e:
            logger.error(f"ASR failed: {e}")
            raise ASRError(
                f"Speech-to-text failed: {str(e)}",
                details={"language": language},
            )

    def text_to_speech(
        self, text: str, language: str = "mr"
    ) -> SynthesisResult:
        """
        Convert text to speech using Bhashini TTS.

        Args:
            text: Text to synthesize.
            language: Target language code ('mr' or 'hi').

        Returns:
            SynthesisResult with audio bytes.

        Raises:
            TTSError: If synthesis fails.
        """
        try:
            logger.info(f"Starting TTS for language: {language}")

            # Get pipeline config for TTS
            callback_url, service_id = self._get_pipeline(
                task_type="tts", source_lang=language
            )

            # Build payload
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "tts",
                        "config": {
                            "language": {"sourceLanguage": language},
                            "serviceId": service_id,
                            "gender": "female",
                        },
                    }
                ],
                "inputData": {"input": [{"source": text}]},
            }

            # Make API call
            response = self._make_request(callback_url, payload)

            # Extract audio from response
            audio_b64 = (
                response.get("pipelineResponse", [{}])[0]
                .get("audio", [{}])[0]
                .get("audioContent", "")
            )

            if not audio_b64:
                raise TTSError("Empty audio result from Bhashini")

            audio_bytes = base64.b64decode(audio_b64)

            logger.info(f"TTS complete: {len(audio_bytes)} bytes")

            return SynthesisResult(audio_content=audio_bytes, format="wav")

        except TTSError:
            raise
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            raise TTSError(
                f"Text-to-speech failed: {str(e)}",
                details={"language": language, "text_length": len(text)},
            )

    # --- Private Methods ---

    def _get_pipeline(
        self, task_type: str, source_lang: str
    ) -> tuple[str, str]:
        """
        Get pipeline callback URL and service ID.
        Caches results to avoid redundant API calls.

        Returns:
            Tuple of (callback_url, service_id).
        """
        cache_key = f"{task_type}_{source_lang}"

        if cache_key in self._pipeline_cache:
            return self._pipeline_cache[cache_key]

        try:
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": task_type,
                        "config": {
                            "language": {"sourceLanguage": source_lang}
                        },
                    }
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.config.pipeline_id
                },
            }

            headers = {
                "Content-Type": "application/json",
                "userID": self.config.user_id,
                "ulcaApiKey": self.config.ulca_api_key,
            }

            response = requests.post(
                PIPELINE_CONFIG_URL,
                json=payload,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            # Extract callback URL and service ID
            callback_url = data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
            service_id = data["pipelineResponseConfig"][0]["config"][0][
                "serviceId"
            ]

            self._pipeline_cache[cache_key] = (callback_url, service_id)
            logger.debug(
                f"Pipeline configured: {task_type}/{source_lang} -> {service_id}"
            )

            return callback_url, service_id

        except requests.RequestException as e:
            raise SpeechAPIConnectionError(
                f"Failed to get Bhashini pipeline config: {str(e)}",
                details={"task": task_type, "language": source_lang},
            )

    def _make_request(
        self, url: str, payload: dict, max_retries: int = 3
    ) -> dict:
        """
        Make API request with retry logic.

        Args:
            url: API endpoint URL.
            payload: Request payload.
            max_retries: Maximum number of retries.

        Returns:
            Response JSON data.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.config.inference_key,
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url, json=payload, headers=headers, timeout=30
                )
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = 2**attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise SpeechAPIConnectionError(
                        f"API request failed after {max_retries} attempts: {str(e)}"
                    )
