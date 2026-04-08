import os
import json
import requests
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Hugging Face Client Initialization ---
client = InferenceClient(
    model=MODEL_NAME,
    token=HF_TOKEN
)

def get_action_from_llm(observation: dict) -> dict:
    """
    Gets an action from the LLM based on the current observation.
    This is a very basic example. A real agent would have a more sophisticated prompt.
    """
    prompt = f"""
    You are an expert logistics dispatcher. Based on the following environment observation, decide the best action to take.
    Your available actions are:
    - pickup_order (action_type=0, order_id=<id>)
    - deliver_order (action_type=1, order_id=<id>)
    - wait (action_type=2, order_id=0)

    Observation:
    {json.dumps(observation, indent=2)}

    Provide your action as a JSON object with "action_type" and "order_id".
    For "wait", order_id can be 0.
    Example: {{"action_type": 0, "order_id": 1}}
    """

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        action_str = response.choices[0].message.content
        return json.loads(action_str)
    except Exception as e:
        print(f"Error getting action from LLM: {e}")
        # Fallback to a simple action if LLM fails
        return {"action_type": 2, "order_id": 0} # Wait

def run_inference():
    """
    Runs a complete episode, interacting with the environment API.
    """
    print("[START]")
    
    # 1. Reset the environment
    response = requests.post(f"{API_BASE_URL}/api/v1/reset")
    if response.status_code != 200:
        print(f"Error resetting environment: {response.text}")
        return
    
    data = response.json()
    obs = data["observation"]
    info = data["info"]
    
    terminated = False
    truncated = False
    total_reward = 0
    step_count = 0

    while not terminated and not truncated:
        print("Loop running...")
        # 2. Get action from the agent (LLM)
        action = get_action_from_llm(obs)
        
        # 3. Take a step in the environment
        step_response = requests.post(f"{API_BASE_URL}/api/v1/step", json=action)
        
        if step_response.status_code != 200:
            print(f"Error during step: {step_response.text}")
            break
            
        step_data = step_response.json()
        
        obs = step_data["observation"]
        reward = step_data["reward"]
        terminated = step_data["terminated"]
        truncated = step_data["truncated"]
        info = step_data["info"]
        
        total_reward += reward
        step_count += 1
        
        # 4. Log the step
        log_entry = {
            "step": step_count,
            "action": action,
            "observation": obs,
            "reward": reward,
            "total_reward": total_reward,
            "terminated": terminated,
            "truncated": truncated,
            "info": info
        }
        print(f"[STEP] {json.dumps(log_entry)}")

    # 5. Log the final result
    final_log = {
        "total_steps": step_count,
        "final_reward": total_reward,
        "final_info": info
    }
    print(f"[END] {json.dumps(final_log)}")

if __name__ == "__main__":
    run_inference()
print("HF TOKEN:", HF_TOKEN)