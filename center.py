# find_center.py
import traci
import subprocess
import os

# Start SUMO briefly just to read network bounds
sumo_cmd = [
    "sumo",
    "-n", "nets/single-intersection/single-intersection.net.xml",
    "--no-step-log", "--duration-log.disable"
]

traci.start(sumo_cmd)
net_bounds = traci.simulation.getNetBoundary()
traci.close()

min_x, min_y = net_bounds[0]
max_x, max_y = net_bounds[1]
center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2

print(f"Network bounds: {net_bounds}")
print(f"SUMO center X: {center_x}")
print(f"SUMO center Y: {center_y}")
print(f"Set SUMO_CENTER_X = {center_x}")
print(f"Set SUMO_CENTER_Y = {center_y}")