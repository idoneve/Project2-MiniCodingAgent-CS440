# qlearning-experiments — reference (Lab 5)

## Environment (already in the workspace, do not modify)

`agent_strategy4.py` provides:

```python
from agent_strategy4 import INITIAL_GRID, VacuumEnvironment, ACTION_DELTAS

INITIAL_GRID = [["start", 0, 0, 0],
                [0, "X", 0, 0],
                [0, 0, 0, 0],
                [0, -1, 0, 10]]
ACTION_DELTAS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

env = VacuumEnvironment(INITIAL_GRID)  # fresh copy of the grid
env.pos          # (row, col), starts at (0, 0)
env.grid         # list of lists, same layout as INITIAL_GRID
env.step(action) # moves the robot; moves into "X" or off the grid are ignored
```

The state is just `env.pos`. Goal = (3, 3).

## File 1: `qLearning_Agent.py`

```text
class QLearningAgent:
    __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1)
        self.alpha, self.gamma, self.epsilon  <- the three arguments
        self.qtable = collections.defaultdict(float)   # key: (state, action)

    chooseAction(self, state, validActions) -> action
        with probability epsilon: random.choice(validActions)
        otherwise: an action with the highest qtable value
                   (break ties with random.choice among the best)

    updateQVal(self, state, action, reward, nextState, nextActions)
        maxFutureQ = max(qtable[(nextState, a)] for a in nextActions), or 0 if nextActions is empty
        qtable[(state, action)] = old + alpha * (reward + gamma * maxFutureQ - old)

    getActions(self, environment) -> list of actions
        every action in ACTION_DELTAS whose next cell is inside the grid
        and is not "X" (use environment.pos and environment.grid)
```

## File 2: `trainVacuum.py`

```text
from agent_strategy4 import VacuumEnvironment, INITIAL_GRID
from qLearning_Agent import QLearningAgent

def trainVacuum(episodes=1000, living_reward=-0.04,
                learning_rate=0.1, discount_factor=0.9, epsilon=0.1) -> QLearningAgent
    agent = QLearningAgent(learning_rate, discount_factor, epsilon)
    for each episode:
        env = VacuumEnvironment(INITIAL_GRID); state = env.pos
        for at most 100 steps:
            action = agent.chooseAction(state, agent.getActions(env))
            env.step(action); nextState = env.pos
            reward = living_reward
            cell = env.grid[row][col] of nextState
            if cell is an int or float: reward += cell     # "start" adds nothing
            done = nextState == (3, 3)
            nextActions = [] if done else agent.getActions(env)
            agent.updateQVal(state, action, reward, nextState, nextActions)
            state = nextState
            if done: break
    return agent
```

## Team decisions from Lab 5 (keep them)

- Only +10 ends an episode. The -1 cell is a penalty the robot can pass
  through, not a terminal state.
- Moves are deterministic (no 80/10/10 slip).
- Defaults: living reward -0.04, alpha 0.1, gamma 0.9, epsilon 0.1,
  1000 episodes, at most 100 steps per episode.
