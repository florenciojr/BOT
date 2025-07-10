const { create } = require('@open-wa/wa-automate');

create({
  sessionId: 'JR5Session',
  multiDevice: true,
  headless: false,
  useChrome: true,
}).then(async client => {
  console.log('\n📞 Contatos (Fornecedores Individuais):');
  const chats = await client.getAllChats();
  chats
    .filter(chat => !chat.isGroup && chat.id.endsWith('@c.us'))
    .forEach(chat => {
      console.log(`🆔 ${chat.id} | 📛 Nome: ${chat.name || 'Sem Nome'}`);
    });

  console.log('\n👥 Grupos:');
  const grupos = await client.getAllGroups();
  grupos.forEach(group => {
    console.log(`🆔 ${group.id} | 🏷️ Nome: ${group.name}`);
  });

  await client.close(); // Fecha o navegador após listar
});
