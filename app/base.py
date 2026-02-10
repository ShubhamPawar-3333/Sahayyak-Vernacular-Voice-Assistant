"""
Abstract base classes defining interfaces for Sahayyak modules.
All implementations must conform to these contracts.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


# --- Data Models ---


@dataclass
class TranscriptionResult:
    """Result from speech-to-text conversion."""

    text: str
    language: str
    confidence: float = 0.0


@dataclass
class SynthesisResult:
    """Result from text-to-speech conversion."""

    audio_content: bytes
    format: str = "wav"


@dataclass
class RetrievalResult:
    """Result from RAG document retrieval."""

    content: str
    source: str
    score: float
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class QueryResponse:
    """Final response from the assistant pipeline."""

    text: str
    sources: list[RetrievalResult] = None
    language: str = "mr"
    audio: Optional[bytes] = None

    def __post_init__(self):
        if self.sources is None:
            self.sources = []


# --- Abstract Interfaces ---


class BaseSpeechService(ABC):
    """Interface for speech processing services."""

    @abstractmethod
    def speech_to_text(
        self, audio: bytes, language: str = "mr"
    ) -> TranscriptionResult:
        """
        Convert speech audio to text.

        Args:
            audio: Raw audio bytes.
            language: ISO language code (mr=Marathi, hi=Hindi).

        Returns:
            TranscriptionResult with transcribed text.
        """
        pass

    @abstractmethod
    def text_to_speech(self, text: str, language: str = "mr") -> SynthesisResult:
        """
        Convert text to speech audio.

        Args:
            text: Text to synthesize.
            language: ISO language code.

        Returns:
            SynthesisResult with audio bytes.
        """
        pass


class BaseLLMService(ABC):
    """Interface for LLM services."""

    @abstractmethod
    def generate(self, query: str, context: str = "", language: str = "mr") -> str:
        """
        Generate a response using the LLM.

        Args:
            query: User's question.
            context: Retrieved context from RAG.
            language: Response language.

        Returns:
            Generated text response.
        """
        pass

    @abstractmethod
    def extract_intent(self, query: str) -> dict[str, Any]:
        """
        Extract user intent and entities from query.

        Args:
            query: User's question in any language.

        Returns:
            Dict with 'intent' and 'entities' keys.
        """
        pass


class BaseRAGService(ABC):
    """Interface for RAG pipeline services."""

    @abstractmethod
    def ingest(self, file_path: str) -> int:
        """
        Ingest a document into the vector store.

        Args:
            file_path: Path to the document file.

        Returns:
            Number of chunks ingested.
        """
        pass

    @abstractmethod
    def query(self, question: str, top_k: int = 5) -> list[RetrievalResult]:
        """
        Query the vector store for relevant documents.

        Args:
            question: Search query.
            top_k: Number of results to return.

        Returns:
            List of RetrievalResult objects.
        """
        pass
