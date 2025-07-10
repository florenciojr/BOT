const { sendProductToAPI } = require('../services/apiService');
const { fornecedores, grupoDestino } = require('../config');

module.exports = async function handleIncomingMessage(message, client) {
  try {
    if (message.isGroupMsg) return 'ignorado';

    const remetente = message.sender.id;
    const body = message.body?.trim() || '';
    const image = message.mimetype?.includes('image') ? message : null;

    if (!fornecedores.includes(remetente)) {
      console.log(`🚫 Mensagem de remetente não autorizado: ${remetente}`);
      return 'ignorado';
    }

    if (!body && !image) {
      console.log(`⚠️ Mensagem vazia de ${remetente}`);
      return 'ignorado';
    }

    const produto = {
      nome: body.substring(0, 50),
      preco: 0,
      descricao: body,
      fornecedor_nome: remetente,
      midias: []
    };

    if (image) {
      const mediaData = await client.decryptFile(image);
      const base64 = Buffer.from(mediaData, 'binary').toString('base64');
      const url = `data:${image.mimetype};base64,${base64}`;
      produto.midias.push({ url });
    }

    // 🔁 Envia para API
    await sendProductToAPI(produto);

    // 📤 Reencaminha para grupo
    const legenda = `📦 Produto de fornecedor: ${produto.fornecedor_nome}\n\n${produto.descricao}`;
    if (produto.midias.length > 0) {
      await client.sendImage(grupoDestino, produto.midias[0].url, 'produto.jpg', legenda);
    } else {
      await client.sendText(grupoDestino, legenda);
    }

    return 'reenviado';
  } catch (error) {
    console.error('❌ Erro em handleIncomingMessage:', error);
    return 'erro';
  }
};
