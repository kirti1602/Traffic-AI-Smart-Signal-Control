# TrafficAI — Autonomous Traffic Control System

A multi-agent AI system that dynamically controls urban traffic signals and prioritizes emergency vehicles using Reinforcement Learning.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://kirti1602.github.io/Traffic-AI-Smart-Signal-Control/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Overview

Urban traffic signal systems operate on fixed timing schedules that fail to adapt to real-time conditions — leading to unnecessary congestion, increased emissions, and delayed emergency response times. TrafficAI addresses this by deploying a Proximal Policy Optimization (PPO) agent that continuously observes intersection state and makes adaptive signal control decisions.

The system is built on top of SUMO (Simulation of Urban MObility), a microscopic traffic simulator, and communicates with it via the TraCI API. A FastAPI backend streams simulation state over WebSockets to a live dashboard.

**Live Dashboard:** [https://kirti1602.github.io/Traffic-AI-Smart-Signal-Control/](https://kirti1602.github.io/Traffic-AI-Smart-Signal-Control/)

**Live API:** [https://nikita-recidivous-engagedly.ngrok-free.dev/state](https://nikita-recidivous-engagedly.ngrok-free.dev/state)

---

## Key Features

- **Adaptive Signal Control** — A PPO-trained reinforcement learning agent dynamically adjusts signal phases based on real-time queue lengths and vehicle wait times, replacing fixed-cycle timing.
- **Emergency Vehicle Prioritization** — The system monitors all active vehicle IDs via TraCI at every simulation step. Upon detecting an emergency vehicle, it immediately overrides the RL agent's action and forces a green phase on the relevant lane.
- **Real-Time Dashboard** — A WebSocket-connected frontend visualizes live signal states, vehicle counts, and performance metrics as the simulation runs.
- **SUMO Simulation Backend** — Microscopic traffic simulation with configurable vehicle flows, multi-lane road networks, and realistic vehicle dynamics.

---

## Architecture

```
Dashboard (HTML + JavaScript)
            |
            | WebSocket
            |
    FastAPI Backend
            |
            | TraCI API
            |
    SUMO Traffic Simulation
            |
            |
    PPO Model (Stable-Baselines3)
```

The RL model observes the environment state (lane queue lengths, current phase, elapsed phase time) and outputs a signal phase action. The FastAPI server runs the simulation loop, applies the model's decisions, handles emergency overrides, and broadcasts state updates to all connected dashboard clients over WebSocket.

---

## Tech Stack

| Component | Technology |
|---|---|
| Traffic Simulation | SUMO 1.26, TraCI |
| Reinforcement Learning | PPO, Stable-Baselines3 |
| Backend | FastAPI, WebSockets, Python 3.12 |
| Frontend | HTML, CSS, JavaScript |
| Deployment | GitHub Pages, ngrok |

---

## Results

| Metric | Fixed-Time Control | PPO Agent |
|---|---|---|
| Average Wait Time | ~45s | ~28s |
| Emergency Response | No priority | Immediate override |
| Vehicle Throughput | Baseline | +35% improvement |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- SUMO installed — [Installation Guide](https://sumo.dlr.de/docs/Installing/index.html)
- `SUMO_HOME` environment variable set
- ngrok (optional, for remote API access)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/kirti1602/Traffic-AI-Smart-Signal-Control.git
cd Traffic-AI-Smart-Signal-Control
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Set SUMO_HOME (Windows)**
```bash
set SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo
```

**4. Set SUMO_HOME (Linux / macOS)**
```bash
export SUMO_HOME=/usr/share/sumo
```

### Running the System

**Start the backend server**
```bash
python backend1.py
```

**Expose the API via ngrok (optional)**
```bash
ngrok http 8000
```

**Open the dashboard**

Open `dashboard.html` in your browser, or visit the deployed version at [https://kirti1602.github.io/Traffic-AI-Smart-Signal-Control/](https://kirti1602.github.io/Traffic-AI-Smart-Signal-Control/).

---

## Project Structure

```
Traffic-AI-Smart-Signal-Control/
├── nets/
│   └── single-intersection/
│       ├── single-intersection.net.xml      # Road network definition
│       ├── single-intersection.rou.xml      # Vehicle routes and flows
│       ├── single-intersection.edg.xml      # Edge definitions
│       └── single-intersection.sumocfg      # SUMO configuration
├── backend1.py                              # FastAPI server and simulation loop
├── run_simulation.py                        # Standalone simulation runner
├── dashboard.html                           # Frontend dashboard
├── requirements.txt
└── README.md
```

---

## How It Works

**State Representation**
At each decision step, the agent receives an observation vector containing the number of vehicles queued on each lane, the current signal phase, and the time elapsed since the last phase change.

**Action Space**
The agent selects from the available signal phases at the intersection. Each action activates a specific combination of green and red signals across the four lanes.

**Reward Function**
The agent is penalized proportionally to the total accumulated wait time across all vehicles in the simulation. This incentivizes it to minimize congestion globally rather than optimizing for any single lane.

**Emergency Override**
At every simulation step, the system queries TraCI for the list of active vehicle IDs. If any vehicle ID contains the identifier `ambulance`, the system bypasses the RL agent's output and directly sets the traffic light phase to green on the ambulance's approaching lane using `traci.trafficlight.setPhase()`.

---

## Contributors

| Name | Contribution |
|---|---|
| Ishhan Goyal | Reinforcement learning model, backend integration |
| Kirti Kashyap | Backend development, SUMO simulation setup |
| Ishika Bisht | Frontend dashboard, WebSocket integration |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
