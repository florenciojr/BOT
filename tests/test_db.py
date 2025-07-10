import pytest
from sqlalchemy import create_engine, text, insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from backend.models.produto import Produto
from backend.database import Base
from backend.config import settings

TEST_DB_CONFIG = {
    "DB_HOST": "localhost",
    "DB_PORT": 3306,
    "DB_USER": "root",
    "DB_PASSWORD": "",
    "DB_NAME": "reencaminhamento_produtos"
}


@pytest.fixture(scope="module")
def engine_and_session():
    # Monta string de conexão
    db_url = (
        f"mysql+pymysql://{TEST_DB_CONFIG['DB_USER']}:{TEST_DB_CONFIG['DB_PASSWORD']}"
        f"@{TEST_DB_CONFIG['DB_HOST']}:{TEST_DB_CONFIG['DB_PORT']}/{TEST_DB_CONFIG['DB_NAME']}"
    )
    engine = create_engine(db_url, echo=True)
    Session = sessionmaker(bind=engine)

    # Cria as tabelas
    Base.metadata.create_all(bind=engine)

    yield engine, Session

    # Limpa as tabelas no final
    Base.metadata.drop_all(bind=engine)


def test_db_connection(engine_and_session):
    engine, Session = engine_and_session
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            assert result.scalar() == TEST_DB_CONFIG["DB_NAME"]
    except SQLAlchemyError as e:
        pytest.fail(f"Erro de conexão: {str(e)}")


def test_full_crud(engine_and_session):
    engine, Session = engine_and_session
    session = Session()

    test_data = {
        "nome": "Produto Teste",
        "preco": 99.99,
        "tamanho": "M",
        "categoria": "Teste"
    }

    # CREATE
    produto = Produto(**test_data)
    session.add(produto)
    session.commit()
    session.refresh(produto)

    assert produto.id is not None

    # READ
    produto_lido = session.query(Produto).filter_by(nome="Produto Teste").first()
    assert produto_lido is not None
    assert produto_lido.preco == 99.99

    # UPDATE
    produto_lido.preco = 120.00
    session.commit()
    session.refresh(produto_lido)
    assert produto_lido.preco == 120.00

    # DELETE
    session.delete(produto_lido)
    session.commit()
    assert session.query(Produto).filter_by(id=produto_lido.id).first() is None
