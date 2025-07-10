const axios = require('axios');
const { apiUrl } = require('../config');

async function sendProductToAPI(produto) {
  try {
    const response = await axios.post(apiUrl, produto);
    console.log('✅ Produto enviado:', response.data);
  } catch (error) {
    console.error('❌ Erro ao enviar produto:', error.response?.data || error.message);
  }
}

module.exports = { sendProductToAPI };
