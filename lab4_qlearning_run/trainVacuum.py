import random
from agent_strategy4 import VacuumEnvironment, INITIAL_GRID
from qLearning_Agent import QLearningAgent


def trainVacuum(episodes=1000, living_reward=-0.04,
                learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
    agent = QLearningAgent(learning_rate, discount_factor, epsilon)
    for _ in range(episodes):
        env = VacuumEnvironment(INITIAL_GRID)
        state = env.pos
        for _ in range(100):
            action = agent.chooseAction(state, agent.getActions(env))
            env.step(action)
            nextState = env.pos
            reward = living_reward
            cell = env.grid[nextState[0]][nextState[1]]
            if isinstance(cell, (int, float)):
                reward += cell
            done = nextState == (3, 3)
            nextActions = [] if done else agent.getActions(env)
            agent.updateQVal(state, action, reward, nextState, nextActions)
            state = nextState
            if done:
                break
    return agent
