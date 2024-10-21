import pytest
from app.main import app
from fastapi import status
from httpx import AsyncClient


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client):  # pylint: disable=redefined-outer-name
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_healthcheck_endpoint(client):  # pylint: disable=redefined-outer-name
    response = await client.get("/healthz")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
