import asyncio
from sqlalchemy import text
from backend.database import engine

async def testar_conexao():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print("✅ Conectado ao MySQL - versão:", version)

if __name__ == "__main__":
    asyncio.run(testar_conexao())
