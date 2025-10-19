import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_status_endpoint_ok():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/status/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "Operacional"
    assert "Microsserviço de Equipamentos está online" in data["mensagem"]
