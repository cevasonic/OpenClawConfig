import json

config_file = "openclaw_config_v4.json"
with open(config_file, "r") as f:
    config = json.load(f)

# 1. Add model to OpenRouter provider
new_model = {
    "id": "openrouter/free",
    "name": "Free Models Router"
}

if "openrouter" in config["models"]["providers"]:
    exists = any(m["id"] == new_model["id"] for m in config["models"]["providers"]["openrouter"]["models"])
    if not exists:
        config["models"]["providers"]["openrouter"]["models"].append(new_model)
        print(f"Added model {new_model['id']} to OpenRouter provider.")
    else:
        print(f"Model {new_model['id']} already exists in OpenRouter provider.")
else:
    print("Error: openrouter provider not found in config.")

# 2. Register model with agent defaults
agent_model_path = f"openrouter/{new_model['id']}"
if "agents" in config and "defaults" in config["agents"] and "models" in config["agents"]["defaults"]:
    if agent_model_path not in config["agents"]["defaults"]["models"]:
        config["agents"]["defaults"]["models"][agent_model_path] = {}
        print(f"Registered model {agent_model_path} with agent defaults.")
    else:
        print(f"Model {agent_model_path} already registered with agent defaults.")

# Write updated config
with open("openclaw_config_v5.json", "w") as f:
    json.dump(config, f, indent=2)

print("Updated config saved to openclaw_config_v5.json")
