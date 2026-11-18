# 05 — Verification

**SDLC stage:** Verification / Validation (with iteration back to spec + implementation)
**Verifies:** [01-intent.md](01-intent.md) success criteria

## Setup

- Model: Ollama `qwen3.5:4b` (local, 32k context).
- Workspace: a clean folder containing only `README.md`, Lab 4's `spec.md`
  (Strategy 1, persistent memory) and Lab 4's `Test/test.py`. **No solution file.**
- Command:

```bash
python mini_coding_agent.py --cwd <clean-lab4-workspace> --approval auto \
  --max-steps 14 --max-new-tokens 6144 --ollama-timeout 600 \
  "Solve Lab 4: implement the agent described in spec.md so that the tests in Test/ pass."
```

The prompt does not name the skill. Selection is left to the similarity check.

## Iterations

| Run | Change before the run | Result |
|-----|-----------------------|--------|
| 1 | — (first implementation) | Skill auto-selected (0.590). The model then looped on `read_file spec.md` until the step limit. **Cause:** component 4 clips each tool result to 900 chars in the transcript, so the 4B model never saw the full 7.5k-char spec. **Fail.** |
| 2 | Added `context` / `resources` to the skill format (spec §1). The skill preloads `spec.md`, `Test/*.py` and `reference.md` into the Active-skill section. | Wrote `agent_strategy1.py` with one `write_file` call. `pytest -q Test` collected **0 tests**, because the file is named `test.py`. The model recovered with `pytest Test/test.py` → **5 passed**. The `__main__` demo crashed (it used `DummyVacuumWorld` from the tests). **Pass, with skill defects.** |
| 3 | Skill fixes: run `pytest -q Test/*.py`; the demo must define its own env; run the file after the tests. | Skill auto-selected (0.590). After 5 malformed `write_file` attempts, which the runtime rejected and the model retried, it wrote the file. Ran `pytest -q Test/*.py` → **5 passed**. Final answer: `Done.` **Pass.** |

Artifacts from run 3 are in [`../lab4_skill_run/`](../lab4_skill_run/).
Run 2's session transcript and run 1's console log are in
`lab4_skill_run/logs/earlier_iterations/`.

## Skill log from run 3 (`lab4_skill_run/logs/console_stderr.txt`)

```
[skills] discovered 2 skill(s): pr-review, vacuum-world-agent
[skills] prompt: 'Solve Lab 4: implement the agent described in spec.md so that the tests in Test/ pass.'
[skills] similarity (threshold 0.20): vacuum-world-agent=0.590, pr-review=0.011 -> selected: vacuum-world-agent
[skills] executing skill 'vacuum-world-agent' (trigger=auto, score=0.590) from .../skills/vacuum-world-agent/SKILL.md; loaded files: spec.md, Test/test.py, vacuum-world-agent/reference.md
```

The same events are stored as JSON lines in `lab4_skill_run/logs/skills.jsonl`
(`discover`, `prompt`, `similarity_check` with all scores, `skill_executed`).

## Success criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| S1 | Skill folders discovered | ✅ | unit tests; `discover` log event |
| S2 | Matching prompt auto-activates the right skill; unrelated prompt doesn't | ✅ | unit tests; live score 0.590 vs 0.011 |
| S3 | Model can trigger a skill mid-run (`use_skill`) | ✅ | `test_model_can_trigger_skill_during_execution` (not exercised in the live run, because auto-selection already fired) |
| S4 | Prompt, similarity check, executed skill logged | ✅ | `skills.jsonl`, stderr |
| S5 | Lab 5 skill packaged as a folder | ✅ | `skills/vacuum-world-agent/` |
| S6 | Mini agent + skill solves Lab 4; Lab 4 tests pass | ✅ | `cd lab4_skill_run && python -m pytest -q Test/test.py` → `5 passed` |
| S7 | Existing tests pass; stdlib only | ✅ | `41 passed` |

## Known limitations

- **Demo still crashes in run 3.** The model skipped the skill's "run the
  file" step and returned `Done.` right after the tests passed. Its
  `__main__` demo then raises `KeyError: 'SUCK'` (it treats `SUCK` as a
  move). The Lab 4 tests don't cover the demo, so S6 still passes, but the
  spec's "standalone demo" requirement is not met by this generated file.
  This comes from the small model's reliability, not from the skill
  component.
