"""Schemas Pydantic usados pela API."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Uma mensagem individual na conversa."""

    role: str = Field(..., description="Papel da mensagem: 'user' ou 'assistant'")
    content: str = Field(..., description="Conteúdo textual da mensagem")


class ChatRequest(BaseModel):
    """Requisição de chat enviada pelo cliente."""

    message: str = Field(..., min_length=1, description="Mensagem atual do usuário")
    history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Histórico recente da conversa (opcional)",
    )


class ChatResponse(BaseModel):
    """Resposta retornada pelo companheiro."""

    reply: str = Field(..., description="Resposta gerada pelo companheiro")
    character_name: str = Field(..., description="Nome do personagem que respondeu")


class HealthResponse(BaseModel):
    """Resposta do endpoint de saúde."""

    status: str
    app_name: str
    version: str
