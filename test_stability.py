from logistics_env.env.environment import LogisticsEnv
import numpy as np

# Test with a dict action, like SB3 would send
env = LogisticsEnv(task_level="medium")
obs, info = env.reset(seed=42)
print("Initial state loaded. Observation keys:", obs.keys())

# Test invalid pickup (order doesn't exist)
action_pickup = {"action_type": 0, "order_id": 99} # 0 = pickup_order
obs, rew, term, trunc, info = env.step(action_pickup)
print(f"Invalid Pickup - Reward: {rew}, Invalid Count: {info['invalid_actions']}, Term: {term}, Trunc: {trunc}")
assert info['invalid_actions'] == 1

# Test invalid deliver (order not picked up)
action_deliver = {"action_type": 1, "order_id": 1} # 1 = deliver_order
obs, rew, term, trunc, info = env.step(action_deliver)
print(f"Invalid Deliver - Reward: {rew}, Invalid Count: {info['invalid_actions']}, Term: {term}, Trunc: {trunc}")
assert info['invalid_actions'] == 2

# Test valid pickup
action_pickup_valid = {"action_type": 0, "order_id": 1}
obs, rew, term, trunc, info = env.step(action_pickup_valid)
print(f"Valid Pickup - Reward: {rew}, Invalid Count: {info['invalid_actions']}, Term: {term}, Trunc: {trunc}")
assert info['invalid_actions'] == 2 # No new invalid actions
assert any(o.id == 1 for o in env.state.current_payload), "Order 1 should be in payload"

# Test valid deliver
action_deliver_valid = {"action_type": 1, "order_id": 1}
obs, rew, term, trunc, info = env.step(action_deliver_valid)
print(f"Valid Deliver - Reward: {rew}, Invalid Count: {info['invalid_actions']}, Term: {term}, Trunc: {trunc}")
assert info['invalid_actions'] == 2 # No new invalid actions
assert not any(o.id == 1 for o in env.state.current_payload), "Order 1 should not be in payload"
assert env.state.orders[0].delivered, "Order 1 should be marked as delivered"


print("\nTest complete - no crashes = success")
