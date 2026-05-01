const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
  process.exit(0);
});

client.on('error', (e) => {
  console.error("Error connecting:", e);
  process.exit(1);
});

client.login('YOUR_DISCORD_BOT_TOKEN').catch(e => {
  console.error("Login failed:", e);
  process.exit(1);
});
