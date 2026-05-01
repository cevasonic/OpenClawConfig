import json

json_path = "/opt/openclaw/.openclaw/openclaw.json"

with open(json_path, "r") as f:
    data = json.load(f)

if "gateway" in data:
    data["gateway"]["bonjour"] = {"enabled": False}

with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print("Bonjour disabled successfully.")
