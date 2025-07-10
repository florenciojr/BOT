// bot/services/aiService.js
const { OpenAI } = require('openai');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function interpretarMensagem(texto) {
  try {
    const prompt = `
Extraia as seguintes informações da mensagem de um fornecedor de produtos:

Mensagem: "${texto}"

Retorne como JSON:
{
  "nome": "Nome do produto",
  "descricao": "Descrição detalhada",
  "preco": valor_em_mzn (sem símbolo),
}
    `;

    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
    });

    const resposta = completion.choices[0].message.content.trim();
    return JSON.parse(resposta);
  } catch (err) {
    console.error('❌ Erro na IA:', err.message);
    return null;
  }
}

module.exports = { interpretarMensagem };
