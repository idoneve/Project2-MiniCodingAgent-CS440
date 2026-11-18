"""Train the Q-learning agent once and report its learned policy.

Run from the project (workspace) root; see SKILL.md for usage.
"""

import argparse
import os
import random
import sys

# Lab 5 kept this skill in <project>/.claude/skills/, so the project root was
# four folders up. In the mini coding agent the skill lives in the agent's own
# skills/ folder and run_shell starts in the workspace, so the workspace is
# the current directory. Both layouts are supported.
_LAB5_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PROJECT_ROOT = os.getcwd() if os.path.isfile("trainVacuum.py") else _LAB5_ROOT
sys.path.insert(0, PROJECT_ROOT)

from agent_strategy4 import INITIAL_GRID, VacuumEnvironment  # noqa: E402
from trainVacuum import trainVacuum  # noqa: E402

GOAL = (3, 3)
ARROWS = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}


def greedy_action(agent, env, state):
    """Pick the highest-Q valid action (no exploration)."""
    actions = agent.getActions(env)
    return max(actions, key=lambda a: agent.qtable[(state, a)])


def greedy_path(agent, max_steps=20):
    """Follow the greedy policy from the start cell."""
    env = VacuumEnvironment(INITIAL_GRID)
    state = env.pos
    path = [state]
    for _ in range(max_steps):
        env.step(greedy_action(agent, env, state))
        state = env.pos
        path.append(state)
        if state == GOAL:
            break
    return path


def policy_grid(agent):
    """Return the greedy policy as rows of arrows."""
    rows = []
    for r, row in enumerate(INITIAL_GRID):
        cells = []
        for c, value in enumerate(row):
            if value == "X":
                cells.append("#")
            elif (r, c) == GOAL:
                cells.append("G")
            else:
                env = VacuumEnvironment(INITIAL_GRID)
                env.pos = (r, c)
                cells.append(ARROWS[greedy_action(agent, env, (r, c))])
        rows.append("  ".join(cells))
    return "\n".join(rows)


def value_grid(agent):
    """Return the max Q-value of each cell as rows of numbers."""
    rows = []
    for r, row in enumerate(INITIAL_GRID):
        cells = []
        for c, value in enumerate(row):
            if value == "X":
                cells.append(f"{'#':>7}")
                continue
            q_values = [agent.qtable[((r, c), a)] for a in ARROWS]
            cells.append(f"{max(q_values):7.2f}")
        rows.append(" ".join(cells))
    return "\n".join(rows)


def train(args, seed):
    """Train one agent with a fixed random seed."""
    random.seed(seed)
    return trainVacuum(
        episodes=args.episodes,
        living_reward=args.living_reward,
        learning_rate=args.alpha,
        discount_factor=args.gamma,
        epsilon=args.epsilon,
    )


def success_rate(args, seeds):
    """Fraction of seeds whose greedy policy reaches the goal, and mean path length."""
    lengths = []
    for seed in seeds:
        path = greedy_path(train(args, seed))
        if path[-1] == GOAL:
            lengths.append(len(path) - 1)
    rate = len(lengths) / len(seeds)
    mean_steps = sum(lengths) / len(lengths) if lengths else float("nan")
    return rate, mean_steps


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--living-reward", dest="living_reward", type=float, default=-0.04)
    parser.add_argument("--alpha", type=float, default=0.1)
    parser.add_argument("--gamma", type=float, default=0.9)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--trials", type=int, default=10, help="seeds used for the success rate")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    agent = train(args, args.seed)
    path = greedy_path(agent)

    print(
        f"Hyperparameters: episodes={args.episodes}, living_reward={args.living_reward}, "
        f"alpha={args.alpha}, gamma={args.gamma}, epsilon={args.epsilon}, seed={args.seed}\n"
    )
    print("Greedy policy (# = wall, G = +10 goal):")
    print(policy_grid(agent))
    print("\nMax Q-value per cell:")
    print(value_grid(agent))
    print(f"\nGreedy path: {' -> '.join(str(p) for p in path)}")
    if path[-1] == GOAL:
        print(f"Reached +10 in {len(path) - 1} steps (shortest possible: 6)")
    else:
        print("Did NOT reach +10 within 20 steps")

    rate, mean_steps = success_rate(args, range(args.trials))
    print(f"\nAcross {args.trials} seeds: reached goal {rate:.0%} of the time, mean {mean_steps:.1f} steps")


if __name__ == "__main__":
    main()
