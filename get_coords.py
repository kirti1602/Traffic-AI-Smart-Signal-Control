# get_coords.py
import osmnx as ox

G = ox.graph_from_place("Meerut, Uttar Pradesh, India", network_type="drive")
nodes, edges = ox.graph_to_gdfs(G)
major = nodes[nodes["street_count"] >= 4]
busiest = major.sort_values("street_count", ascending=False).iloc[0]

print(f"REAL_LAT = {busiest.geometry.y}")
print(f"REAL_LNG = {busiest.geometry.x}")