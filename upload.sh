#!/bin/bash
local_file="new_openclaw.json"
remote_file="/opt/openclaw/.openclaw/openclaw.json"
base64_data=$(base64 -i "$local_file")
./run_ssh.exp "echo $base64_data | base64 -d > $remote_file"

remote_file2="/root/.openclaw/openclaw.json"
./run_ssh.exp "echo $base64_data | base64 -d > $remote_file2"

# Restart OpenClaw (assuming systemctl or pm2 or docker restart)
./run_ssh.exp "systemctl restart openclaw || docker restart openclaw || pm2 restart all"
