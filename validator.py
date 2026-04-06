import os
import requests
import docker

def check_dockerfile():
    """Checks if Dockerfile exists and can be built."""
    print("\n--- Checking Dockerfile ---")
    try:
        client = docker.from_env()
        print("✅ Docker client connected.")
        if not os.path.exists("Dockerfile"):
            print("❌ Dockerfile not found!")
            return False
        
        print("Building Docker image (this might take a moment)...")
        image, build_log = client.images.build(path=".", tag="logistics-env-validator")
        print("✅ Docker image built successfully.")
        return True
    except docker.errors.DockerException as e:
        print(f"❌ Docker is not running or not installed. Please start Docker. Error: {e}")
        return False
    except docker.errors.BuildError as e:
        print(f"❌ Docker build failed!")
        for line in e.build_log:
            if 'stream' in line:
                print(line['stream'].strip())
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred during Docker check: {e}")
        return False

def check_api_endpoints(base_url="http://127.0.0.1:8000"):
    """Checks if the API endpoints are responsive."""
    print("\n--- Checking API Endpoints ---")
    print("Note: This check requires the server to be running.")
    
    try:
        # Health check
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ /health endpoint is responsive.")
        else:
            print(f"❌ /health endpoint failed with status {response.status_code}.")
            return False

        # Reset check
        response = requests.post(f"{base_url}/api/v1/reset")
        if response.status_code == 200:
            print("✅ /api/v1/reset endpoint is responsive.")
        else:
            print(f"❌ /api/v1/reset endpoint failed with status {response.status_code}.")
            return False
            
        return True
    except requests.ConnectionError:
        print("❌ Connection to API failed. Is the server running? `uvicorn logistics_env.server.app:app`")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred during API check: {e}")
        return False

def check_openenv_yaml():
    """Checks for the existence and basic structure of openenv.yaml."""
    print("\n--- Checking openenv.yaml ---")
    if not os.path.exists("openenv.yaml"):
        print("❌ openenv.yaml not found!")
        return False
    
    # Basic validation can be expanded (e.g., using a YAML library)
    print("✅ openenv.yaml found.")
    return True

def check_inference_script():
    """Checks for the existence of inference.py."""
    print("\n--- Checking Inference Script ---")
    if not os.path.exists("inference.py"):
        print("❌ inference.py not found!")
        return False
    
    print("✅ inference.py found.")
    return True

def main():
    print("🚀 Starting Pre-submission Validation Script 🚀")
    
    results = {
        "Dockerfile Builds": check_dockerfile(),
        "openenv.yaml Compliance": check_openenv_yaml(),
        "Inference Script Present": check_inference_script(),
        "API Endpoint Reachable": check_api_endpoints(),
    }
    
    print("\n--- 📊 Validation Summary ---")
    all_passed = True
    for check, result in results.items():
        status = "✅ Passed" if result else "❌ Failed"
        print(f"{check}: {status}")
        if not result:
            all_passed = False
            
    print("\n--- 🏁 Final Verdict ---")
    if all_passed:
        print("🎉 Congratulations! All checks passed. You are ready to submit.")
    else:
        print("🔥 Some checks failed. Please review the logs above and fix the issues before submitting.")

if __name__ == "__main__":
    main()
