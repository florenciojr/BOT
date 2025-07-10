from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import APIKeyHeader
from ..services.whatsapp_service import WhatsAppService
from ..services.ai_service import AIService
from ..schemas.produto import ProdutoCreate
from ..utils.validator import validate_whatsapp_message
from ..utils.logger import logger

router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-KEY")


@router.post("/whatsapp")
async def whatsapp_webhook(
        request: Request,
        api_key: str = Depends(api_key_header)
):
    if api_key not in settings.API_KEYS:
        raise HTTPException(status_code=403, detail="Acesso não autorizado")

    try:
        payload = await request.json()
        if not validate_whatsapp_message(payload):
            raise HTTPException(status_code=400, detail="Mensagem inválida")

        # Processar com IA
        enhanced_product = await AIService.enhance_product_description(
            payload["message"],
            payload.get("media_url")
        )

        # Salvar no banco e reencaminhar
        await WhatsAppService.process_incoming_product(enhanced_product)

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")