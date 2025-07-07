# === Imports ===
import os
import pickle
from datetime import datetime

import gymnasium as gym
import gym_tictactoe
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

from ai.agent import TicTacToeAgent

# === Hyperparameters ===
learning_rate = 0.1
n_episodes = 500
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 1.5)
final_epsilon = 0.1

# === Environment ===
env = gym.make("gym_tictactoe/TicTacToe-v0", render_mode="human")
env = gym.wrappers.RecordEpisodeStatistics(env)
env.return_queue.clear()
env.length_queue.clear()

# === Load or Train Agent ===
model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(model_dir, exist_ok=True)

existing_models = sorted(f for f in os.listdir(model_dir) if f.startswith("q_table_") and f.endswith(".pkl"))
q_values = None

if existing_models:
    print("Available saved agents:")
    for i, fname in enumerate(existing_models):
        print(f"[{i}] {fname}")
    choice = input("Enter the number of a model to load, or press Enter to train a new one: ").strip()
    if choice.isdigit() and int(choice) < len(existing_models):
        with open(os.path.join(model_dir, existing_models[int(choice)]), "rb") as f:
            q_values = pickle.load(f)
        print(f"Loaded model: {existing_models[int(choice)]}")
    else:
        print("Invalid choice. Training new agent.")
else:
    print("No models found. Training new agent...")

# === Agent ===
agent = TicTacToeAgent(
    env,
    learning_rate=learning_rate,
    intial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
    q_table=q_values,
)
ai_player = 1
current_player = 1

# === Training ===
wins = losses = draws = 0
for episode in tqdm(range(n_episodes), desc="Training Episodes"):
    obs, _ = env.reset()
    done = False
    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, _ = env.step(action)

        if reward == 1.0 and current_player == ai_player:
            wins += 1
        elif reward == -1.0 and current_player == ai_player:
            losses += 1
        elif reward == 0.5:
            draws += 1
        current_player = 3 - current_player
        agent.update(obs, action, reward, terminated, next_obs)
        obs = next_obs
        done = terminated or truncated
    agent.decay_epsilon()

# === Save Q-table ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
model_path = os.path.join(model_dir, f"q_table_{timestamp}.pkl")
with open(model_path, "wb") as f:
    pickle.dump(agent.q_values, f)
print(f"\nSaved model: {model_path}")
print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")

# === Plotting ===
def get_moving_avgs(arr, window, mode):
    return np.convolve(np.array(arr).flatten(), np.ones(window), mode=mode) / window

rolling_length = 500
fig, axs = plt.subplots(ncols=3, figsize=(15, 5))

# Rewards
axs[0].set_title("Episode Rewards")
reward_moving_avg = get_moving_avgs(env.return_queue, rolling_length, "valid")
axs[0].plot(reward_moving_avg)
axs[0].set_xlabel("Episode")
axs[0].set_ylabel("Reward")

# Episode Length
axs[1].set_title("Episode Length")
length_moving_avg = get_moving_avgs(env.length_queue, rolling_length, "valid")
axs[1].plot(length_moving_avg)
axs[1].set_xlabel("Episode")
axs[1].set_ylabel("Length")

# Training Error
axs[2].set_title("Training Error")
training_error_moving_avg = get_moving_avgs(agent.training_error, rolling_length, "same")
axs[2].plot(training_error_moving_avg)
axs[2].set_xlabel("Episode")
axs[2].set_ylabel("TD Error")

plt.tight_layout()
plt.show()
