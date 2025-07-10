import openai
from typing import Optional
from ..config import settings
from ..models.produto import EnhancedProduct
from ..utils.formatter import clean_text

openai.api_key = settings.OPENAI_API_KEY


async def enhance_product(
        raw_text: str,
        image_url: Optional[str] = None
) -> EnhancedProduct:
    """Processa texto com IA"""
    try:
        cleaned = clean_text(raw_text)

        if not settings.OPENAI_API_KEY:
            return EnhancedProduct(
                name="Produto",
                description=cleaned,
                price=0.0,
                size="Único",
                hashtags=["#produto"]
            )

        prompt = f"""
        Extraia informações deste produto para WhatsApp:
        {cleaned}

        Retorne JSON com:
        - name: Nome do produto (max 3 palavras)
        - price: Apenas o valor numérico
        - size: Tamanho ou "Único"
        - description: Descrição melhorada (3 linhas)
        - hashtags: 3 hashtags relevantes
        """

        response = await openai.ChatCompletion.acreate(
            model=settings.AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        return EnhancedProduct(**eval(response.choices[0].message.content))

    except Exception as e:
        raise ValueError(f"Erro na IA: {str(e)}")