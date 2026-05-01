import json

with open("openclaw_config.json", "r") as f:
    config = json.load(f)

# Add new provider
new_provider_id = "openrouter-nvidia"
config["models"]["providers"][new_provider_id] = {
    "baseUrl": "https://openrouter.ai/api/v1",
    "api": "openai-completions",
    "apiKey": "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",
    "models": [
        {"id": "nvidia/nemotron-3-super-120b-a12b:free", "name": "NVIDIA: Nemotron 3 Super (free)"}
    ]
}

# Register model with agent
model_path = f"{new_provider_id}/nvidia/nemotron-3-super-120b-a12b:free"
if "agents" in config and "defaults" in config["agents"] and "models" in config["agents"]["defaults"]:
    config["agents"]["defaults"]["models"][model_path] = {}

with open("openclaw_config_updated.json", "w") as f:
    json.dump(config, f, indent=2)

print(f"Added model: {model_path}")
