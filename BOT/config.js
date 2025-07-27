require('dotenv').config();

module.exports = {
  sessionId: process.env.SESSION_ID || 'JR5Session',
  apiUrl: process.env.API_URL || 'http://localhost:8000/api/v1/produtos',
  fornecedores: process.env.FORNECEDORES_AUTORIZADOS?.split(',') || [],
  grupoDestino: process.env.GRUPO_DESTINO,
  iaNumber: process.env.IA_NUMBER, // Número da IA no WhatsApp
  promptIA: process.env.PROMPT_IA || 'Formate este produto para venda no WhatsApp. Padronize nome, preço, marca e garantia. Não use emojis. Exemplo:\nSAMSUNG A12 64GB Preto - 1 Ano Garantia Preço: 15.500 MT',
  grupoVendas: process.env.GRUPO_VENDAS // Grupo de vendas para enviar resposta da IA
};
