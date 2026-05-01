const { Client } = require('ssh2');
const conn = new Client();

const config = {
  host: '180.93.137.94',
  port: 22,
  username: 'root',
  password: 'nsM7H_!$?!Ye'
};

conn.on('ready', () => {
  console.log('--- STARTING SAFE VPS CLEANUP ---');
  const commands = [
    'apt-get clean',
    'journalctl --vacuum-time=3d',
    'npm cache clean --force',
    'cd /opt/openclaw && npm cache clean --force',
    'rm -rf /root/.cache/ms-playwright/*',
    'rm -rf /opt/openclaw/.cache/ms-playwright/*',
    'rm -rf /opt/openclaw/go/pkg/mod/*',
    'rm -f /opt/openclaw/.openclaw/openclaw.json.clobbered.*',
    'rm -f /opt/openclaw/.openclaw/openclaw.json.bak.*',
    'rm -rf /tmp/*',
    'df -h /'
  ];
  
  const runNext = (i) => {
    if (i >= commands.length) {
      console.log('--- CLEANUP FINISHED ---');
      return conn.end();
    }
    console.log(`> ${commands[i]}`);
    conn.exec(commands[i], (err, stream) => {
      if (err) {
        console.error(err);
        return runNext(i + 1);
      }
      stream.on('close', () => runNext(i + 1))
            .on('data', (data) => process.stdout.write(data))
            .stderr.on('data', (data) => process.stderr.write(data));
    });
  };
  runNext(0);
}).on('error', (err) => console.error('SSH Connection Error:', err))
  .connect(config);
