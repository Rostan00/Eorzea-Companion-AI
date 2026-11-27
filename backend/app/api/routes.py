"""Rotas principais da API."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict

from app.core.config import settings
from app.character.persona import get_default_persona
from app.llm.factory import get_llm_provider
from .schemas import ChatRequest, ChatResponse, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica se o serviço está no ar."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de conversa com o companheiro.

    Recebe a mensagem do usuário + histórico opcional e retorna a resposta
    gerada com base na persona configurada.
    """
    persona = get_default_persona()
    llm = get_llm_provider()

    # Monta o histórico no formato esperado pelo provedor
    messages: List[Dict[str, str]] = []

    if request.history:
        for msg in request.history:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})

    # Adiciona a mensagem atual
    messages.append({"role": "user", "content": request.message})

    try:
        reply = await llm.generate(
            system_prompt=persona.to_system_prompt(),
            messages=messages,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resposta do LLM: {str(exc)}",
        ) from exc

    return ChatResponse(
        reply=reply,
        character_name=persona.name,
    )
