import json

with open("clean_openclaw.json", "r") as f:
    data = json.load(f)

# Define two OpenRouter providers for separate keys
data["models"]["providers"]["openrouter-step"] = {
    "baseUrl": "https://openrouter.ai/api/v1",
    "api": "openai-completions",
    "apiKey": "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",
    "models": [
        {"id": "stepfun/step-3.5-flash", "name": "Step 3.5 Flash"}
    ]
}

data["models"]["providers"]["openrouter-gemma"] = {
    "baseUrl": "https://openrouter.ai/api/v1",
    "api": "openai-completions",
    "apiKey": "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",
    "models": [
        {"id": "google/gemma-4-31b-it", "name": "Gemma 4 31B"}
    ]
}

# Remove the old consolidated one if it exists
if "openrouter" in data["models"]["providers"]:
    del data["models"]["providers"]["openrouter"]

# Target IDs
primary_model = "openrouter-step/stepfun/step-3.5-flash"
other_model = "openrouter-gemma/google/gemma-4-31b-it"

data["agents"]["defaults"]["model"] = {
    "primary": primary_model
}

# Clear and update agents.defaults.models
data["agents"]["defaults"]["models"] = {
    "trollllm/gemini-3.1-pro": {},
    "trollllm/claude-haiku-4.5": {},
    primary_model: {},
    other_model: {}
}

# Enable plugins (only valid plugins should be here)
# 'openrouter-step' and 'openrouter-gemma' are model providers, not plugins.

with open("new_openclaw.json", "w") as f:
    json.dump(data, f, indent=2)
