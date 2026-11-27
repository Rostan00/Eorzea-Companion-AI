"""Interface base para provedores de LLM."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMProvider(ABC):
    """Contrato que todo provedor de LLM deve implementar."""

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Gera uma resposta a partir do system prompt e do histórico de mensagens.

        Args:
            system_prompt: Instruções de sistema / persona.
            messages: Lista de mensagens no formato [{"role": "user"|"assistant", "content": "..."}]
            temperature: Controle de criatividade.
            max_tokens: Limite de tokens na resposta.

        Returns:
            Texto da resposta gerada.
        """
        pass
