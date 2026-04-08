import gymnasium as gym
import numpy as np
from typing import Dict, Any, List

class Order:
    def __init__(self, id, pickup_location, delivery_location, time_window):
        self.id = id
        self.pickup_location = pickup_location
        self.delivery_location = delivery_location
        self.time_window = time_window
        self.delivered = False
        self.picked_up = False

class State:
    def __init__(self):
        self.orders = []
        self.current_location = np.array([0, 0])
        self.current_time = 0
        self.current_payload = []

class LogisticsEnv(gym.Env):
    def __init__(self, task_level="medium"):
        super().__init__()
        self.task_level = task_level
        self.action_space = gym.spaces.Dict({
            "action_type": gym.spaces.Discrete(3),  # 0: pickup, 1: deliver, 2: wait
            "order_id": gym.spaces.Discrete(10)  # Assume up to 10 orders
        })
        self.observation_space = gym.spaces.Dict({
            "orders": gym.spaces.Sequence(gym.spaces.Dict({
                "id": gym.spaces.Discrete(10),
                "pickup_location": gym.spaces.Box(low=0, high=100, shape=(2,)),
                "delivery_location": gym.spaces.Box(low=0, high=100, shape=(2,)),
                "time_window": gym.spaces.Box(low=0, high=100, shape=(2,)),
                "delivered": gym.spaces.Discrete(2),
                "picked_up": gym.spaces.Discrete(2),
            })),
            "current_location": gym.spaces.Box(low=0, high=100, shape=(2,)),
            "current_time": gym.spaces.Box(low=0, high=100, shape=(1,)),
            "current_payload": gym.spaces.Sequence(gym.spaces.Discrete(10)),
        })
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = State()
        self.state.orders = [
            Order(1, np.array([10, 10]), np.array([20, 20]), np.array([0, 50])),
            Order(2, np.array([30, 30]), np.array([40, 40]), np.array([0, 50])),
        ]
        self.invalid_actions = 0
        obs = self._get_observation()
        info = {"invalid_actions": self.invalid_actions}
        return obs, info

    def step(self, action):
        action_type = action["action_type"]
        order_id = action["order_id"]
        
        reward = 0
        terminated = False
        truncated = False
        
        if action_type == 0:  # pickup
            order = next((o for o in self.state.orders if o.id == order_id), None)
            if order is None or order.picked_up or order.delivered:
                self.invalid_actions += 1
                reward = -1
            else:
                order.picked_up = True
                self.state.current_payload.append(order)
                reward = 1
        elif action_type == 1:  # deliver
            order = next((o for o in self.state.current_payload if o.id == order_id), None)
            if order is None:
                self.invalid_actions += 1
                reward = -1
            else:
                order.delivered = True
                self.state.current_payload.remove(order)
                reward = 10
        elif action_type == 2:  # wait
            reward = 0
        
        obs = self._get_observation()
        info = {"invalid_actions": self.invalid_actions}
        return obs, reward, terminated, truncated, info

    def _get_observation(self):
        return {
            "orders": self.state.orders,
            "current_location": self.state.current_location,
            "current_time": self.state.current_time,
            "current_payload": self.state.current_payload,
        }