from fastapi import FastAPI
from logistics_env.env.environment import LogisticsEnv

app = FastAPI()

env = LogisticsEnv(task_level="medium")

step_count = 0
MAX_STEPS = 10


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/reset")
def reset():
    global step_count
    step_count = 0

    obs, info = env.reset()

    return {
        "observation": str(obs),
        "info": str(info)
    }


@app.post("/api/v1/step")
def step(action: dict):
    global step_count
    step_count += 1

    obs, reward, terminated, truncated, info = env.step(action)

    if step_count >= MAX_STEPS:
        truncated = True

    return {
        "observation": str(obs),
        "reward": float(reward),
        "terminated": bool(terminated),
        "truncated": bool(truncated),
        "info": str(info)
    }


@app.get("/")
def root():
    return {"message": "API running"}


#extra 2 endpoints
@app.post("/reset")
def reset_root():
    return reset()


@app.post("/step")
def step_root(action: dict):
    return step(action)