import osmnx as ox
import json

# Pull actual Meerut road network
print("Fetching Meerut road network from OpenStreetMap...")
G = ox.graph_from_place("Meerut, Uttar Pradesh, India", network_type="drive")

# Get all major intersections (4+ roads meeting)
nodes, edges = ox.graph_to_gdfs(G)
major = nodes[nodes["street_count"] >= 4]

print(f"Found {len(major)} major intersections in Meerut")
print(major[["street_count"]].head(10))

# Real traffic flow data from published Indian studies:
# Source: IRC (Indian Roads Congress) SP-41, HCM India 2017
# Peak hour volume for a medium city intersection = 800-1200 PCU/hour
# Off-peak = 300-500 PCU/hour
# Night = 50-150 PCU/hour

# Convert PCU/hour to SUMO probability per second:
# probability = vehicles_per_hour / 3600
TRAFFIC_PROFILES = {
    "morning_peak":   {"hours": range(8, 11),  "prob_main": 0.28, "prob_cross": 0.18},
    "afternoon":      {"hours": range(11, 17), "prob_main": 0.15, "prob_cross": 0.10},
    "evening_peak":   {"hours": range(17, 21), "prob_main": 0.32, "prob_cross": 0.22},
    "night":          {"hours": range(21, 24), "prob_main": 0.04, "prob_cross": 0.03},
    "early_morning":  {"hours": range(0, 8),   "prob_main": 0.03, "prob_cross": 0.02},
}

# Save profiles
with open("traffic_profiles.json", "w") as f:
    json.dump(TRAFFIC_PROFILES, f, indent=2, default=list)

print("✅ Saved traffic_profiles.json")
print("\nTraffic flow summary (vehicles/hour):")
for name, p in TRAFFIC_PROFILES.items():
    main_vph  = int(p["prob_main"]  * 3600)
    cross_vph = int(p["prob_cross"] * 3600)
    print(f"  {name:20s}: Main road {main_vph} v/h, Cross road {cross_vph} v/h")