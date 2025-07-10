from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import produtos, webhook, grupos
from .config import settings
from .utils.logger import setup_logging
from .database import engine, Base

app = FastAPI(
    title="Sistema de Reencaminhamento Automatizado",
    version=__version__,
    description="API para processar e reencaminhar produtos via WhatsApp"
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(produtos.router, prefix="/api/v1/produtos")
app.include_router(webhook.router, prefix="/api/v1/webhook")
app.include_router(grupos.router, prefix="/api/v1/grupos")

@app.on_event("startup")
async def startup():
    setup_logging()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)