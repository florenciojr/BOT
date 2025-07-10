import logging
from venom import Bot
from typing import Optional
from ..models.produto import Produto
from ..models.grupo import GrupoVendas
from ..services.db_service import DBService
from ..config import settings
from ..utils.formatter import format_product_message

logger = logging.getLogger(__name__)


class WhatsAppService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.bot = Bot(settings.WHATSAPP_SESSION)
        return cls._instance

    @classmethod
    async def process_incoming_product(cls, product_data: dict):
        try:
            # Salvar no banco
            produto = await DBService.criar_produto(product_data)

            # Obter grupos ativos
            grupos = await DBService.listar_grupos_ativos()

            # Enviar para cada grupo
            for grupo in grupos:
                await cls._send_to_group(produto, grupo.grupo_id)

            logger.info(f"Produto {produto.id} processado com sucesso")

        except Exception as e:
            logger.error(f"Falha ao processar produto: {str(e)}")
            raise

    @classmethod
    async def _send_to_group(cls, produto: Produto, grupo_id: str):
        try:
            message = format_product_message(produto)

            if produto.midias:
                await cls._instance.bot.send_image(
                    grupo_id,
                    produto.midias[0].url,
                    caption=message
                )
            else:
                await cls._instance.bot.send_text(grupo_id, message)

            await DBService.registrar_envio(produto.id, grupo_id)

        except Exception as e:
            logger.error(f"Falha ao enviar para grupo {grupo_id}: {str(e)}")
            await DBService.registrar_falha(produto.id, grupo_id, str(e))