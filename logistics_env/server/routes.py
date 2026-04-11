from fastapi import APIRouter
from logistics_env.env.environment import LogisticsEnv

router = APIRouter()

step_count = 0
MAX_STEPS = 10

env = LogisticsEnv(task_level="medium")


@router.get("/health")
def health():
    return {"status": "ok"}


# ✅ FIXED (REMOVE /api/v1)
@router.post("/reset")
def reset():
    global step_count
    step_count = 0

    obs, info = env.reset()

    return {
        "observation": obs,
        "info": info
    }


# ✅ FIXED (REMOVE /api/v1)
@router.post("/step")
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


# ✅ FIXED (REMOVE /api/v1)
@router.get("/state")
def state():
    return env.state()