"""Armazenamento persistente de memórias (SQLite)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone

from .models import MemoryEntry, MemoryType


class MemoryStore:
    """
    Armazena e recupera memórias de forma persistente usando SQLite.

    Foco inicial:
    - Memórias episódicas (eventos / momentos)
    - Fatos semânticos (preferências, nomes, metas)
    - Recuperação por relevância simples (palavras-chave + importância)
    """

    def __init__(self, db_path: str | Path = "data/memories.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    importance REAL NOT NULL DEFAULT 0.5,
                    tags TEXT NOT NULL DEFAULT '[]',
                    source TEXT NOT NULL DEFAULT 'conversation',
                    created_at TEXT NOT NULL,
                    last_accessed_at TEXT,
                    access_count INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC)"
            )
            conn.commit()

    def add(self, entry: MemoryEntry) -> MemoryEntry:
        """Adiciona uma nova memória."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO memories (
                    id, content, memory_type, importance, tags,
                    source, created_at, last_accessed_at, access_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.id,
                    entry.content,
                    entry.memory_type.value,
                    entry.importance,
                    json.dumps(entry.tags, ensure_ascii=False),
                    entry.source,
                    entry.created_at.isoformat(),
                    entry.last_accessed_at.isoformat()
                    if entry.last_accessed_at
                    else None,
                    entry.access_count,
                ),
            )
            conn.commit()
        return entry

    def get(self, memory_id: str) -> Optional[MemoryEntry]:
        """Busca uma memória pelo ID."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
        if not row:
            return None
        return self._row_to_entry(row)

    def list_recent(self, limit: int = 20) -> List[MemoryEntry]:
        """Retorna as memórias mais recentes."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._row_to_entry(r) for r in rows]

    def search(
        self,
        query: str,
        limit: int = 5,
        min_importance: float = 0.0,
    ) -> List[MemoryEntry]:
        """Busca simples por palavras-chave + ranking por importância."""
        tokens = [t.lower() for t in query.split() if len(t) > 2]
        if not tokens:
            return self.list_recent(limit=limit)

        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM memories WHERE importance >= ?",
                (min_importance,),
            ).fetchall()

        scored: list = []
        for row in rows:
            entry = self._row_to_entry(row)
            content_lower = entry.content.lower()
            tag_text = " ".join(entry.tags).lower()

            hit_count = sum(
                1 for t in tokens if t in content_lower or t in tag_text
            )
            if hit_count == 0:
                continue

            score = (
                (hit_count / len(tokens)) * 0.6
                + entry.importance * 0.3
                + min(entry.access_count / 10.0, 0.1)
            )
            scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, entry in scored[:limit]:
            entry.mark_accessed()
            self._update_access(entry)
            results.append(entry)
        return results

    def add_from_conversation(
        self,
        content: str,
        importance: float = 0.6,
        tags: Optional[list] = None,
        memory_type: MemoryType = MemoryType.EPISODIC,
    ) -> MemoryEntry:
        """Atalho para gravar algo dito/vivido na conversa."""
        entry = MemoryEntry(
            content=content.strip(),
            memory_type=memory_type,
            importance=max(0.0, min(1.0, importance)),
            tags=tags or [],
            source="conversation",
        )
        return self.add(entry)

    def build_context_block(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """Monta bloco de texto com memórias relevantes para o LLM."""
        memories = self.search(query, limit=limit)
        if not memories:
            recent = self.list_recent(limit=10)
            memories = [m for m in recent if m.importance >= 0.6][:limit]

        if not memories:
            return ""

        lines = ["Memórias relevantes da Lauda:"]
        for m in memories:
            tipo = m.memory_type.value
            lines.append(f"- [{tipo}] {m.content}")
        return "\n".join(lines)

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM memories").fetchone()
        return int(row["c"]) if row else 0

    def _update_access(self, entry: MemoryEntry) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE memories
                SET last_accessed_at = ?, access_count = ?
                WHERE id = ?
                """,
                (
                    entry.last_accessed_at.isoformat()
                    if entry.last_accessed_at
                    else None,
                    entry.access_count,
                    entry.id,
                ),
            )
            conn.commit()

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> MemoryEntry:
        data = dict(row)
        data["tags"] = json.loads(data.get("tags") or "[]")
        return MemoryEntry.from_dict(data)
