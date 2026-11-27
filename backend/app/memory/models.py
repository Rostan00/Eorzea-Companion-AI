"""Modelos de dados da memória."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import uuid


class MemoryType(str, Enum):
    """Tipos de memória suportados."""

    EPISODIC = "episodic"  # Eventos / momentos vividos
    SEMANTIC = "semantic"  # Fatos e preferências
    GOAL = "goal"  # Objetivos do jogador ou da Lauda


@dataclass
class MemoryEntry:
    """Uma entrada individual de memória."""

    content: str
    memory_type: MemoryType = MemoryType.EPISODIC
    importance: float = 0.5  # 0.0 a 1.0
    tags: list = field(default_factory=list)
    source: str = "conversation"  # conversation | system | manual
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed_at: Optional[datetime] = None
    access_count: int = 0

    def mark_accessed(self) -> None:
        """Atualiza contadores de acesso."""
        self.last_accessed_at = datetime.now(timezone.utc)
        self.access_count += 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "importance": self.importance,
            "tags": self.tags,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "last_accessed_at": self.last_accessed_at.isoformat()
            if self.last_accessed_at
            else None,
            "access_count": self.access_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryEntry":
        created = data.get("created_at")
        if isinstance(created, str):
            created = datetime.fromisoformat(created)
        else:
            created = datetime.now(timezone.utc)

        last_accessed = data.get("last_accessed_at")
        if isinstance(last_accessed, str):
            last_accessed = datetime.fromisoformat(last_accessed)

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            content=data["content"],
            memory_type=MemoryType(data.get("memory_type", "episodic")),
            importance=float(data.get("importance", 0.5)),
            tags=list(data.get("tags") or []),
            source=data.get("source", "conversation"),
            created_at=created,
            last_accessed_at=last_accessed,
            access_count=int(data.get("access_count", 0)),
        )
