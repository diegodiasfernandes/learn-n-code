"""Interface Streamlit para perguntas sobre os documentos indexados no FAISS."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_community.vectorstores import FAISS

from semantic_search import search_similar_chunks
from vector_db_creation_v2 import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_VECTOR_DIRECTORY,
    load_vector_db,
)


PROJECT_DIRECTORY = Path(__file__).resolve().parent
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"

load_dotenv(PROJECT_DIRECTORY / ".env")


def get_api_key() -> str:
    """Return the Gemini key without exposing it in the interface."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Defina GEMINI_API_KEY no arquivo .env antes de iniciar o aplicativo."
        )
    return api_key


@st.cache_resource(show_spinner="Carregando o índice vetorial...")
def get_vector_store(vector_directory: str) -> FAISS:
    """Load the local FAISS index once per directory."""
    return load_vector_db(Path(vector_directory), DEFAULT_EMBEDDING_MODEL)


def format_context(results: list[dict[str, Any]]) -> str:
    """Build a grounded context block with source metadata for Gemini."""
    context_parts: list[str] = []
    for position, result in enumerate(results, start=1):
        metadata = result["metadata"]
        file_names = metadata.get("file_name", metadata.get("source", "desconhecido"))
        pages = metadata.get("pages", metadata.get("page", "desconhecidas"))
        context_parts.append(
            f"[Trecho {position} | arquivo: {file_names} | páginas: {pages}]\n"
            f"{result['text']}"
        )
    return "\n\n".join(context_parts)


def generate_answer(
    client: genai.Client,
    model_name: str,
    question: str,
    results: list[dict[str, Any]],
) -> str:
    """Ask Gemini to answer only from the chunks retrieved by the RAG step."""
    prompt = f"""Você é um assistente que responde perguntas em português usando RAG.
Responda à pergunta somente com base no contexto abaixo.
Se a resposta não estiver no contexto, diga claramente que não encontrou essa
informação nos documentos. Não invente fatos. Seja claro e conciso.

Contexto recuperado:
{format_context(results)}

Pergunta do usuário:
{question}
"""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=800,
        ),
    )
    answer = response.text
    if not answer:
        raise RuntimeError("O Gemini retornou uma resposta vazia.")
    return answer


def render_sources(results: list[dict[str, Any]]) -> None:
    """Render expandable source chunks below each assistant response."""
    with st.expander("Ver trechos usados como fonte"):
        for position, result in enumerate(results, start=1):
            metadata = result["metadata"]
            file_names = metadata.get("file_name", metadata.get("source", "desconhecido"))
            pages = metadata.get("pages", metadata.get("page", "desconhecidas"))
            st.markdown(
                f"**Trecho {position}** — arquivo: `{file_names}`; "
                f"páginas: `{pages}`; similaridade: `{result['score']:.4f}`"
            )
            st.caption(result["text"])


def main() -> None:
    st.set_page_config(page_title="Chat RAG", page_icon="💬")
    st.title("💬 Chat com seus documentos")
    st.caption("Gemini Flash Lite + busca semântica no índice FAISS local")

    with st.sidebar:
        st.header("Configuração")
        vector_directory = st.text_input(
            "Diretório do índice FAISS",
            value=os.getenv("VECTOR_DIRECTORY", str(DEFAULT_VECTOR_DIRECTORY)),
        )
        number_of_chunks = st.slider("Trechos recuperados (k)", 1, 8, 4)
        model_name = st.text_input(
            "Modelo Gemini",
            value=os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL),
        )
        if st.button("Limpar conversa"):
            st.session_state.messages = []
            st.rerun()

    try:
        vector_store = get_vector_store(vector_directory)
    except (FileNotFoundError, RuntimeError, ValueError, TypeError) as error:
        st.error(f"Não foi possível carregar o índice vetorial: {error}")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("sources"):
                render_sources(message["sources"])

    question = st.chat_input("Faça uma pergunta sobre os documentos...")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            results = search_similar_chunks(question, vector_store, number_of_chunks)
            client = genai.Client(api_key=get_api_key())
            with st.spinner("Consultando os documentos e gerando a resposta..."):
                answer = generate_answer(client, model_name, question, results)
            st.markdown(answer)
            render_sources(results)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": results}
            )
        except (FileNotFoundError, RuntimeError, ValueError, TypeError) as error:
            message = f"Não foi possível responder: {error}"
            st.error(message)
            st.session_state.messages.append(
                {"role": "assistant", "content": message}
            )


if __name__ == "__main__":
    main()
