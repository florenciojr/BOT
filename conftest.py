import pytest
import asyncio
from backend.database import engine

@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para cada sessão de testes"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def clean_db():
    """Garante que cada teste comece com um banco limpo"""
    async with engine.begin() as conn:
        # Aqui você pode adicionar limpeza de tabelas se necessário
        pass