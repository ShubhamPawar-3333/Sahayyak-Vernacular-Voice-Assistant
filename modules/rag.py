"""
RAG (Retrieval-Augmented Generation) pipeline for Sahayyak.
Handles document ingestion, embedding, storage, and retrieval.
"""

import os
from pathlib import Path
from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.base import BaseRAGService, RetrievalResult
from app.config import get_config
from app.exceptions import DocumentIngestionError, RetrievalError
from app.logging_config import get_logger

logger = get_logger("rag")

# Multilingual embedding model (free, supports 50+ languages incl. Marathi)
DEFAULT_EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


class RAGService(BaseRAGService):
    """
    RAG pipeline for government scheme knowledge base.

    Features:
    - Multilingual embeddings (Marathi/Hindi/English)
    - ChromaDB for persistent vector storage
    - Chunking with metadata preservation
    - Source citation in results
    """

    def __init__(
        self,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        collection_name: str = "sahayyak_schemes",
    ):
        config = get_config()
        self._collection_name = collection_name
        self._persist_dir = str(config.app.vectordb_dir)
        self._data_dir = str(config.app.data_dir / "schemes")

        # Initialize embeddings
        logger.info(f"Loading embedding model: {embedding_model}")
        self._embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        # Initialize text splitter
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", "।", ".", " ", ""],  # Hindi/Marathi sentence end
        )

        # Initialize vector store
        self._vectorstore = Chroma(
            collection_name=self._collection_name,
            embedding_function=self._embeddings,
            persist_directory=self._persist_dir,
        )

        logger.info(
            f"RAG initialized: {self._vectorstore._collection.count()} "
            f"documents in store"
        )

    def ingest(self, file_path: str) -> int:
        """
        Ingest a single document into the vector store.

        Args:
            file_path: Path to the document (Markdown or text).

        Returns:
            Number of chunks ingested.

        Raises:
            DocumentIngestionError: If ingestion fails.
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise DocumentIngestionError(f"File not found: {file_path}")

            logger.info(f"Ingesting: {path.name}")

            # Load document
            if path.suffix == ".md":
                loader = UnstructuredMarkdownLoader(str(path))
            else:
                loader = TextLoader(str(path), encoding="utf-8")

            documents = loader.load()

            # Add metadata
            for doc in documents:
                doc.metadata.update(
                    {
                        "source_file": path.name,
                        "source_path": str(path),
                        "category": self._detect_category(path.name),
                    }
                )

            # Split into chunks
            chunks = self._splitter.split_documents(documents)

            if not chunks:
                logger.warning(f"No chunks generated from {path.name}")
                return 0

            # Add to vector store
            self._vectorstore.add_documents(chunks)

            logger.info(
                f"Ingested {len(chunks)} chunks from {path.name}"
            )
            return len(chunks)

        except DocumentIngestionError:
            raise
        except Exception as e:
            logger.error(f"Ingestion failed for {file_path}: {e}")
            raise DocumentIngestionError(
                f"Failed to ingest {file_path}: {str(e)}"
            )

    def ingest_directory(self, directory: Optional[str] = None) -> int:
        """
        Ingest all documents from a directory.

        Args:
            directory: Path to directory. Defaults to data/schemes/.

        Returns:
            Total number of chunks ingested.
        """
        dir_path = directory or self._data_dir
        total_chunks = 0

        if not os.path.exists(dir_path):
            logger.warning(f"Directory not found: {dir_path}")
            return 0

        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if file_name.endswith((".md", ".txt")) and os.path.isfile(file_path):
                try:
                    chunks = self.ingest(file_path)
                    total_chunks += chunks
                except DocumentIngestionError as e:
                    logger.error(f"Skipping {file_name}: {e}")

        logger.info(f"Total ingested: {total_chunks} chunks from {dir_path}")
        return total_chunks

    def query(self, question: str, top_k: int = 5) -> list[RetrievalResult]:
        """
        Query the vector store for relevant documents.

        Args:
            question: Search query (supports Marathi/Hindi/English).
            top_k: Number of results to return.

        Returns:
            List of RetrievalResult with content, source, and score.

        Raises:
            RetrievalError: If retrieval fails.
        """
        try:
            results = self._vectorstore.similarity_search_with_relevance_scores(
                question, k=top_k
            )

            if not results:
                logger.info(f"No results found for: '{question[:50]}...'")
                return []

            retrieval_results = [
                RetrievalResult(
                    content=doc.page_content,
                    source=doc.metadata.get("source_file", "unknown"),
                    score=score,
                    metadata=doc.metadata,
                )
                for doc, score in results
            ]

            logger.info(
                f"Retrieved {len(retrieval_results)} results for: "
                f"'{question[:50]}...'"
            )
            return retrieval_results

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            raise RetrievalError(f"Failed to query vector store: {str(e)}")

    def get_context(self, question: str, top_k: int = 5) -> str:
        """
        Get formatted context string for LLM consumption.

        Args:
            question: User's query.
            top_k: Number of chunks to include.

        Returns:
            Formatted context string with sources.
        """
        results = self.query(question, top_k)

        if not results:
            return ""

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {result.source}]\n{result.content}"
            )

        return "\n\n---\n\n".join(context_parts)

    @property
    def document_count(self) -> int:
        """Number of documents in the vector store."""
        return self._vectorstore._collection.count()

    def clear(self):
        """Clear all documents from the vector store."""
        self._vectorstore.delete_collection()
        self._vectorstore = Chroma(
            collection_name=self._collection_name,
            embedding_function=self._embeddings,
            persist_directory=self._persist_dir,
        )
        logger.info("Vector store cleared")

    @staticmethod
    def _detect_category(filename: str) -> str:
        """Detect scheme category from filename."""
        name = filename.lower()
        if "kisan" in name or "krishi" in name or "agri" in name:
            return "agriculture"
        elif "ayushman" in name or "health" in name or "swasthya" in name:
            return "health"
        elif "awas" in name or "housing" in name:
            return "housing"
        elif "pension" in name or "vridha" in name:
            return "pension"
        elif "education" in name or "shiksha" in name:
            return "education"
        elif "mahila" in name or "women" in name:
            return "women"
        return "general"
