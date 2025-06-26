from gymnasium.envs.registration import register

register(
    id="gym_tictactoe/TicTacToe-v0",
    entry_point="gym_tictactoe.envs.tictactoe_env:TicTacToeEnv",
    max_episode_steps=50,
)
