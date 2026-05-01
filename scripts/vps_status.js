const { Client } = require('ssh2');
const conn = new Client();

const config = {
  host: '180.93.137.94',
  port: 22,
  username: 'root',
  password: 'nsM7H_!$?!Ye'
};

conn.on('ready', () => {
  console.log('--- VPS STATUS REPORT ---');
  const cmd = `
    echo "[1] DISK USAGE:"; df -h /;
    echo "\n[2] TOP JUNK LOCATIONS:";
    du -sh /var/log /var/cache/apt /tmp /opt/openclaw/.cache/ms-playwright /opt/openclaw/.npm /opt/openclaw/go/pkg 2>/dev/null;
    echo "\n[3] OPENCLAW STATUS:";
    ps aux | grep -i openclaw-gateway | grep -v grep;
  `;
  
  conn.exec(cmd, (err, stream) => {
    if (err) throw err;
    stream.on('close', () => conn.end())
          .on('data', (data) => process.stdout.write(data))
          .stderr.on('data', (data) => process.stderr.write(data));
  });
}).on('error', (err) => console.error('SSH Connection Error:', err))
  .connect(config);
