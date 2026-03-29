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
