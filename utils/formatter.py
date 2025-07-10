from typing import List
from ..models.produto import Produto

def format_product_message(produto: Produto) -> str:
    """Formata mensagem de produto para envio no WhatsApp"""
    return (
        f"🛍️ *{produto.nome.upper()}* 🛍️\n\n"
        f"💰 *Preço*: {_format_price(produto.preco)}\n"
        f"📏 *Tamanho*: {produto.tamanho or 'Único'}\n"
        f"📦 *Categoria*: {produto.categoria or 'Geral'}\n\n"
        f"{produto.descricao or 'Sem descrição adicional'}\n\n"
        f"🔖 #{produto.categoria or 'produto'} "
        f"🔖 #{produto.fornecedor.nome.replace(' ', '') if produto.fornecedor else 'fornecedor'}"
    )

def _format_price(price: float) -> str:
    """Formata preço para o formato mozambicano"""
    return f"{price:,.2f} MT".replace(",", "X").replace(".", ",").replace("X", ".")