# Lab 4 solved with Q-learning by the mini agent using the Lab 5 skill

Input workspace for the `qlearning-experiments` run (Project 2, iteration 4).
It contains only the Lab 4 environment, the task and the tests. There is no
`qLearning_Agent.py` or `trainVacuum.py` until the agent writes them.

| File | Origin |
|------|--------|
| `agent_strategy4.py`, `Test/test_strategy4.py` | Lab 4 environment and tests (group8 repo) |
| `spec.md`, `Test/test_qlearning.py` | Q-learning task and acceptance tests (input) |
| `qLearning_Agent.py`, `trainVacuum.py` | **written by the mini agent** (after the run) |
| `logs/` | run 4b: `skills.jsonl`, `session.json`, `console_output.txt`; failed run 4a: `run4a_session.json` |

## How to run

The agent treats the git repo root as its workspace, so run it on a copy
**outside** this repo (the same way `lab4_skill_run` was produced).

PowerShell (Windows):

```powershell
Copy-Item -Recurse lab4_qlearning_run $HOME\lab4_qlearning_ws
python mini_coding_agent.py --cwd $HOME\lab4_qlearning_ws --approval auto `
  --max-steps 14 --max-new-tokens 6144 --ollama-timeout 600 `
  "Solve Lab 4 with Q-learning: train the vacuum robot on the 4x4 grid and report the learned policy."
```

bash (macOS / Linux):

```bash
cp -r lab4_qlearning_run ~/lab4_qlearning_ws
python mini_coding_agent.py --cwd ~/lab4_qlearning_ws --approval auto \
  --max-steps 14 --max-new-tokens 6144 --ollama-timeout 600 \
  "Solve Lab 4 with Q-learning: train the vacuum robot on the 4x4 grid and report the learned policy."
```

The prompt does not name a skill; the similarity check picks it.

## After the run

Copy back into this folder:

- `qLearning_Agent.py`, `trainVacuum.py` from the workspace copy
- `.mini-coding-agent/logs/skills.jsonl` → `logs/skills.jsonl`
- the newest file in `.mini-coding-agent/sessions/` → `logs/session.json`
- the terminal output (`[skills]` lines + final answer) → `logs/console_output.txt`

Check it:

```bash
python -m pytest -q Test/test_qlearning.py Test/test_strategy4.py
python ../skills/qlearning-experiments/scripts/evaluate.py --episodes 1000 --seed 0
```
