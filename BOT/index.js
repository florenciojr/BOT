const { create } = require('@open-wa/wa-automate');
const handleIncomingMessage = require('./controllers/messageController');
const { sessionId } = require('./config');

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

  // 📩 Quando chegar nova mensagem
  client.onMessage(async (message) => {
    try {
      const status = await handleIncomingMessage(message, client);

      if (status === 'reenviado') {
        console.log(`✅ Produto de ${message.sender.pushname || message.from} reencaminhado com sucesso`);
      } else if (status === 'ignorado') {
        console.log(`ℹ️ Mensagem ignorada de ${message.sender.pushname || message.from}`);
      }

    } catch (error) {
      console.error('❌ Erro ao processar mensagem:', error);
      await client.sendText(message.from, '❌ Erro ao processar sua mensagem.');
    }
  });

}).catch(error => {
  console.error('❌ Erro ao iniciar bot:', error);
  process.exit(1);
});
