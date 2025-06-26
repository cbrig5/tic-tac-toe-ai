from collections import defaultdict
import gymnasium as gym
import numpy as np



class DefaultQValues:
    def __init__(self, n_actions):
        self.n_actions = n_actions

    def __call__(self):
        return np.zeros(self.n_actions)

class TicTacToeAgent:

    def __init__(
        self,
        env: gym.Env,
        learning_rate: float,
        intial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
        q_table: dict = None,
    ):
        self.env = env
        self.q_values = defaultdict(DefaultQValues(env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = intial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []
        if q_table is not None:
            for obs_key, q_value in q_table.items():
                self.q_values[obs_key] = q_value
        else:
            for obs_key in self.q_values.keys():
                self.q_values[obs_key] = np.zeros(env.action_space.n)



    def get_action(self, obs: np.ndarray) -> int:
        obs_key = tuple(obs)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample() #explore
        else:
            q_values = self.q_values[obs_key]
            max_q_value = np.max(q_values)
            best_actions = np.flatnonzero(q_values == max_q_value)
            return int(np.random.choice(best_actions)) #exploit

    def update(
        self,
        obs: np.ndarray,
        action: int,
        reward: float,
        terminated: bool,
        next_obs: np.ndarray,
    ):
        obs_key = tuple(obs)
        next_obs_key = tuple(next_obs)
        future_q_value = (not terminated) * np.max(self.q_values[next_obs_key])
        temporal_difference = (reward + self.discount_factor * future_q_value - self.q_values[obs_key][action])
        self.q_values[obs_key][action] = (
            self.q_values[obs_key][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
