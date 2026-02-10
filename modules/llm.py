"""
LLM integration module.
Supports Sarvam-M (primary) and Gemini (fallback) via LangChain.
"""

from typing import Any, Optional

from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.base import BaseLLMService
from app.config import GeminiConfig, get_config
from app.exceptions import LLMError, LLMResponseError, MissingAPIKeyError
from app.logging_config import get_logger
from modules.prompts import SYSTEM_PROMPT, INTENT_EXTRACTION_PROMPT

logger = get_logger("llm")


class LLMService(BaseLLMService):
    """
    LLM service with Sarvam-M (primary) and Gemini (fallback).

    Uses LangChain for unified interface, prompt management,
    and conversation memory.
    """

    def __init__(self):
        self._llm = None
        self._provider = None
        self._memory = ConversationBufferWindowMemory(
            k=10, return_messages=True, memory_key="chat_history"
        )
        self._init_llm()

    def _init_llm(self):
        """Initialize LLM provider: Sarvam-M first, then Gemini."""
        config = get_config()

        # Try Sarvam-M first (free per token)
        if self._try_sarvam(config):
            return

        # Fallback to Gemini
        if self._try_gemini(config.gemini):
            return

        logger.error("No LLM provider available")

    def _try_sarvam(self, config) -> bool:
        """Try to initialize Sarvam-M via OpenAI-compatible endpoint."""
        sarvam_key = config.gemini.api_key  # Reuse config slot or add separate
        try:
            import os

            sarvam_api_key = os.getenv("SARVAM_API_KEY", "")
            if not sarvam_api_key:
                logger.info("Sarvam API key not set, skipping")
                return False

            from langchain_openai import ChatOpenAI

            self._llm = ChatOpenAI(
                model="sarvam-m",
                api_key=sarvam_api_key,
                base_url="https://api.sarvam.ai/v1",
                temperature=0.7,
                max_tokens=1024,
            )
            self._provider = "sarvam-m"
            logger.info("LLM initialized: Sarvam-M (free)")
            return True

        except Exception as e:
            logger.warning(f"Sarvam-M init failed: {e}")
            return False

    def _try_gemini(self, config: GeminiConfig) -> bool:
        """Try to initialize Google Gemini."""
        try:
            if not config.is_configured():
                logger.info("Gemini API key not set, skipping")
                return False

            from langchain_google_genai import ChatGoogleGenerativeAI

            self._llm = ChatGoogleGenerativeAI(
                model=config.model_name,
                google_api_key=config.api_key,
                temperature=config.temperature,
                max_output_tokens=config.max_tokens,
            )
            self._provider = "gemini"
            logger.info(f"LLM initialized: Gemini ({config.model_name})")
            return True

        except Exception as e:
            logger.warning(f"Gemini init failed: {e}")
            return False

    def generate(
        self, query: str, context: str = "", language: str = "mr"
    ) -> str:
        """
        Generate a response using the configured LLM.

        Args:
            query: User's question (can be in Marathi/Hindi/English).
            context: Retrieved context from RAG pipeline.
            language: Response language code.

        Returns:
            Generated text response.
        """
        if not self._llm:
            raise MissingAPIKeyError(
                "No LLM provider configured. Set SARVAM_API_KEY or GOOGLE_API_KEY."
            )

        try:
            # Build prompt with context and memory
            prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=SYSTEM_PROMPT),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessage(
                        content=self._build_user_prompt(query, context, language)
                    ),
                ]
            )

            # Get chat history
            history = self._memory.load_memory_variables({})
            chat_history = history.get("chat_history", [])

            # Generate response
            chain = prompt | self._llm
            response = chain.invoke({"chat_history": chat_history})
            response_text = response.content.strip()

            if not response_text:
                raise LLMResponseError("Empty response from LLM")

            # Save to memory
            self._memory.save_context(
                {"input": query}, {"output": response_text}
            )

            logger.info(
                f"LLM response generated ({self._provider}): "
                f"{len(response_text)} chars"
            )
            return response_text

        except (MissingAPIKeyError, LLMResponseError):
            raise
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise LLMError(f"Failed to generate response: {str(e)}")

    def extract_intent(self, query: str) -> dict[str, Any]:
        """
        Extract user intent and entities from a query.

        Args:
            query: User's question in any language.

        Returns:
            Dict with 'intent' and 'entities' keys.
        """
        if not self._llm:
            raise MissingAPIKeyError("No LLM provider configured.")

        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=INTENT_EXTRACTION_PROMPT),
                    HumanMessage(content=query),
                ]
            )

            chain = prompt | self._llm
            response = chain.invoke({})

            # Parse JSON response
            import json

            try:
                result = json.loads(response.content.strip())
            except json.JSONDecodeError:
                result = {"intent": "general_query", "entities": {}}

            logger.info(f"Intent extracted: {result.get('intent', 'unknown')}")
            return result

        except Exception as e:
            logger.error(f"Intent extraction failed: {e}")
            return {"intent": "general_query", "entities": {}}

    def clear_memory(self):
        """Clear conversation memory for a new session."""
        self._memory.clear()
        logger.info("Conversation memory cleared")

    def _build_user_prompt(
        self, query: str, context: str, language: str
    ) -> str:
        """Build the user prompt with context."""
        lang_map = {"mr": "Marathi", "hi": "Hindi", "en": "English"}
        lang_name = lang_map.get(language, "Marathi")

        if context:
            return (
                f"Context from knowledge base:\n{context}\n\n"
                f"User question: {query}\n\n"
                f"Respond in {lang_name}."
            )
        return f"User question: {query}\n\nRespond in {lang_name}."

    @property
    def provider(self) -> Optional[str]:
        """Current LLM provider name."""
        return self._provider

    @property
    def is_available(self) -> bool:
        """Whether any LLM provider is configured."""
        return self._llm is not None
