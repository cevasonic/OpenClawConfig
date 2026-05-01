import json

json_path = "/opt/openclaw/.openclaw/openclaw.json"
with open(json_path, "r") as f:
    data = json.load(f)

if "gateway" in data and "bonjour" in data["gateway"]:
    del data["gateway"]["bonjour"]

with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print("Bonjour config removed from gateway object.")
