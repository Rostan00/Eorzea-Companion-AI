"""Rotas principais da API."""

from functools import lru_cache
from typing import List, Dict

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.character.persona import get_default_persona
from app.llm.factory import get_llm_provider
from app.memory.store import MemoryStore
from app.memory.extractor import extract_candidate_memories
from app.memory.models import MemoryType
from .schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    MemoryCreateRequest,
    MemoryItem,
    MemoryListResponse,
)

router = APIRouter()


@lru_cache(maxsize=1)
def get_memory_store() -> MemoryStore:
    """Instância única do store de memória para o processo."""
    return MemoryStore(db_path=settings.memory_db_path)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica se o serviço está no ar."""
    store = get_memory_store()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
        memory_count=store.count(),
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de conversa com o companheiro.

    - Recupera memórias relevantes
    - Gera resposta com a persona
    - Extrai e grava novas memórias quando fizer sentido
    """
    persona = get_default_persona()
    llm = get_llm_provider()
    store = get_memory_store()

    memory_block = store.build_context_block(
        query=request.message,
        limit=settings.memory_retrieval_limit,
    )
    memories_used = memory_block.count("\n- ") if memory_block else 0

    system_prompt = persona.to_system_prompt()
    if memory_block:
        system_prompt = f"{system_prompt}\n\n{memory_block}"

    messages: List[Dict[str, str]] = []
    if request.history:
        for msg in request.history:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": request.message})

    try:
        reply = await llm.generate(
            system_prompt=system_prompt,
            messages=messages,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resposta do LLM: {str(exc)}",
        ) from exc

    if settings.memory_auto_extract:
        candidates = extract_candidate_memories(
            user_message=request.message,
            assistant_reply=reply,
        )
        for content, importance, tags, mem_type in candidates:
            store.add_from_conversation(
                content=content,
                importance=importance,
                tags=tags,
                memory_type=mem_type,
            )

    return ChatResponse(
        reply=reply,
        character_name=persona.name,
        memories_used=memories_used,
    )


@router.get("/memories", response_model=MemoryListResponse)
async def list_memories(limit: int = 20):
    """Lista as memórias mais recentes."""
    store = get_memory_store()
    items = store.list_recent(limit=min(limit, 100))
    return MemoryListResponse(
        total=store.count(),
        items=[
            MemoryItem(
                id=m.id,
                content=m.content,
                memory_type=m.memory_type.value,
                importance=m.importance,
                tags=m.tags,
                created_at=m.created_at.isoformat(),
                access_count=m.access_count,
            )
            for m in items
        ],
    )


@router.post("/memories", response_model=MemoryItem)
async def create_memory(body: MemoryCreateRequest):
    """Cria uma memória manualmente."""
    store = get_memory_store()
    try:
        mem_type = MemoryType(body.memory_type)
    except ValueError:
        mem_type = MemoryType.EPISODIC

    entry = store.add_from_conversation(
        content=body.content,
        importance=body.importance,
        tags=body.tags,
        memory_type=mem_type,
    )
    return MemoryItem(
        id=entry.id,
        content=entry.content,
        memory_type=entry.memory_type.value,
        importance=entry.importance,
        tags=entry.tags,
        created_at=entry.created_at.isoformat(),
        access_count=entry.access_count,
    )
