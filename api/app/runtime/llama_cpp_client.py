import os
import httpx

LLAMA_BASE_URL = os.getenv("LLAMA_BASE_URL", "http://localhost:8080/v1")
LLAMA_MODEL_ALIAS = os.getenv("LLAMA_MODEL_ALIAS", "microgpt-local")


async def generate_answer(message: str) -> tuple[str, str]:
    payload = {
        "model": LLAMA_MODEL_ALIAS,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are MicroGPT, a CPU-first open-source assistant. "
                    "Provide useful, creative, safe answers. Refuse violent or sexual content. "
                    "When factual, prefer evidence and cite sources when retrieval is available."
                ),
            },
            {"role": "user", "content": message},
        ],
        "temperature": 0.2,
        "max_tokens": 512,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{LLAMA_BASE_URL}/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"], "llama.cpp"
    except Exception:
        fallback = (
            "MicroGPT runtime is reachable at the API layer, but the local llama.cpp model server "
            "is not available yet. Add a GGUF model to ./models/model.gguf and start the inference profile."
        )
        return fallback, "fallback"
