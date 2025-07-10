from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    preco = Column(Float, nullable=False)
    tamanho = Column(String(20))
    categoria = Column(String(50))
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    data_cadastro = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    midias = relationship("Midia", back_populates="produto")
    logs = relationship("LogReencaminhamento", back_populates="produto")

    def __repr__(self):
        return f"<Produto {self.nome} - {self.preco} MT>"