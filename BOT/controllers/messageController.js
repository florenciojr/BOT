const { fornecedores, iaNumber, promptIA, grupoVendas } = require('../config');

async function aguardarRespostaIA(client, iaNumber, ultimoIdAntes, timeoutMs = 30000, intervaloMs = 3000) {
  const inicio = Date.now();

  while (Date.now() - inicio < timeoutMs) {
    const mensagens = await client.getAllMessagesInChat(iaNumber, true, true);
    for (let i = mensagens.length - 1; i >= 0; i--) {
      const msg = mensagens[i];
      if (msg.id === ultimoIdAntes) break;
      if (!msg.fromMe && msg.type === 'chat' && msg.body?.trim().length > 0) {
        return msg.body.trim();
      }
    }
    await new Promise(resolve => setTimeout(resolve, intervaloMs));
  }

  return null;
}

module.exports = async function handleIncomingMessage(message, client) {
  try {
    if (message.isGroupMsg) return { status: 'ignorado' };

    const remetente = message.sender.id;
    const body = message.body?.trim() || '';
    const image = message.mimetype?.includes('image') ? message : null;

    if (!fornecedores.includes(remetente)) {
      console.log(`🚫 Mensagem de remetente não autorizado: ${remetente}`);
      return { status: 'ignorado' };
    }

    if (!body && !image) {
      console.log(`⚠️ Mensagem vazia de ${remetente}`);
      return { status: 'ignorado' };
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

    const msgsAntes = await client.getAllMessagesInChat(iaNumber, true, true);
    const ultimoIdAntes = msgsAntes.length > 0 ? msgsAntes[msgsAntes.length - 1].id : null;

    const textoParaIA = `${promptIA}\n\n${body}`;
    if (image) {
      await client.sendImage(iaNumber, produto.midias[0].url, 'produto.jpg', textoParaIA);
    } else {
      await client.sendText(iaNumber, textoParaIA);
    }

    const novaResposta = await aguardarRespostaIA(client, iaNumber, ultimoIdAntes);

    if (novaResposta) {
      console.log('🧠 Resposta da IA:', novaResposta);
      await client.sendText(grupoVendas, novaResposta);
      return { status: 'reenviado' };
    } else {
      console.log('⚠️ IA não respondeu a tempo.');
      await client.sendText(remetente, '⚠️ A IA não respondeu. Tente de novo em 1 minuto.');
      return { status: 'erro' };
    }
  } catch (error) {
    console.error('❌ Erro em handleIncomingMessage:', error);
    await client.sendText(message.from, '❌ Ocorreu um erro ao processar sua mensagem.');
    return { status: 'erro' };
  }
};
