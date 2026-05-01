import json
import os

json_path = "/opt/openclaw/.openclaw/openclaw.json"

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    if "auth" not in data:
        data["auth"] = {}
    if "profiles" not in data["auth"]:
        data["auth"]["profiles"] = {}
        
    data["auth"]["profiles"]["elevated"] = {
        "allowFrom": ["telegram"]
    }

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print("Auth profiles updated successfully.")
else:
    print("Config file not found.")
