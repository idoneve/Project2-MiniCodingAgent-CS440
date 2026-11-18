"""Compare values of one hyperparameter, holding the others at the defaults.

The default is a short training budget (30 episodes): with 1000 episodes
every reasonable setting solves this small grid, so a short budget is what
shows which settings learn quickly and which learn slowly or not at all.

Run from the project (workspace) root; see SKILL.md for usage.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from evaluate import parse_args as default_args, success_rate  # noqa: E402

DEFAULT_VALUES = {
    "living_reward": [0.0, -0.04, -0.5, -2.0],
    "gamma": [0.1, 0.5, 0.9, 0.99],
    "alpha": [0.01, 0.1, 0.5, 1.0],
    "epsilon": [0.0, 0.05, 0.1, 0.3],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--param", required=True, choices=DEFAULT_VALUES)
    parser.add_argument("--values", type=float, nargs="+")
    parser.add_argument("--episodes", type=int, default=30)
    parser.add_argument("--trials", type=int, default=30)
    sweep = parser.parse_args()

    values = sweep.values or DEFAULT_VALUES[sweep.param]
    print(f"Sweeping {sweep.param} ({sweep.episodes} episodes, {sweep.trials} seeds each)\n")
    print(f"{sweep.param:>14} | reached +10 | mean steps")
    print("-" * 42)
    for value in values:
        args = default_args([])
        args.episodes = sweep.episodes
        setattr(args, sweep.param, value)
        rate, mean_steps = success_rate(args, range(sweep.trials))
        print(f"{value:>14} | {rate:>11.0%} | {mean_steps:>10.1f}")


if __name__ == "__main__":
    main()
