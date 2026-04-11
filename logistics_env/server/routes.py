from fastapi import APIRouter
from logistics_env.env.environment import LogisticsEnv

router = APIRouter()

env = LogisticsEnv(task_level="medium")

step_count = 0
MAX_STEPS = 10


@router.post("/reset")   # ✅ NO /api/v1
def reset():
    global step_count
    step_count = 0

    obs, info = env.reset()

    return {
        "observation": obs,
        "info": info
    }


@router.post("/step")   # ✅ NO /api/v1
def step(action: dict):
    global step_count
    step_count += 1

    obs, reward, terminated, truncated, info = env.step(action)

    if step_count >= MAX_STEPS:
        truncated = True

    return {
        "observation": obs,
        "reward": float(reward),
        "terminated": bool(terminated),
        "truncated": bool(truncated),
        "info": info
    }


@router.get("/state")
def state():
    return env.state()

# redeploy trigger #temporary comment