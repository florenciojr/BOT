from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from ..models.produto import Produto
from ..models.fornecedor import Fornecedor
from ..schemas.produto import ProdutoCreate, ProdutoUpdate
from ..database import SessionLocal
from ..utils.logger import logger

class DBService:
    @staticmethod
    async def criar_produto(produto_data: ProdutoCreate):
        async with SessionLocal() as session:
            try:
                produto = Produto(**produto_data.dict())
                session.add(produto)
                await session.commit()
                await session.refresh(produto)
                return produto
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Erro ao criar produto: {str(e)}")
                raise

    @staticmethod
    async def listar_produtos(skip: int = 0, limit: int = 100):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Produto)
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()

    @staticmethod
    async def atualizar_produto(produto_id: int, produto_data: ProdutoUpdate):
        async with SessionLocal() as session:
            try:
                stmt = (
                    update(Produto)
                    .where(Produto.id == produto_id)
                    .values(**produto_data.dict(exclude_unset=True))
                )
                await session.execute(stmt)
                await session.commit()
                return await session.get(Produto, produto_id)
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Erro ao atualizar produto: {str(e)}")
                raise