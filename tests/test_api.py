"""Testes básicos da API."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health():
    """Verifica se o endpoint de saúde responde corretamente."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_chat_basic():
    """Testa o endpoint de chat com uma mensagem simples."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat",
            json={"message": "Oi, tudo bem?"},
        )

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "character_name" in data
    assert len(data["reply"]) > 0
    assert data["character_name"] == "Lauda"


@pytest.mark.asyncio
async def test_chat_with_history():
    """Testa o chat passando histórico de mensagens."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat",
            json={
                "message": "Bora fazer uma dungeon?",
                "history": [
                    {"role": "user", "content": "Oi"},
                    {"role": "assistant", "content": "Eae. Pronto pra mais uma sessão?"},
                ],
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 0
