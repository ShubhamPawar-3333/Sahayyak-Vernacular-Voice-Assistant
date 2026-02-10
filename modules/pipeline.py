"""
Unified query pipeline for Sahayyak Voice Assistant.
Connects Speech → LLM → RAG into a single end-to-end flow.
"""

from typing import Optional

from app.base import QueryResponse, RetrievalResult, TranscriptionResult
from app.exceptions import SahayyakError
from app.logging_config import get_logger, setup_logging
from modules.llm import LLMService
from modules.rag import RAGService
from modules.speech_service import SpeechService

logger = get_logger("pipeline")


class QueryPipeline:
    """
    End-to-end pipeline: Voice/Text → Understand → Retrieve → Respond → Voice

    Flow:
    1. Speech-to-Text (if audio input)
    2. Intent Extraction
    3. RAG Retrieval (if scheme-related)
    4. LLM Generation
    5. Text-to-Speech (if voice output needed)
    """

    def __init__(self):
        setup_logging()
        logger.info("Initializing Sahayyak pipeline...")

        self._speech = SpeechService()
        self._llm = LLMService()
        self._rag = RAGService()

        logger.info(
            f"Pipeline ready | "
            f"Speech: {self._speech.available_providers} | "
            f"LLM: {self._llm.provider} | "
            f"RAG docs: {self._rag.document_count}"
        )

    def process_voice(
        self, audio: bytes, language: str = "mr", voice_response: bool = True
    ) -> QueryResponse:
        """
        Process a voice query end-to-end.

        Args:
            audio: Raw audio bytes from user.
            language: Language code ('mr', 'hi', 'en').
            voice_response: Whether to include audio in response.

        Returns:
            QueryResponse with text, sources, and optional audio.
        """
        try:
            # Step 1: Speech to Text
            logger.info("Step 1: Converting speech to text...")
            transcription = self._speech.speech_to_text(audio, language)
            logger.info(f"Transcribed: '{transcription.text[:80]}...'")

            # Step 2-4: Process text query
            response = self.process_text(transcription.text, language)

            # Step 5: Text to Speech (if requested)
            if voice_response and response.text:
                try:
                    logger.info("Step 5: Converting response to speech...")
                    synthesis = self._speech.text_to_speech(
                        response.text, language
                    )
                    response.audio = synthesis.audio_content
                except SahayyakError as e:
                    logger.warning(f"TTS failed, returning text only: {e}")

            return response

        except SahayyakError:
            raise
        except Exception as e:
            logger.error(f"Voice pipeline failed: {e}")
            raise SahayyakError(f"Pipeline error: {str(e)}")

    def process_text(
        self, query: str, language: str = "mr"
    ) -> QueryResponse:
        """
        Process a text query through the pipeline.

        Args:
            query: User's text query (any language).
            language: Response language.

        Returns:
            QueryResponse with text and sources.
        """
        try:
            # Step 2: Extract intent
            logger.info("Step 2: Extracting intent...")
            intent_data = self._llm.extract_intent(query)
            intent = intent_data.get("intent", "general_query")
            logger.info(f"Intent: {intent}")

            # Step 3: RAG retrieval (for scheme-related queries)
            context = ""
            sources: list[RetrievalResult] = []

            if self._should_use_rag(intent):
                logger.info("Step 3: Retrieving from knowledge base...")
                sources = self._rag.query(query, top_k=5)
                context = self._rag.get_context(query, top_k=5)
                logger.info(f"Retrieved {len(sources)} relevant documents")
            else:
                logger.info("Step 3: Skipped RAG (not scheme-related)")

            # Step 4: Generate response
            logger.info("Step 4: Generating response...")
            response_text = self._llm.generate(
                query=query, context=context, language=language
            )

            return QueryResponse(
                text=response_text,
                sources=sources,
                language=language,
            )

        except SahayyakError:
            raise
        except Exception as e:
            logger.error(f"Text pipeline failed: {e}")
            raise SahayyakError(f"Pipeline error: {str(e)}")

    def ingest_knowledge_base(self, directory: Optional[str] = None) -> int:
        """
        Ingest scheme documents into the RAG vector store.

        Args:
            directory: Path to scheme docs. Defaults to data/schemes/.

        Returns:
            Number of chunks ingested.
        """
        logger.info("Ingesting knowledge base...")
        count = self._rag.ingest_directory(directory)
        logger.info(f"Knowledge base updated: {count} chunks ingested")
        return count

    def clear_session(self):
        """Clear conversation memory for a new user session."""
        self._llm.clear_memory()
        logger.info("Session cleared")

    @staticmethod
    def _should_use_rag(intent: str) -> bool:
        """Determine if the query needs RAG retrieval."""
        rag_intents = {
            "scheme_inquiry",
            "eligibility_check",
            "application_help",
        }
        return intent in rag_intents

    @property
    def status(self) -> dict:
        """Pipeline health status."""
        return {
            "speech_providers": self._speech.available_providers,
            "llm_provider": self._llm.provider,
            "llm_available": self._llm.is_available,
            "rag_documents": self._rag.document_count,
        }
