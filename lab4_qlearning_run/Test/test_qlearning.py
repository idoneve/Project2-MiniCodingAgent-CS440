"""Lab 4 acceptance tests for the Q-learning vacuum agent (Project 2, qlearning-experiments run)."""

import random

from agent_strategy4 import INITIAL_GRID, VacuumEnvironment
from qLearning_Agent import QLearningAgent
from trainVacuum import trainVacuum

GOAL = (3, 3)


def greedy_path(agent, max_steps=20):
    env = VacuumEnvironment(INITIAL_GRID)
    state = env.pos
    path = [state]
    for _ in range(max_steps):
        actions = agent.getActions(env)
        env.step(max(actions, key=lambda a: agent.qtable[(state, a)]))
        state = env.pos
        path.append(state)
        if state == GOAL:
            break
    return path


def test_default_hyperparameters():
    agent = QLearningAgent()
    assert (agent.alpha, agent.gamma, agent.epsilon) == (0.1, 0.9, 0.1)


def test_valid_actions_respect_walls_and_edges():
    agent = QLearningAgent()
    env = VacuumEnvironment(INITIAL_GRID)
    assert sorted(agent.getActions(env)) == ["DOWN", "RIGHT"]
    env.pos = (0, 1)  # wall below
    assert sorted(agent.getActions(env)) == ["LEFT", "RIGHT"]
    env.pos = (2, 1)  # wall above
    assert sorted(agent.getActions(env)) == ["DOWN", "LEFT", "RIGHT"]


def test_q_update_uses_best_next_action():
    agent = QLearningAgent(learning_rate=0.5, discount_factor=0.9, epsilon=0.0)
    agent.qtable[((0, 1), "RIGHT")] = 2.0
    agent.updateQVal((0, 0), "RIGHT", 1.0, (0, 1), ["LEFT", "RIGHT"])
    # 0 + 0.5 * (1 + 0.9 * 2 - 0) = 1.4
    assert abs(agent.qtable[((0, 0), "RIGHT")] - 1.4) < 1e-9


def test_terminal_update_ignores_future_value():
    agent = QLearningAgent(learning_rate=1.0, discount_factor=0.9)
    agent.qtable[(GOAL, "UP")] = 100.0
    agent.updateQVal((3, 2), "RIGHT", 10.0, GOAL, [])
    assert agent.qtable[((3, 2), "RIGHT")] == 10.0


def test_greedy_choice_when_epsilon_is_zero():
    agent = QLearningAgent(epsilon=0.0)
    agent.qtable[((0, 0), "DOWN")] = 1.0
    for _ in range(20):
        assert agent.chooseAction((0, 0), ["DOWN", "RIGHT"]) == "DOWN"


def test_train_accepts_all_hyperparameters():
    agent = trainVacuum(episodes=5, living_reward=-0.04, learning_rate=0.1,
                        discount_factor=0.9, epsilon=0.1)
    assert isinstance(agent, QLearningAgent)


def test_training_learns_a_path_to_the_goal():
    random.seed(0)
    agent = trainVacuum(episodes=1000)
    assert greedy_path(agent)[-1] == GOAL
