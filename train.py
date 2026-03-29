import gymnasium as gym
import numpy as np
import traci
import sumo_rl
from stable_baselines3 import PPO
from gymnasium import spaces


class SingleIntersectionEnv(gym.Env):
    def __init__(self, use_gui=True):
        super().__init__()

        self.env = sumo_rl.SumoEnvironment(
            net_file="nets/single-intersection/single-intersection.net.xml",
            route_file="nets/single-intersection/single-intersection.rou.xml",
            use_gui=use_gui,
            num_seconds=100000,    
            min_green=5,
            delta_time=5
            )

        self.ts_id = self.env.ts_ids[0]
        self.action_space = self.env.action_space

        obs_size = self.env.observation_space.shape[0]
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(obs_size + 1,), dtype=np.float32
        )

        self.step_count = 0

    def _get_obs(self, raw_obs):
        amb_feature = 0.0
        vehicles = traci.vehicle.getIDList()
        for v in vehicles:
            if "ambulance" in v:
                pos = traci.vehicle.getLanePosition(v)
                lane_len = traci.lane.getLength(traci.vehicle.getLaneID(v))
                amb_feature = pos / max(lane_len, 1.0)
                break
        return np.append(raw_obs, amb_feature).astype(np.float32)

    def reset(self, seed=None, options=None):
        result = self.env.reset()
        obs = result[0] if isinstance(result, tuple) else result
        self.step_count = 0
        raw_obs = obs[self.ts_id] if isinstance(obs, dict) else obs
        return self._get_obs(raw_obs), {}

    def step(self, action):                          # indented inside class
        self.step_count += 1

        # Spawn ambulance every 200 steps
        if self.step_count % 200 == 0:
            amb_id = f"ambulance_{self.step_count}"
            try:
                traci.vehicle.add(
                    vehID=amb_id,
                    routeID="route_ns",
                    typeID="DEFAULT_VEHTYPE",
                    departSpeed="5",
                    departLane="best"
                )
                traci.vehicle.setColor(amb_id, (255, 0, 0, 255))
                traci.vehicle.setLength(amb_id, 8.0)
                traci.vehicle.setMaxSpeed(amb_id, 15.0)
                traci.vehicle.setSpeedMode(amb_id, 0)
                print(f"🚑 Ambulance {amb_id} spawned!")
            except Exception as e:
                print(f"Spawn error: {e}")

        # Priority override for any ambulance
        if any("ambulance" in v for v in traci.vehicle.getIDList()):
            action = 0
            print("🚑 PRIORITY MODE — signal forced green!")

        result = self.env.step({self.ts_id: int(action)})

        if len(result) == 5:
            obs, reward, terminated, truncated, info = result
        else:
            obs, reward, done, info = result
            terminated = done
            truncated = False

        raw_obs = obs[self.ts_id] if isinstance(obs, dict) else obs
        reward_val = reward[self.ts_id] if isinstance(reward, dict) else reward
        done_flag = terminated if isinstance(terminated, bool) else terminated.get("__all__", False)

        return self._get_obs(raw_obs), float(reward_val), done_flag, truncated, info

    def close(self):                                 # indented inside class
        self.env.close()


if __name__ == "__main__":
    print("Training PPO...")

    env = SingleIntersectionEnv(use_gui=False)      # no GUI for faster training

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        n_steps=512,
        batch_size=64
    )

    model.learn(total_timesteps=15000)
    model.save("ppo_traffic2")
    env.close()
    print("✅ Model saved!")