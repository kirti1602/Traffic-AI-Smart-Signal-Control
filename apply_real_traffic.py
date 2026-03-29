import json
from datetime import datetime

with open("traffic_profiles.json") as f:
    profiles = json.load(f)

# Detect current time period
hour = datetime.now().hour
current_profile = None
current_name = None

for name, data in profiles.items():
    if hour in list(data["hours"]):
        current_profile = data
        current_name = name
        break

if not current_profile:
    current_profile = profiles["afternoon"]
    current_name = "afternoon"

p_main  = current_profile["prob_main"]
p_cross = current_profile["prob_cross"]

print(f"Current hour: {hour}:00 → Profile: {current_name}")
print(f"Main road flow:  {p_main} prob/s ({int(p_main*3600)} vehicles/hour)")
print(f"Cross road flow: {p_cross} prob/s ({int(p_cross*3600)} vehicles/hour)")

# Write calibrated .rou.xml
rou_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<routes>
    <!-- Generated from real Indian traffic data (IRC SP-41, HCM India 2017) -->
    <!-- Profile: {current_name} | Hour: {hour}:00 -->
    
    <route id="route_ns" edges="n_t t_s"/>
    <route id="route_we" edges="w_t t_e"/>

    <!-- Main corridor (N-S): {int(p_main*3600)} vehicles/hour -->
    <flow id="flow_ns" route="route_ns" begin="0" end="100000"
          probability="{p_main}" departSpeed="max"
          departPos="base" departLane="best"/>

    <!-- Cross road (E-W): {int(p_cross*3600)} vehicles/hour -->
    <flow id="flow_we" route="route_we" begin="0" end="100000"
          probability="{p_cross}" departSpeed="max"
          departPos="base" departLane="best"/>
</routes>"""

with open("nets/single-intersection/single-intersection.rou.xml", "w") as f:
    f.write(rou_xml)

print("✅ Updated single-intersection.rou.xml with real traffic calibration")