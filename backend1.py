from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import threading
import asyncio
import json
import time
import traci
from stable_baselines3 import PPO
from train import SingleIntersectionEnv
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Paste your coords from get_coords.py here ──────────────
# ── Coordinates ───────────────────────────────────────────
# Real GPS center of Meerut intersection (from get_coords.py)
REAL_LAT = 28.97481   # your actual output
REAL_LNG = 77.69610   # your actual output

# SUMO network center (from find_center.py output)
SUMO_CENTER_X = 147.25   # replace with find_center.py output
SUMO_CENTER_Y = 147.25   # replace with find_center.py output

# Scale: how many degrees per SUMO meter
# Earth at 29°N: 1 degree lat ≈ 111,000m, 1 degree lng ≈ 97,000m
SCALE_LAT = 1 / 111000
SCALE_LNG = 1 / 97000

def sumo_to_latlng(x, y):
    lat = REAL_LAT + (y - SUMO_CENTER_Y) * SCALE_LAT
    lng = REAL_LNG + (x - SUMO_CENTER_X) * SCALE_LNG
    return round(lat, 7), round(lng, 7)
# ───────────────────────────────────────────────────────────

PHASES = {
    0: "🟢 N-S Green",
    1: "🟡 N-S Yellow",
    2: "🟢 E-W Green",
    3: "🟡 E-W Yellow"
}

state = {
    "running":          False,
    "step":             0,
    "vehicles":         0,
    "ambulance_active": False,
    "ambulance_road":   "",
    "ambulance_speed":  0.0,
    "reward":           0.0,
    "total_reward":     0.0,
    "signal_phase":     0,
    "phase_name":       "—",
    "reward_history":   [],
    "vehicle_history":  [],
    "ambulance_log":    [],
    "vehicle_positions":  [],
    "intersection_lat": REAL_LAT,
    "intersection_lng": REAL_LNG,
}

connected_clients = []
sim_thread = None


def run_simulation():
    model = PPO.load("ppo_traffic2")
    env   = SingleIntersectionEnv(use_gui=False)
    obs, _ = env.reset()
    done   = False

    while not done and state["running"]:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = env.step(action)

        vehicles   = traci.vehicle.getIDList()
        ambulances = [v for v in vehicles if "ambulance" in v]
        phase      = traci.trafficlight.getPhase(env.ts_id)

        # Build vehicle positions for map
        positions = []
        for vid in vehicles:
            try:
                x, y     = traci.vehicle.getPosition(vid)
                lat, lng = sumo_to_latlng(x, y)
                speed    = round(traci.vehicle.getSpeed(vid), 1)
                positions.append({
                    "id":           vid,
                    "lat":          lat,
                    "lng":          lng,
                    "speed":        speed,
                    "is_ambulance": "ambulance" in vid
                })
            except Exception:
                pass
        time.sleep(0.09)  # control update rate (adjust as needed)

        # Update state
        state["step"]             += 1
        state["vehicles"]          = len(vehicles)
        state["reward"]            = round(float(reward), 4)
        state["total_reward"]      = round(state["total_reward"] + float(reward), 4)
        state["ambulance_active"]  = len(ambulances) > 0
        state["signal_phase"]      = phase
        state["phase_name"]        = PHASES.get(phase, str(phase))
        state["vehicle_positions"] = positions

        if ambulances:
            amb = ambulances[0]
            state["ambulance_road"]  = traci.vehicle.getRoadID(amb)
            state["ambulance_speed"] = round(traci.vehicle.getSpeed(amb), 1)
            entry = (
                f"Step {state['step']} | {amb} on "
                f"{state['ambulance_road']} @ {state['ambulance_speed']}m/s"
            )
            if not state["ambulance_log"] or state["ambulance_log"][0] != entry:
                state["ambulance_log"].insert(0, entry)
                state["ambulance_log"] = state["ambulance_log"][:20]

        state["reward_history"].append(round(float(reward), 4))
        state["vehicle_history"].append(len(vehicles))
        if len(state["reward_history"]) > 80:
            state["reward_history"].pop(0)
            state["vehicle_history"].pop(0)

    state["running"] = False
    env.close()


@app.post("/start")
def start():
    global sim_thread
    if not state["running"]:
        state.update({
            "running":           True,
            "step":              0,
            "total_reward":      0.0,
            "reward_history":    [],
            "vehicle_history":   [],
            "ambulance_log":     [],
            "vehicle_positions": [],
            "ambulance_active":  False,
            "ambulance_road":    "",
            "ambulance_speed":   0.0,
        })
        sim_thread = threading.Thread(target=run_simulation, daemon=True)
        sim_thread.start()
    return {"status": "started"}


@app.post("/stop")
def stop():
    state["running"] = False
    return {"status": "stopped"}


@app.get("/state")
def get_state():
    return state


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.send_text(json.dumps(state))
            await asyncio.sleep(0.15)   # ~6 updates per second
    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
    except Exception:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)