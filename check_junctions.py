# check_junctions.py
import traci

traci.start([
    "sumo",
    "-n", "nets/single-intersection/single-intersection.net.xml",
    "--no-step-log", "--duration-log.disable"
])

junctions = traci.junction.getIDList()
print(f"All junctions: {junctions}")

for jid in junctions:
    x, y = traci.junction.getPosition(jid)
    lng, lat = traci.simulation.convertGeo(x, y)
    print(f"  {jid}: SUMO({x:.1f}, {y:.1f}) → GPS({lat:.6f}, {lng:.6f})")

traci.close()