"""
Speech service facade.
Routes to Bhashini (primary) or Whisper (fallback) based on availability.
"""

from typing import Optional

from app.base import BaseSpeechService, SynthesisResult, TranscriptionResult
from app.exceptions import ASRError, SpeechError, TTSError
from app.logging_config import get_logger

logger = get_logger("speech.service")


class SpeechService:
    """
    Unified speech service with automatic fallback.

    Primary: Bhashini API (supports Marathi/Hindi)
    Fallback: OpenAI Whisper (local, supports Marathi)
    """

    def __init__(self):
        self._bhashini: Optional[BaseSpeechService] = None
        self._whisper_available = False
        self._init_providers()

    def _init_providers(self):
        """Initialize speech providers based on availability."""
        # Try Bhashini
        try:
            from modules.speech import BhashiniClient

            client = BhashiniClient()
            if client.config.is_configured():
                self._bhashini = client
                logger.info("Bhashini speech provider initialized")
            else:
                logger.warning("Bhashini API keys not set, skipping")
        except Exception as e:
            logger.warning(f"Bhashini init failed: {e}")

        # Check Whisper availability
        try:
            import whisper  # noqa: F401

            self._whisper_available = True
            logger.info("Whisper fallback available")
        except ImportError:
            logger.info("Whisper not installed (optional fallback)")

    def speech_to_text(
        self, audio: bytes, language: str = "mr"
    ) -> TranscriptionResult:
        """
        Convert speech to text. Tries Bhashini first, falls back to Whisper.

        Args:
            audio: Raw audio bytes.
            language: Language code ('mr' or 'hi').

        Returns:
            TranscriptionResult with transcribed text.
        """
        # Try Bhashini first
        if self._bhashini:
            try:
                return self._bhashini.speech_to_text(audio, language)
            except SpeechError as e:
                logger.warning(f"Bhashini ASR failed, trying fallback: {e}")

        # Fallback to Whisper
        if self._whisper_available:
            return self._whisper_transcribe(audio, language)

        raise ASRError(
            "No speech-to-text provider available. "
            "Configure Bhashini API keys or install whisper."
        )

    def text_to_speech(
        self, text: str, language: str = "mr"
    ) -> SynthesisResult:
        """
        Convert text to speech. Uses Bhashini (no Whisper fallback for TTS).

        Args:
            text: Text to synthesize.
            language: Language code.

        Returns:
            SynthesisResult with audio bytes.
        """
        if self._bhashini:
            return self._bhashini.text_to_speech(text, language)

        raise TTSError(
            "No text-to-speech provider available. "
            "Configure Bhashini API keys."
        )

    def _whisper_transcribe(
        self, audio: bytes, language: str
    ) -> TranscriptionResult:
        """Fallback transcription using OpenAI Whisper."""
        import tempfile

        import whisper

        logger.info("Using Whisper fallback for ASR")

        # Whisper needs a file path
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio)
            temp_path = f.name

        try:
            model = whisper.load_model("base")
            result = model.transcribe(temp_path, language=language)

            return TranscriptionResult(
                text=result["text"].strip(),
                language=language,
                confidence=0.75,
            )
        except Exception as e:
            raise ASRError(f"Whisper transcription failed: {str(e)}")
        finally:
            import os

            os.unlink(temp_path)

    @property
    def available_providers(self) -> list[str]:
        """List of available speech providers."""
        providers = []
        if self._bhashini:
            providers.append("bhashini")
        if self._whisper_available:
            providers.append("whisper")
        return providers
