# Traffic AI — Smart Signal Control System

## Overview
This project uses Reinforcement Learning (PPO) to dynamically control traffic signals and prioritize emergency vehicles in real-time.

## Features
- Adaptive traffic signal control
- Emergency vehicle (ambulance) prioritization
- Real-time dashboard visualization
- SUMO simulation integration
- Live deployment via ngrok

## Tech Stack
- Python (FastAPI, Stable-Baselines3)
- SUMO (Traffic Simulation)
- Reinforcement Learning (PPO)
- HTML Dashboard (WebSocket-based)

## Architecture
Frontend (Dashboard) → Backend (FastAPI) → SUMO → RL Model

## Live Demo

Backend API:
https://nikita-recidivous-engagedly.ngrok-free.dev/state

## Architecture

Dashboard (HTML + JS)
        ↓
FastAPI Backend (WebSocket)
        ↓
SUMO Simulation (Traffic)
        ↓
PPO Model (Decision Making)

Dashboard:
Open `dashboard.html` locally or hosted version.

## Team
- Ishhan Goyal — AI + Backend
- Kirti Kashyap — Backend
- Ishika Bisht — Frontednd 

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

## 2. Start backend
python backend1.py

## 3. Run ngrok
Run ngrok

OPen dashboard in browser

---
