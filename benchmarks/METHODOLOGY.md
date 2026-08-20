# Signal multi-agent benchmark methodology

This is the design decision `benchmarks/README.md` refers to as its source
of truth. It extends the original single-agent pilot (`README.md`) to run
fairly across multiple coding agents without turning into a benchmark
framework. Read `README.md` first for the question, matrix, and metrics —
this document covers what changed to make that pilot runnable across
agents: isolation, skill installation, and evaluation dimensions.

Nothing here executes a run. Preparing and validating a workspace is the
only automated part; running the agent and scoring the output stays manual.

## Why isolation needed a mechanism, not just a rule

`README.md` already states "fresh workspace per run, no prior run outputs
visible" and "baseline has no Signal documentation available" as fairness
controls. Those were principles without a concrete implementation. Running
across three different agents (Claude Code, Codex, Antigravity) makes that
gap unsafe by default: each agent, run from the repo root, could see
`SKILL.md`, `CONTRACT.md`, `recipes/`, `benchmarks/cases/*/acceptance.md`,
and other agents' runs — contaminating both the baseline/Signal comparison
and the cross-agent comparison. `benchmarks/scripts/prepare_workspace.py`
and `validate_workspace.py` turn the stated rule into something that can
be checked.

## Evaluation dimensions

Kept explicit and separate so results from one don't get read as answers
to another.

### A. Signal efficacy (primary result)

Within one agent: `signal` condition vs. `baseline` condition, same case,
same prompt. This delta is the headline number per agent. Claude vs. Codex
vs. Antigravity is never compared as a primary result — different models
have different baselines for unrelated reasons.

### B. Skill portability (secondary result)

Across agents: does `Δ Signal = signal_condition − baseline_condition`
come out positive for more than one agent? A skill that only helps one
agent is a weaker result than one that transfers. This is read from the
same run data as (A), just aggregated differently — no separate runs.

### C. Skill discovery (kept separate, not blended into A or B)

