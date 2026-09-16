"""Create and persist a local FAISS vector database from PDF files.

Install the dependencies once in the project virtual environment:

    pip install pypdf faiss-cpu langchain-community langchain-huggingface \
        sentence-transformers

The embedding model is downloaded once from Hugging Face and then cached
locally. No OpenAI API, key, or network call is used during embedding after
the model has been downloaded.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


DEFAULT_PDF_DIRECTORY = Path("database")
DEFAULT_VECTOR_DIRECTORY = Path("vector_db")
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_pdf_documents(pdf_directory: Path) -> list[Document]:
    """Extract text from every PDF below *pdf_directory* with page metadata."""
    if not pdf_directory.exists():
        raise FileNotFoundError(f"PDF directory does not exist: {pdf_directory}")

    pdf_files = sorted(pdf_directory.rglob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {pdf_directory}")

    documents: list[Document] = []
    for pdf_path in pdf_files:
        reader = PdfReader(str(pdf_path))
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip().lower()
            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(pdf_path),
                            "file_name": pdf_path.name,
                            "page": page_number,
                        },
                    )
                )

    if not documents:
        raise ValueError("The PDFs were found, but no text could be extracted.")
    return documents


def split_documents(
    documents: Iterable[Document],
    chunk_size: int = 1200,
    chunk_overlap: int = 400,
) -> list[Document]:
    """Split pages into overlapping chunks while preserving their metadata."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        #separators=[". ", " ", ""],
    )
    return splitter.split_documents(list(documents))


def create_embeddings(model_name: str = DEFAULT_EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
    """Create a local Hugging Face embedding model (no OpenAI dependency)."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True},
    )


def build_and_save_vector_db(
    pdf_directory: Path = DEFAULT_PDF_DIRECTORY,
    vector_directory: Path = DEFAULT_VECTOR_DIRECTORY,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> FAISS:
    """Create the FAISS index and persist it to *vector_directory*."""
    documents = load_pdf_documents(pdf_directory)
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    vector_store = FAISS.from_documents(chunks, create_embeddings(model_name))
    vector_store.save_local(str(vector_directory))
    return vector_store


def load_vector_db(
    vector_directory: Path = DEFAULT_VECTOR_DIRECTORY,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> FAISS:
    """Load a previously persisted FAISS index created by this script.

    FAISS stores the document metadata in a pickle file. Only load indexes
    from a directory you created or otherwise fully trust.
    """
    if not (vector_directory / "index.faiss").exists():
        raise FileNotFoundError(
            f"FAISS index not found in {vector_directory}. "
            "Run this script to create it first."
        )
    return FAISS.load_local(
        str(vector_directory),
        create_embeddings(model_name),
        allow_dangerous_deserialization=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local persistent FAISS database from PDF files."
    )
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=DEFAULT_PDF_DIRECTORY,
        help="Directory containing PDFs (default: database).",
    )
    parser.add_argument(
        "--vector-dir",
        type=Path,
        default=DEFAULT_VECTOR_DIRECTORY,
        help="Output directory for the FAISS database (default: vector_db).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Local Hugging Face embedding model name.",
    )
    parser.add_argument("--chunk-size", type=int, default=1000)
    parser.add_argument("--chunk-overlap", type=int, default=200)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vector_store = build_and_save_vector_db(
        pdf_directory=args.pdf_dir,
        vector_directory=args.vector_dir,
        model_name=args.model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    print(
        f"FAISS database created at '{args.vector_dir}' with "
        f"{len(vector_store.index_to_docstore_id)} chunks."
    )


if __name__ == "__main__":
    main()