- Results with a 4B model vary from run to run. Run 3 is one recorded run,
  not a guarantee.
- Similarity is lexical (TF-IDF). A paraphrase with no shared words (e.g.
  "build the thing for lab 4" scores 0.165) won't auto-trigger. The model
  can still call `use_skill`, or the user can type `/skill vacuum-world-agent ...`.

## About the Lab 5 skill

The Lab 5 repository has no `SKILL.md` checked in. `skills/vacuum-world-agent`
was written from Lab 5's spec-driven workflow (spec → generate → test) and
its Q-learning notes. If the team has its own Lab 5 `SKILL.md`, drop it into
`skills/<name>/SKILL.md`, add `context:` / `resources:` lines if needed, and
rerun the command above.

## Iteration 4 — team's original Lab 5 skill (`qlearning-experiments`)

See [02-spec.md §9](02-spec.md). Runs 1–3 above are unchanged.

### Offline checks (no model)

| Check | Result |
|-------|--------|
| Similarity check, Austin's §8 prompt | `vacuum-world-agent=0.586`, `qlearning-experiments=0.049`, `pr-review=0.013` → `vacuum-world-agent`. Run 3 logged 0.590 with two skills; the small drift comes from adding a third skill to the TF-IDF corpus. |
| Similarity check, Q-learning prompt | `qlearning-experiments=0.634`, `vacuum-world-agent=0.502`, `pr-review=0.000` → `qlearning-experiments` |
| Skill scripts against the team's Lab 5 code | `evaluate.py` (seed 0): greedy path reaches +10 in 6 steps (shortest possible), 100% over 10 seeds |
| Workspace tests against the team's Lab 5 code | `14 passed` |
| Scripted run with `FakeModelClient` | skill auto-selected, prompt carries spec + tests + reference, files written, tests and `evaluate.py` run through `run_shell` |

### Live run (Ollama `qwen3.5:4b`)

Command and prompt: [`../lab4_qlearning_run/RUN.md`](../lab4_qlearning_run/RUN.md).

| Run | Result |
|-----|--------|
| 4a (Windows, CPU) | Selected `qlearning-experiments` (0.634 vs `vacuum-world-agent` 0.502). Agent wrote `qLearning_Agent.py` and `trainVacuum.py` from reference.md; workspace tests **14 passed**. It then ran `python "qlearning-experiments/scripts/evaluate.py"`: the model shortened the `SKILL_DIR` placeholder to the skill's name instead of the absolute path, the file was not found, and it spent the remaining steps on `list_files` retries. Stopped at the 14-step limit with no final answer. |
| 4b (Windows, CPU, after the fix) | **Pass.** Selected `qlearning-experiments` (0.634). Agent wrote `qLearning_Agent.py` and `trainVacuum.py`, workspace tests **14 passed**, ran `evaluate.py` from the skill folder: greedy policy reaches +10 in **6 steps** (shortest possible), **100%** over 10 seeds, mean 6.0 steps. Final answer reports the policy grid and Q-values from the script output. |

**Fix after run 4a.** Substituting a placeholder is unreliable for a 4B model,
so the component now does it: `MiniAgent.skill_body()` replaces `{skill_dir}`
in a skill's body with the skill folder's absolute path (forward slashes, so
it stays valid inside a JSON tool call on Windows and survives spaces in the
path when quoted). `qlearning-experiments/SKILL.md` uses `{skill_dir}` and
tells the model to copy commands exactly. Test:
`test_skill_dir_placeholder_becomes_absolute_forward_slash_path`.

**Windows path fix.** `skill_files()` labels preloaded files with
`relative_to(root).as_posix()` instead of `str(...)`, so labels and the
`loaded_files` log field read `Test/test_qlearning.py` on Windows too
(`test_skill_context_and_resources_are_loaded_into_prompt` failed on Windows
before this change; macOS output is unchanged).

Artifacts in `lab4_qlearning_run/logs/`: run 4b `skills.jsonl`, `session.json`, `console_output.txt`; run 4a `run4a_session.json`.
