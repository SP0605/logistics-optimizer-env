step_count = 0
MAX_STEPS = 10
from fastapi import APIRouter
from logistics_env.env.environment import LogisticsEnv

router = APIRouter()

# Create global environment
env = LogisticsEnv(task_level="medium")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/api/v1/reset")
def reset():
    global step_count
    step_count = 0

    obs, info = env.reset()

    return {
        "observation": str(obs),
        "info": str(info)
    }


@router.post("/api/v1/step")
def step(action: dict):
    global step_count
    step_count += 1

    obs, reward, terminated, truncated, info = env.step(action)

    # 🔥 FORCE STOP
    if step_count >= MAX_STEPS:
        truncated = True

    return {
        "observation": str(obs),
        "reward": float(reward),
        "terminated": bool(terminated),
        "truncated": bool(truncated),
        "info": str(info)
    }


@router.get("/api/v1/state")
def state():
    return env.state()