import json
import os
import time
from datetime import datetime, timezone

from openai import OpenAI


def _parse_worker_models(default_models):
    raw = os.getenv("WORKER_MODELS", "").strip()
    if not raw:
        return default_models
    parsed = [item.strip() for item in raw.split(",") if item.strip()]
    return parsed if parsed else default_models


DEFAULT_WORKER_MODELS = [
    "openrouter/elephant-alpha",
    "minimax/minimax-m2.5:free",
    "google/gemma-4-31b-it:free",
]

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
LOG_PATH = os.getenv("CHAT_LOG_PATH", "chat_history.jsonl")

# 1. Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "your-openrouter-key-here"),
)

# Define the models you want to use
# Note: Ensure these model strings are currently available on OpenRouter
worker_models = _parse_worker_models(DEFAULT_WORKER_MODELS)

# The model that will synthesize the final answer
judge_model = os.getenv("JUDGE_MODEL", "arcee-ai/trinity-large-preview:free")


def call_model_with_retry(model_id, messages):
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=REQUEST_TIMEOUT,
            )
            return response.choices[0].message.content
        except Exception as err:
            last_error = err
            if attempt < MAX_RETRIES:
                time.sleep(1 + attempt)
    raise RuntimeError(
        f"Failed calling {model_id} after {MAX_RETRIES + 1} attempt(s): {last_error}"
    )


def log_turn(user_input, worker_responses, final_answer):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_input": user_input,
        "worker_models": worker_models,
        "worker_responses": worker_responses,
        "judge_model": judge_model,
        "final_answer": final_answer,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

print("Multi-Model Chatbot started! (Type 'quit' to stop)")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    worker_responses = []

    # 2. Collect answers from all worker models
    print("Consulting the experts...")
    for model_id in worker_models:
        try:
            print(f" -> Querying {model_id}...")
            ans = call_model_with_retry(
                model_id, [{"role": "user", "content": user_input}]
            )
            worker_responses.append(f"Model ({model_id}):\n{ans}")
        except Exception as e:
            print(f"Error calling {model_id}: {e}")

    # 3. Combine the answers into a single string for the "Judge"
    combined_context = "\n\n---\n\n".join(worker_responses)

    final_prompt = f"""
    A user asked: "{user_input}"

    I have gathered responses from {len(worker_responses)} different AI models.
    Your task is to compare these answers, resolve any contradictions, and provide the most accurate,
    comprehensive final response.

    HERE ARE THE RESPONSES:
    {combined_context}

    FINAL ACCURATE ANSWER:
    """

    # 4. Call the final "Judge" model to process everything
    print("Finalizing answer...")
    final_answer = call_model_with_retry(
        judge_model, [{"role": "user", "content": final_prompt}]
    )

    log_turn(user_input, worker_responses, final_answer)

    print("-" * 30)
    print(f"AI FINAL ANSWER:\n{final_answer}")
    print("-" * 30)
