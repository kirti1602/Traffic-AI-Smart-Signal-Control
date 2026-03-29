import traci

# start SUMO with your actual config
traci.start(["sumo", "-c", "nets/single-intersection/single-intersection.sumocfg"])

lanes = traci.lane.getIDList()

xs, ys = [], []

for lane in lanes:
    try:
        shape = traci.lane.getShape(lane)
        for x, y in shape:
            xs.append(x)
            ys.append(y)
    except:
        pass

center_x = sum(xs) / len(xs)
center_y = sum(ys) / len(ys)

print("CENTER X:", center_x)
print("CENTER Y:", center_y)

traci.close()