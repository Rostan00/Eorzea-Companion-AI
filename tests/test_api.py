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
    assert "memory_count" in data


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
    assert "memories_used" in data


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


@pytest.mark.asyncio
async def test_create_and_list_memories():
    """Testa criação e listagem de memórias via API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post(
            "/api/v1/memories",
            json={
                "content": "O jogador prefere fazer Occult Crescent de madrugada",
                "importance": 0.8,
                "tags": ["preferencia", "occult"],
                "memory_type": "semantic",
            },
        )
        assert create_resp.status_code == 200
        created = create_resp.json()
        assert created["content"].startswith("O jogador prefere")

        list_resp = await client.get("/api/v1/memories?limit=10")
        assert list_resp.status_code == 200
        listed = list_resp.json()
        assert listed["total"] >= 1
        assert len(listed["items"]) >= 1
