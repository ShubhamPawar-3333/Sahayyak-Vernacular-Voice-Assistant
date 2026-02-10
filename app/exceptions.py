"""
Custom exception hierarchy for Sahayyak Voice Assistant.
"""


class SahayyakError(Exception):
    """Base exception for all Sahayyak errors."""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


# --- Speech Exceptions ---


class SpeechError(SahayyakError):
    """Base exception for speech-related errors."""

    pass


class ASRError(SpeechError):
    """Speech-to-text conversion failed."""

    pass


class TTSError(SpeechError):
    """Text-to-speech conversion failed."""

    pass


class SpeechAPIConnectionError(SpeechError):
    """Cannot connect to speech API (Bhashini)."""

    pass


# --- LLM Exceptions ---


class LLMError(SahayyakError):
    """Base exception for LLM-related errors."""

    pass


class LLMRateLimitError(LLMError):
    """API rate limit exceeded."""

    pass


class LLMResponseError(LLMError):
    """Invalid or empty response from LLM."""

    pass


# --- RAG Exceptions ---


class RAGError(SahayyakError):
    """Base exception for RAG pipeline errors."""

    pass


class DocumentIngestionError(RAGError):
    """Failed to ingest document into vector store."""

    pass


class RetrievalError(RAGError):
    """Failed to retrieve relevant documents."""

    pass


# --- Configuration Exceptions ---


class ConfigError(SahayyakError):
    """Configuration or environment variable error."""

    pass


class MissingAPIKeyError(ConfigError):
    """Required API key is missing."""

    pass
