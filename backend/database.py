from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from backend.config import settings  # suas configs do .env ou config.py

# 🔧 Monta URL da base de dados
DATABASE_URL = (
    f"mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# 🛠️ Criação do engine com pooling (similar ao Java MysqlDataSource)
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,               # Mostra logs SQL se debug = True
    pool_size=settings.DB_POOL_SIZE,   # Ex: 10
    max_overflow=settings.DB_MAX_OVERFLOW,  # Ex: 20 conexões extra
    pool_pre_ping=True,                # Testa conexão antes de usar
    poolclass=QueuePool,               # Tipo de pool
    future=True
)

# 🔄 Criar sessões do SQLAlchemy com suporte async
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# 📦 Base para todos os modelos
Base = declarative_base()

# ⚙️ Injeção de dependência segura
async def get_db():
    """Fornece uma sessão do banco para usar em rotas"""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
s