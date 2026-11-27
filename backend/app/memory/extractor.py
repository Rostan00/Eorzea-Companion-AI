"""Extração simples de fatos/memórias a partir da conversa."""

from __future__ import annotations

import re
from typing import List, Tuple

from .models import MemoryType


_PREFERENCE_PATTERNS = [
    (r"\beu\s+(gosto|prefiro|adoro|amo|odio|odeio|detesto)\s+.+" , 0.75, ["preferencia"]),
    (r"\bminha?\s+(classe|job|main|servidor|fc|free company)\s+(é|e|eh)\s+.+" , 0.8, ["perfil"]),
    (r"\beu\s+(jogo|jogo de|main)\s+\w+", 0.7, ["perfil", "job"]),
    (r"\b(sempre|nunca|costumo)\s+.+" , 0.65, ["habito"]),
]

_GOAL_PATTERNS = [
    (r"\b(quero|pretendo|vou|preciso)\s+(upar|craftar|fazer|conseguir|completar|farmar)\s+.+" , 0.8, ["objetivo"]),
    (r"\bmeta\s+(é|e|eh)\s+.+" , 0.75, ["objetivo"]),
]

_EVENT_PATTERNS = [
    (r"\b(fizemos|a gente fez|limpamos|zeramos|morremos|wipeamos)\s+.+" , 0.7, ["evento"]),
    (r"\b(hoje|ontem|semana passada)\s+.+" , 0.6, ["evento", "tempo"]),
]


def extract_candidate_memories(
    user_message: str,
    assistant_reply: str = "",
) -> List[Tuple[str, float, List[str], MemoryType]]:
    """
    Analisa a mensagem do usuário e devolve candidatos a memória.

    Retorno: lista de (conteudo, importancia, tags, tipo)
    """
    text = user_message.strip()
    if len(text) < 8:
        return []

    candidates: List[Tuple[str, float, List[str], MemoryType]] = []
    lower = text.lower()

    for pattern, importance, tags in _PREFERENCE_PATTERNS:
        if re.search(pattern, lower, re.IGNORECASE):
            candidates.append((text, importance, tags, MemoryType.SEMANTIC))
            break

    for pattern, importance, tags in _GOAL_PATTERNS:
        if re.search(pattern, lower, re.IGNORECASE):
            candidates.append((text, importance, tags, MemoryType.GOAL))
            break

    for pattern, importance, tags in _EVENT_PATTERNS:
        if re.search(pattern, lower, re.IGNORECASE):
            candidates.append((text, importance, tags, MemoryType.EPISODIC))
            break

    game_keywords = [
        "dungeon", "trial", "raid", "craft", "gather", "island",
        "occult", "crescent", "roulette", "savage", "ultimate",
        "montaria", "minion", "glamour", "gear", "ilvl",
    ]
    if not candidates and any(k in lower for k in game_keywords) and len(text) > 25:
        candidates.append((text, 0.55, ["jogo"], MemoryType.EPISODIC))

    return candidates
