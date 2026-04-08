---
title: Logistics Optimizer Env
emoji: 🚚
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# 🚚 Logistics Optimizer Environment

This is a Gymnasium-based RL environment for last-mile logistics optimization. The agent must manage vehicle capacity, delivery deadlines, and dynamic orders to maximize efficiency and on-time deliveries.

---

## 📦 Environment Description

The agent controls a single vehicle to pick up and deliver packages in a 2D grid world. The goal is to maximize the total reward by delivering packages as quickly as possible while respecting constraints.

---

## 🎮 Action and Observation Space

### 🔹 Action Space

The action space is a dictionary with two keys:

- **action_type**:
  - `0` → Pick up an order  
  - `1` → Deliver an order  
  - `2` → Wait  

- **order_id**:
  - The ID of the order to interact with

---

### 🔹 Observation Space

The observation is a dictionary representing the current state of the environment, including:

- `orders` → List of all orders  
- `current_location` → Vehicle coordinates  
- `current_time` → Current time step  
- `current_payload` → Orders currently in vehicle  

---

## 🧩 Tasks

The environment includes three tasks of increasing difficulty:

- **Easy**  
  Single package delivery with no constraints. Focus on shortest path.

- **Medium**  
  Multiple packages with capacity constraint. Requires optimized delivery sequence.

- **Hard**  
  Multiple packages with deadlines, priorities, and dynamic orders. Requires balancing multiple objectives.

---

## 📊 Baseline Scores

Baseline performance can be generated using the `inference.py` script.

---