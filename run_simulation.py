import time
import traci
import sumo_rl

env = sumo_rl.SumoEnvironment(
    net_file="nets/single-intersection/single-intersection.net.xml",
    route_file="nets/single-intersection/single-intersection.rou.xml",
    use_gui=True,
    num_seconds=10000,
    min_green=5,
    delta_time=5,
    sumo_warnings=False,
    # FIX 1: add this so vehicles actually appear in GUI
    render_mode="human"
)

# FIX 2: obs from reset() is a dict in multi-agent mode — don't unpack it
obs, info = env.reset()   # sumo-rl >= 1.4 returns (obs, info)
done = {"__all__": False}
step = 0

print("🚦 Simulation running!")

# FIX 3: check done correctly for multi-agent dict
while not done.get("__all__", False):
    # TraCI is safe to use AFTER reset()
    vehicles = traci.vehicle.getIDList()

    if vehicles:
        print(f"Step {step}: {len(vehicles)} vehicles on road")

    ambulance_present = any("ambulance" in v for v in vehicles)

    if ambulance_present:
        print(f"🚨 AMBULANCE DETECTED at step {step}!")
        action = {ts: 0 for ts in env.ts_ids}
    else:
        action = {ts: env.action_space.sample() for ts in env.ts_ids}

    obs, reward, terminated, truncated, info = env.step(action)
    
    # FIX 4: sumo-rl >= 1.4 uses terminated/truncated instead of done
    done = terminated

    step += 1
    time.sleep(0.05)

print("✅ Simulation complete!")
input("Press Enter to close...")
env.close()