---
name: qlearning-experiments
description: Train and evaluate the vacuum-world Q-learning agent, or compare hyperparameter settings (living reward, discount factor, learning rate, epsilon). Use when asked to train the agent, show the learned policy or Q-values, check whether the agent reaches the +10 cell, or justify/tune hyperparameters.
triggers: q-learning agent, qlearning, train the agent, train the vacuum robot, learned policy, q-values, hyperparameter, living reward, epsilon-greedy
context: spec.md, Test/test_qlearning.py
resources: reference.md
---

# Q-learning experiments for the vacuum world (CS440 Lab 5 skill)

The environment is the fixed 4x4 grid in `agent_strategy4.py` (`INITIAL_GRID`):
start (0,0), wall at (1,1), -1 at (3,1), +10 at (3,3). Training lives in
`trainVacuum.py`; the agent is `QLearningAgent` in `qLearning_Agent.py`.
Never edit `INITIAL_GRID`, `agent_strategy4.py`, or anything in `aima/`.

`spec.md`, `Test/test_qlearning.py` and `reference.md` are already loaded
below under "Skill files". Do not call read_file on them. One tool call per
reply. The commands below already contain the full path to this skill's
scripts: copy them exactly, do not shorten or change the path.

## Step 1 - Make sure the agent exists (Project 2 addition)
If `qLearning_Agent.py` and `trainVacuum.py` are not in the workspace, write
them first, one write_file call each, following the interface in
reference.md exactly (class, method and argument names are what the tests and
the scripts call). Use only the Python standard library.

## Step 2 - Run the tests
`{"command":"python -m pytest -q Test/test_qlearning.py Test/test_strategy4.py","timeout":120}`
If a test fails, read the assertion, fix the smallest piece with patch_file
(or rewrite the file), and run the tests again.

## Step 3 - Train and evaluate one setting
Run from the workspace root:

`{"command":"python \"{skill_dir}/scripts/evaluate.py\" --episodes 1000 --living-reward -0.04 --alpha 0.1 --gamma 0.9 --epsilon 0.1 --seed 0","timeout":120}`

It prints:
- the greedy policy as an arrow grid (`#` = wall, `G` = +10 goal),
- the greedy path from start and whether it reaches +10,
- the max Q-value per cell,
- a success rate across several random seeds.

## Compare hyperparameters (only when asked)

`{"command":"python \"{skill_dir}/scripts/sweep.py\" --param living_reward","timeout":120}`

`--param` is one of `living_reward`, `gamma`, `alpha`, `epsilon`. The other
three stay at the team's chosen defaults. The sweep trains for only 30
episodes per run (30 seeds each) on purpose: with 1000 episodes every
reasonable setting solves this small grid, so a short budget is what shows
which values learn fast and which fail. Use `--episodes` to change it. Add
`--values` to override the tested values, e.g. `--values -0.04 -0.5 -2`.

## How to report results
Reply with `<final>` containing:
- whether the greedy policy reaches +10 and in how many steps
  (the shortest possible path is 6 moves),
- the policy grid exactly as printed,
- the test result line (for example `11 passed`),
- when comparing settings, the sweep table and one sentence per parameter on
  why the chosen value is reasonable, tying it to the grid (e.g. +10 is 6
  moves away, so gamma must keep distant reward meaningful).
Report numbers from the script output only; do not estimate them.
