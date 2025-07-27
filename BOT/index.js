const { create } = require('@open-wa/wa-automate');
const handleIncomingMessage = require('./controllers/messageController');
const { sessionId, iaNumber } = require('./config');

create({
  sessionId,
  multiDevice: true,
  headless: false,
  useChrome: true,
  qrTimeout: 0,
  authTimeout: 60,
  cacheEnabled: false,
}).then(async client => {
  console.log(`🤖 Bot iniciado com sessão: ${sessionId}`);

  client.onMessage(async (message) => {
    try {
      // Ignora mensagens que vêm da IA
      if (message.from !== iaNumber) {
        const result = await handleIncomingMessage(message, client);

        if (result.status === 'reenviado') {
          console.log(`✅ Produto de ${message.sender.pushname || message.from} reencaminhado com sucesso`);
        } else if (result.status === 'ignorado') {
          console.log(`ℹ️ Mensagem ignorada de ${message.sender.pushname || message.from}`);
        } else if (result.status === 'erro') {
          await client.sendText(message.from, '❌ Erro ao processar sua mensagem.');
        }
      }
    } catch (error) {
      console.error('❌ Erro ao processar mensagem:', error);
    }
  });
});
