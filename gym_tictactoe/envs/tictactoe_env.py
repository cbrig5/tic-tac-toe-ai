import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np


class TicTacToeEnv(gym.Env):
    metadata = {"render_modes": ["human", "ansi"], "render_fps": 4}

    def __init__(self, render_mode=None, size=3):
        self.size = size
        self.total_cells = size * size
        self.window_size = 600
        self.observation_space = spaces.MultiDiscrete([3] * self.total_cells)
        self.board = [''] * self.total_cells
        self.current_player = 1
        self.done = False
        # We have one action for each cell in the tic-tac-toe board
        self.action_space = spaces.Discrete(self.total_cells)
  

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None


    def _get_obs(self):
        mapping = {'X': 1, 'O': 2, '': 0}
        encoded = [mapping[mark] for mark in self.board]
        return np.array(encoded, dtype=np.int8)
    
    def _get_info(self):    
        info = {
            "current_player": self.current_player,
        }
        winner = self.check_winner()
        if winner:
            info["winner"] = winner
            winning_combos = [
                (0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)
            ]
            for combo in winning_combos:
                i, j, k = combo
                if self.board[i] == self.board[j] == self.board[k] != '':
                    info["winning_combo"] = combo
                    break
        return info

    def get_mark(self):
        return 'X' if self.current_player == 1 else 'O'

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.board = [''] * self.total_cells
        self.current_player = 1
        self.done = False
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self, action):
        if self.done or self.board[action] != '':
            return self._get_obs(), -10, False, False, self._get_info()
        
        mark = self.get_mark()

        self.board[action] = mark
        winner = self.check_winner()
        if winner:
            self.done = True
            reward = 1.0 if winner == mark else -1.0
        elif winner == 0:
            self.done = True
            reward = 0.5
        else:
            self.done = False
            reward = 0.0
            self.current_player = 3 - self.current_player
        
        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), reward, self.done, False, self._get_info()

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for i,j,k in winning_combinations:
            if self.board[i] == self.board[j] == self.board[k] and self.board[k] != '':
                return self.board[i]
        if '' not in self.board:
            return 0
        return None

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        cell_size = self.window_size / self.size

        # Draw grid lines
        for i in range(1, self.size):
            pygame.draw.line(canvas, (0, 0, 0), (0, i * cell_size), (self.window_size, i * cell_size), 4)
            pygame.draw.line(canvas, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.window_size), 4)

        # Draw Xs and Os
        for row in range(self.size):
            for col in range(self.size):
                index = row * self.size + col
                mark = self.board[index]
                center = (int(col * cell_size + cell_size / 2), int(row * cell_size + cell_size / 2))

                if mark == 'X':
                    offset = cell_size / 3
                    pygame.draw.line(canvas, (0, 0, 0),
                                    (center[0] - offset, center[1] - offset),
                                    (center[0] + offset, center[1] + offset), 6)
                    pygame.draw.line(canvas, (0, 0, 0),
                                    (center[0] - offset, center[1] + offset),
                                    (center[0] + offset, center[1] - offset), 6)

                elif mark == 'O':
                    pygame.draw.circle(canvas, (0, 0, 0), center, int(cell_size / 3), 6)

        # Render
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata.get("render_fps", 30))
        else:  # rgb_array
            return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None