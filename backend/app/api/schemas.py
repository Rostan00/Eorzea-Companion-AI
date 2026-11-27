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
    memories_used: int = Field(
        default=0,
        description="Quantidade de memórias injetadas no contexto",
    )


class HealthResponse(BaseModel):
    """Resposta do endpoint de saúde."""

    status: str
    app_name: str
    version: str
    memory_count: int = 0


class MemoryCreateRequest(BaseModel):
    """Criação manual de uma memória."""

    content: str = Field(..., min_length=3)
    importance: float = Field(default=0.7, ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    memory_type: str = Field(
        default="episodic",
        description="episodic | semantic | goal",
    )


class MemoryItem(BaseModel):
    id: str
    content: str
    memory_type: str
    importance: float
    tags: List[str]
    created_at: str
    access_count: int


class MemoryListResponse(BaseModel):
    total: int
    items: List[MemoryItem]