The primary benchmark uses **implicit discovery**: Signal is installed at
the project level, the prompt is an ordinary plotting request, and nothing
in the prompt says "use Signal" or names it. This tests whether the agent
finds and applies the skill on its own. Explicit invocation (`/signal`,
`$signal`, or an agent's equivalent) is a separate condition, run and
reported separately if it happens at all. Every `run.json` records an
`invocation` field (`implicit` | `explicit`) specifically so these never
get merged into one number by accident.

## Isolation model

**Baseline workspace** — must not contain, anywhere in the tree:

```text
SKILL.md, CONTRACT.md, recipes/, components/, references/, themes/, intents/
.claude/skills/, .agents/skills/
benchmarks/, tests/, lab/, .git/
acceptance.md (any case), score.json, other runs
```

**Signal workspace** — receives Signal only through the project-level skill
mechanism native to that agent. Everything forbidden for baseline stays
forbidden here too, except the one skill directory that condition
installs. A Signal workspace never becomes "the Signal repo" — it gets a
copy of the minimal payload (below), not the repository.

**Both workspaces** get the exact same `data.csv` and `prompt.txt`, byte
for byte. The only experimental difference is the skill's presence.
Benchmark plumbing ("save as `plot.py`... `plot.png`") is shared by both
conditions, same as the existing pilot already establishes.

## Skill payload: what ships, what doesn't

Installing the whole Signal repo as the project skill would hand the
agent `benchmarks/cases/*/acceptance.md` and prior run outputs — the
comparison would be measuring rubric-reading, not plotting. The payload is
instead the minimal file set `SKILL.md`'s own selective-loading section
declares as needed, assembled fresh from the repo root by
`prepare_workspace.py` (never a hand-maintained duplicate that can drift):

```text
SKILL.md
CONTRACT.md
intents/README.md
recipes/_TEMPLATE.md, recipes/common/*.md, recipes/scientific/*.md
components/*.md
references/chart_selection.md, references/scientific_integrity.md
themes/README.md, themes/signal_style.py
```

Excluded, deliberately:

- `lab/` — `SKILL.md` lists it under "chart reproduction/learning," an
  optional, explicitly experimental lane, not something ordinary plotting
  needs. Confirmed absent from both `SKILL.md`'s and `CONTRACT.md`'s
  required paths.
- `references/sources.md` — architectural provenance/credits, not needed
  to produce a plot.
- `examples/`, `templates/` — neither is referenced by `SKILL.md`'s
  selective-loading list.
- `docs/`, `AGENTS.md`, `CONTRIBUTING.md`, root `README.md` — repo
  contributor material, not skill runtime content.
- `benchmarks/`, `tests/`, `.git/` — the benchmark itself; must never be
  visible to an evaluated agent under any condition.

One payload, reused for every agent. Signal is not forked or rewritten
per agent.

## Project-level skill installation per agent

| Agent | Native project-skill path | Payload |
|---|---|---|
| Claude Code | `.claude/skills/signal/` | shared payload above |
| Codex | `.agents/skills/signal/` | shared payload above |
| Antigravity | `.agents/skills/signal/` | shared payload above |

Codex and Antigravity both walk up from the working directory looking for
`.agents/skills/`, so the same installed directory satisfies both without
a fork. Claude Code uses its own `.claude/skills/` convention. Verify
these paths against each product's current docs before running — agent
skill conventions move faster than this file will be updated.

## Workspace layout

```text
benchmarks/workspaces/<agent>/<condition>/<case>/
```

e.g. `benchmarks/workspaces/claude/signal/plant_growth/`. Generated by
`prepare_workspace.py`, wiped and rebuilt on every call (that's what makes
"fresh workspace per run" real rather than aspirational), and gitignored —
it's scratch, not a record. The permanent record is `benchmarks/runs/`,
populated by hand-copying the finished workspace's outputs after a run
(see `README.md`'s `runs/<run-id>/` layout).

## Minimal tooling

`benchmarks/scripts/`:

- `prepare_workspace.py --agent {claude,codex,antigravity} --condition {baseline,signal} --case <name>`
  builds one workspace: copies `data.csv`/`prompt.txt`, installs the skill
  payload at the native path if `condition=signal`, prints the resulting
  paths.
- `validate_workspace.py --agent ... --condition ... --case ...` re-walks
  that workspace and asserts nothing forbidden is present and (for
  `signal`) that the payload matches exactly. Exits non-zero and lists
  violations on failure.

Neither runs an agent, scores a run, or touches `benchmarks/runs/`. They
exist to remove the two invalid-experiment failure modes that are cheap
to prevent: a hand-copied workspace missing a file, and a stale leftover
file from a previous run.

## Run metadata

`benchmarks/runs/run.template.json` is the format. Fields left `null` mean
"not obtainable from this agent/session" — never fabricate a token count,
seed, or model id to fill a field. Raw artifacts
(`prompt.txt`, `plot.py`, `plot.png`, `stdout.txt`, `stderr.txt`,
`transcript.txt`) remain the source of truth; `run.json` and `score.json`
are indexes into them, not replacements.

## Acceptance rubrics stay evaluator-side

`acceptance.md` for every case, including the new `nonlinear_surface`
case, lives only under `benchmarks/cases/<case>/` in the main repo tree —
never copied into a workspace by `prepare_workspace.py`, never visible to
an evaluated agent under either condition. `validate_workspace.py` checks
for its absence as part of containment.

## Pilot execution order

Do not run the full matrix. Expand only after each stage discriminates
meaningfully and isolation validates clean.

1. **Smoke test** — `plant_growth` × {claude, codex, antigravity} ×
   {baseline, signal} = 6 runs. Confirms the isolation mechanism and
   install paths actually work end to end on the existing, already-tuned
   case.
2. **Adversarial case** — `nonlinear_surface` × {claude, codex,
   antigravity} × {baseline, signal} = 6 more runs. Confirms the new case
   discriminates before investing in repeats.
3. Only after both stages look sound: expand to repeated runs (3x per
   the existing fairness control) and the remaining cases (`temperature`,
   `ab_experiment`).

## Scope not covered here (future work, not silently skipped)

- OS-level containment (containers, sandboxes): not implemented. The
  isolation here is filesystem-assertion-level, sufficient to catch
  accidental leakage, not adversarial escape. If that distinction starts
  to matter, it's future work, not something to bolt on now.
- No orchestration, no LLM-as-judge, no dashboards, no automated
  execution of Claude/Codex/Antigravity — all still manual, per
  `README.md`'s existing scope.
