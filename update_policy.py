import json
import os

json_path = "/opt/openclaw/.openclaw/openclaw.json"

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    if "channels" in data and "discord" in data["channels"]:
        data["channels"]["discord"]["dm"] = {"policy": "open"}

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

print("Policy updated successfully.")
