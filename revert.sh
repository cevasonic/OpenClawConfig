#!/bin/bash
local_file="clean_openclaw.json"
remote_file="/opt/openclaw/.openclaw/openclaw.json"
base64_data=$(base64 -i "$local_file")
./run_ssh.exp "echo $base64_data | base64 -d > $remote_file"
remote_file2="/root/.openclaw/openclaw.json"
./run_ssh.exp "echo $base64_data | base64 -d > $remote_file2"

# Restart
./run_ssh.exp "systemctl restart openclaw"
