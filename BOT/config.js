require('dotenv').config();

module.exports = {
  sessionId: process.env.SESSION_ID || 'JR5Session',
  apiUrl: process.env.API_URL || 'http://localhost:8000/api/v1/produtos',
  fornecedores: process.env.FORNECEDORES_AUTORIZADOS?.split(',') || [],
  grupoDestino: process.env.GRUPO_DESTINO
};
