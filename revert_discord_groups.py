import json

json_path = "/opt/openclaw/.openclaw/openclaw.json"
with open(json_path, "r") as f:
    data = json.load(f)

if "channels" in data and "discord" in data["channels"]:
    if "groups" in data["channels"]["discord"]:
        del data["channels"]["discord"]["groups"]

with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print("Groups config removed.")
