import time
import numpy as np
import traci
from stable_baselines3 import PPO
from train import SingleIntersectionEnv

print("🎬 Loading trained model...")
model = PPO.load("ppo_traffic2")

env = SingleIntersectionEnv(use_gui=True)
obs, _ = env.reset()
done = False
step = 0
total_reward = 0.0

print("🚦 Running demo — watch the SUMO GUI!")
print("-" * 40)

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    total_reward += reward
    step += 1

    vehicles = traci.vehicle.getIDList()
    ambulances = [v for v in vehicles if "ambulance" in v]

    if ambulances:
        time.sleep(0.3)   # slow down so you can see it
        for amb in ambulances:
            amb_speed = traci.vehicle.getSpeed(amb)
            amb_road  = traci.vehicle.getRoadID(amb)
            amb_pos   = traci.vehicle.getLanePosition(amb)
            # follow it with camera
            amb_x, amb_y = traci.vehicle.getPosition(amb)
            traci.gui.setZoom("View #0", 500)
            traci.gui.setOffset("View #0", amb_x, amb_y)
            print(f"  🚨 {amb} | road={amb_road} pos={amb_pos:.0f}m speed={amb_speed:.1f}m/s | 🟢 GREEN")
    else:
        time.sleep(0.05)

    if step % 100 == 0:
        print(f"Step {step:4d} | Vehicles: {len(vehicles):3d} | Reward: {reward:+.3f} | Total: {total_reward:+.2f}")

print("-" * 40)
print(f"✅ Demo complete! Steps: {step} | Total reward: {total_reward:.2f}")
input("Press Enter to close...")
env.close()