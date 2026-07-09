import os
import json
import traceback
from openai import OpenAI
from dotenv import load_dotenv

# Load env variables for local testing (Harness will override these in production)
load_dotenv()

# --- HARNESS ENVIRONMENT VARIABLES ---
# The harness will inject these during grading.
API_KEY = os.environ.get("FIREWORKS_API_KEY", "dummy-key-for-local")
BASE_URL = os.environ.get("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")
ALLOWED_MODELS_STR = os.environ.get("ALLOWED_MODELS", "accounts/fireworks/models/llama-v3-8b-instruct,accounts/fireworks/models/llama-v3-70b-instruct")
ALLOWED_MODELS = [m.strip() for m in ALLOWED_MODELS_STR.split(",")]

# Ensure we have models to pick from
if not ALLOWED_MODELS:
    raise ValueError("No allowed models provided by harness!")

# For our strategy: 
# We assume the first model in the list is the smaller/faster one, 
# and the last model is the larger/smarter one.
SMALL_MODEL = ALLOWED_MODELS[0]
BIG_MODEL = ALLOWED_MODELS[-1]

# Initialize OpenAI client to route through Fireworks API
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def classify_task_complexity(prompt: str) -> str:
    """
    Zero-Token Local Router:
    Decides whether a task requires a complex model (BIG_MODEL) 
    or if it can be handled by a simpler model (SMALL_MODEL).
    We use simple heuristics here to save 100% of routing tokens.
    """
    prompt_lower = prompt.lower()
    
    # Complex tasks: coding, multi-step math, logic puzzles
    complex_keywords = [
        "code", "python", "function", "bug", "debug", "react",
        "puzzle", "logic", "deduce", "mathematical", "equation"
    ]
    
    if any(keyword in prompt_lower for keyword in complex_keywords):
        return "COMPLEX"
        
    return "SIMPLE"

def process_task(prompt: str) -> str:
    """
    Processes a single task by routing it to the appropriate model.
    """
    complexity = classify_task_complexity(prompt)
    
    # Pick model based on local heuristic routing
    selected_model = BIG_MODEL if complexity == "COMPLEX" else SMALL_MODEL
    
    print(f"[*] Routing to {selected_model} (Reason: {complexity})")
    
    # Make the API call to Fireworks
    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are a highly accurate and concise AI assistant. Provide exactly what is asked without extra conversational filler to save tokens."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1 # Keep it deterministic for accuracy
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[!] Error calling API: {e}")
        return "Error generating response."

def main():
    print("🚀 Starting Agent container...")
    
    input_file = "/input/tasks.json"
    output_file = "/output/results.json"
    
    # For local testing, we adjust paths if we are not running inside Docker
    if not os.path.exists("/input"):
        input_file = "./input/tasks.json"
        output_file = "./output/results.json"
    
    # 1. Read tasks
    if not os.path.exists(input_file):
        print(f"[!] Error: {input_file} not found. Exiting.")
        exit(1)
        
    with open(input_file, "r") as f:
        tasks = json.load(f)
        
    print(f"[*] Loaded {len(tasks)} tasks.")
    
    results = []
    
    # 2. Process each task
    for task in tasks:
        task_id = task.get("task_id")
        prompt = task.get("prompt")
        
        print(f"\n--- Processing Task: {task_id} ---")
        answer = process_task(prompt)
        
        results.append({
            "task_id": task_id,
            "answer": answer
        })
    
    # 3. Write results
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\n✅ All tasks completed. Results written to {output_file}")
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        traceback.print_exc()
        exit(1) # Guide says: non-zero on failure
