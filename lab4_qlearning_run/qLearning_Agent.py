import random
from collections import defaultdict


class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.qtable = defaultdict(float)

    def chooseAction(self, state, validActions):
        if random.random() < self.epsilon:
            return random.choice(validActions)
        else:
            max_q = max(self.qtable[(state, a)] for a in validActions)
            best_actions = [a for a in validActions if self.qtable[(state, a)] == max_q]
            return random.choice(best_actions)

    def updateQVal(self, state, action, reward, nextState, nextActions):
        old_q = self.qtable[(state, action)]
        if nextActions:
            max_future_q = max(self.qtable[(nextState, a)] for a in nextActions)
        else:
            max_future_q = 0.0
        new_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
        self.qtable[(state, action)] = new_q

    def getActions(self, environment):
        actions = []
        for action, delta in ACTION_DELTAS.items():
            next_row = environment.pos[0] + delta[0]
            next_col = environment.pos[1] + delta[1]
            if 0 <= next_row < len(environment.grid) and 0 <= next_col < len(environment.grid[0]):
                cell = environment.grid[next_row][next_col]
                if cell != "X":
                    actions.append(action)
        return actions


ACTION_DELTAS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
