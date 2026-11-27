"""Testes do sistema de memória."""

from pathlib import Path

import pytest

from app.memory.store import MemoryStore
from app.memory.models import MemoryEntry, MemoryType
from app.memory.extractor import extract_candidate_memories


@pytest.fixture
def store(tmp_path: Path) -> MemoryStore:
    db = tmp_path / "test_memories.db"
    return MemoryStore(db_path=db)


def test_add_and_get(store: MemoryStore):
    entry = MemoryEntry(
        content="O jogador main é Dark Knight",
        memory_type=MemoryType.SEMANTIC,
        importance=0.9,
        tags=["perfil", "job"],
    )
    store.add(entry)
    loaded = store.get(entry.id)
    assert loaded is not None
    assert loaded.content == entry.content
    assert loaded.memory_type == MemoryType.SEMANTIC
    assert loaded.importance == 0.9


def test_search_by_keyword(store: MemoryStore):
    store.add_from_conversation(
        "Gosto de fazer Island Sanctuary no fim de semana",
        importance=0.8,
        tags=["preferencia", "island"],
        memory_type=MemoryType.SEMANTIC,
    )
    store.add_from_conversation(
        "Wipeamos no trial de ontem",
        importance=0.6,
        tags=["evento"],
        memory_type=MemoryType.EPISODIC,
    )

    results = store.search("Island Sanctuary")
    assert len(results) >= 1
    assert "Island" in results[0].content or "island" in results[0].content.lower()


def test_build_context_block(store: MemoryStore):
    store.add_from_conversation(
        "Prefiro tankar em roulette",
        importance=0.85,
        tags=["preferencia"],
        memory_type=MemoryType.SEMANTIC,
    )
    block = store.build_context_block("roulette tank")
    assert "Memórias relevantes" in block
    assert "tankar" in block.lower() or "roulette" in block.lower()


def test_extractor_preference():
    candidates = extract_candidate_memories("Eu gosto de craftar armaduras")
    assert len(candidates) >= 1
    content, importance, tags, mem_type = candidates[0]
    assert importance >= 0.6


def test_extractor_goal():
    candidates = extract_candidate_memories(
        "Quero upar meu Culinarian até o 90 essa semana"
    )
    assert len(candidates) >= 1
    _, _, _, mem_type = candidates[0]
    assert mem_type == MemoryType.GOAL


def test_count(store: MemoryStore):
    assert store.count() == 0
    store.add_from_conversation("Teste de contagem")
    assert store.count() == 1
