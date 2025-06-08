import pytest_asyncio
from httpx import AsyncClient
from app.composites.http_api import app  # твой FastAPI instance
from httpx import ASGITransport

@pytest_asyncio.fixture
async def test_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
