import json
import os

env_path = "/opt/openclaw/.env"
json_path = "/opt/openclaw/.openclaw/openclaw.json"
token = "YOUR_DISCORD_BOT_TOKEN"

# 1. Update .env
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        lines = f.readlines()
    
    with open(env_path, "w") as f:
        found = False
        for line in lines:
            if "DISCORD_BOT_TOKEN=" in line:
                f.write(f"DISCORD_BOT_TOKEN={token}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"\nDISCORD_BOT_TOKEN={token}\n")

# 2. Update openclaw.json
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    if "channels" not in data:
        data["channels"] = {}
    
    data["channels"]["discord"] = {
        "enabled": True,
        "token": token,
        "dm": {"policy": "open"}
    }

    if "plugins" not in data:
        data["plugins"] = {"entries": {}}
    
    if "entries" not in data["plugins"]:
        data["plugins"]["entries"] = {}

    data["plugins"]["entries"]["discord"] = {"enabled": True}

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

print("Token updated successfully.")
