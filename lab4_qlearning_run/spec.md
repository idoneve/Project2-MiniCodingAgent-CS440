# spec.md — Lab 4 solved with Q-learning (Lab 5 requirements)

## Goal

Implement a Q-learning vacuum robot for the Lab 4 environment. The robot
does not know the transitions or rewards ahead of time; it learns them by
trial and error and must end up with a greedy policy that reaches the +10
cell from the start.

## Environment (given, do not modify)

`agent_strategy4.py` from Lab 4 provides `INITIAL_GRID`, `VacuumEnvironment`
and `ACTION_DELTAS`.

    start  0   0   0
      0    X   0   0
      0    0   0   0
      0   -1   0  10

- start = (0,0), wall X = (1,1), penalty -1 = (3,1), goal +10 = (3,3)
- moves: UP, DOWN, LEFT, RIGHT (deterministic)

## Files to create

- `qLearning_Agent.py` — class `QLearningAgent` (epsilon-greedy Q-learning)
- `trainVacuum.py` — function `trainVacuum(...)` that trains and returns the agent

Use only the Python standard library.

## Hyperparameters (Lab 5)

| Name | Value |
|------|-------|
| living reward | -0.04 |
| learning rate (alpha) | 0.1 |
| discount factor (gamma) | 0.9 |
| epsilon | 0.1 |
| episodes | 1000 (max 100 steps each) |

## Acceptance

- `python -m pytest -q Test/test_qlearning.py Test/test_strategy4.py` passes.
- The evaluation script reports that the greedy policy reaches +10.
