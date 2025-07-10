const handleIncomingMessage = require('../controllers/messageController');
const { fornecedores, grupoDestino } = require('../config');

(async () => {
  const fornecedorSimulado = fornecedores[0];

  const fakeMessage = {
    isGroupMsg: false,
    sender: { id: fornecedorSimulado, pushname: 'JR5 Movitel' },
    from: fornecedorSimulado,
    body: 'Powerbank Original 10000mAh, ideal para emergências',
    mimetype: null
  };

  const fakeClient = {
    decryptFile: async () => null, // não usamos imagem
    sendText: async (to, message) => {
      console.log(`✅ MENSAGEM ENVIADA PARA ${to}:\n${message}`);
    },
    sendImage: async (to, base64, filename, caption) => {
      console.log(`📷 IMAGEM ENVIADA PARA ${to} (${filename}):\n${caption}`);
    }
  };

  await handleIncomingMessage(fakeMessage, fakeClient);
})();
