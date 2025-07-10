# Exportações principais
from .app import app
from .database import Base, engine, SessionLocal
from .config import settings

__all__ = ['app', 'Base', 'engine', 'SessionLocal', 'settings']
__version__ = "1.0.0"


def models():
    return None