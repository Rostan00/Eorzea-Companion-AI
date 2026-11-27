"""Implementação mock do provedor de LLM para desenvolvimento e testes."""

from typing import List, Dict
from .base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Provedor falso usado enquanto não há chave de API real.
    Responde de forma simples e determinística para permitir testes.
    """

    async def generate(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        if not messages:
            return "Oi. Estou pronta quando você estiver."

        last_user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_message = msg.get("content", "").lower()
                break

        # Respostas simples baseadas em palavras-chave (apenas para desenvolvimento)
        if any(word in last_user_message for word in ["dungeon", "duty", "roulette", "raid", "trial"]):
            return (
                "Beleza. Qual a gente vai fazer? "
                "Se for roulette eu entro de tank ou healer, você escolhe. "
                "Só não esquece de checar o gear antes."
            )

        if any(word in last_user_message for word in ["craft", "crafting", "receita", "synth"]):
            return (
                "Crafting? Me fala o que você precisa. "
                "Eu posso te ajudar a planejar a rota de materiais ou só acompanhar enquanto você faz."
            )

        if any(word in last_user_message for word in ["ilha", "island", "sanctuary"]):
            return (
                "Island Sanctuary? Boa. "
                "Eu gosto de manter os pastos organizados e focar nos materiais que estão faltando pro craft da semana. "
                "Quer que eu monte um checklist rápido?"
            )

        if any(word in last_user_message for word in ["occult", "crescent", "moon"]):
            return (
                "Occult Crescent tá com boa janela agora. "
                "Bora. Eu fico de olho nos eventos e te aviso se aparecer alguma coisa interessante."
            )

        if any(word in last_user_message for word in ["oi", "olá", "eae", "fala", "hey", "hi"]):
            return "Eae. Pronto pra jogar ou só veio falar?"

        # Resposta genérica
        return (
            "Ok. Me fala o que você quer fazer — dungeon, craft, ilha, Occult... "
            "Eu me viro com qualquer uma."
        )
