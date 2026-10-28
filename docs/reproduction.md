# Reproduction paths

Python 3.13 is the project's reference environment. Start with the lightweight demo; full training uses a separate, heavier dependency file and requires original data/artifacts.

## 1. Inspect the entry offline

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/demo.txt
python examples/entry_demo.py
python examples/entry_demo.py --scenario confirm
python examples/entry_demo.py --scenario fallback
python examples/entry_demo.py --scenario revise --json
```

The demo uses seeded synthetic hourly history for the organizers' stock universe. Structured role outputs are scripted. The actual `V3Desk`, validation, risk self-check, simulator, and fallback paths execute; no provider or competition client is invoked. Execution prices are synthetic constants, so the demo deliberately reports no return/Sharpe result. Its purpose is to expose the decision artifact and verify one entry trade followed by holding.

The default revision spreads a three-name draft over five names at the same gross. The printed effective-name count comes from `selfcheck.report`, not an illustrative number copied into the script.

## 2. Focused tests

```bash
python -m pip install -r requirements/test.txt
python -m pytest -q tests/test_v3.py tests/test_vol.py tests/test_daily_features.py tests/test_train.py tests/test_schemas.py
```

These cover entry confirmation/revision/fallback, caps and gross rules, plan schemas, forecasting behavior, feature timing, and purged training splits. The GitHub workflow also runs all three synthetic demo routes. No inference, live order, submission, notification, or training command is used by that workflow.

The repository contains a larger research/operational test suite. Some tests require optional dependencies or original local data and should be interpreted under their own fixtures. A passing focused suite is not a rerun of the historical contest or model training.

## 3. Full modeling environment

```bash
python -m pip install -r requirements.txt
```

This includes AutoGluon and provider adapters and is substantially heavier than the demo environment. Install into an environment appropriate for your hardware and check dependency/platform support before training. `pydantic` is explicitly required for structured role schemas.

Useful code entry points:

| Task | Entry point |
|:--|:--|
| Daily/intraday purged training | `tools/train_walkforward.py` |
| Daily feature diagnostics | `tools/daily_feature_report.py` |
| HAR volatility diagnostics | `tools/vol_report.py` |
| Designed entry experiments | `tools/entry_replay.py` |
| Experiment decisions/paired comparisons | `tools/doe_report.py` |
| Official metrics calculator | `starter-kit/tools/evaluate.py` |

Read each tool's `--help`, dependency and data requirements first. Paid entry experiments have an explicit opt-in; a data-backed replay and a cached replay are different from the scripted offline demo.

## 4. Inputs and artifact boundaries

- **Organizer panel:** participant-licensed hourly data, obtained through the competition's Files tab; not redistributed here.
- **Historical market feeds:** the original dated snapshots used for development. Some rolling intraday feeds cannot be refetched once their retention window moves.
- **External context:** point-in-time daily universe, macro series, earnings calendars, eligible news, and—where enabled—SEC filings, under their providers' terms.
- **Model artifacts:** trained AutoGluon stacks, out-of-sample prediction panels, HAR inputs, and provider/model identifiers for the specific run.
- **Agent artifacts:** cached role responses, timestamps, prompts, configuration, entry record, and simulator/live-run records.

All are separate from source code. The local data layout is described in `CLAUDE.md` and the dated development notes, but private storage locations mentioned in old notes are not public download endpoints. No access to that storage is necessary for the synthetic demo.

## 5. Exact replay versus a new inference run

`CachedBrain` keys outputs by model, role, system prompt, and observation. Original caches are needed to recover the same hosted-model answers without calling a provider. Calling a currently available model again is a new experiment, even when its public model name is unchanged. Provider access, decoding behavior, historical snapshots, timestamps, and current feed revisions can all affect reproduction.

The recorded official entry is described in `OFFICIAL_ENTRY_2026-10-12.md`. Historical development notes include older overlays and trial commands; use the entry record when reporting the submitted configuration.

## 6. Contest and operational boundaries

The submission clients and production runner remain in the repository for implementation completeness. They are not part of the demo path. Preparing a public repository does not register a team, arm a runner, change a strategy, or submit a contest round. Keep runtime credentials out of source control and supply them privately only for an independently authorized deployment.

## Diagram source

`assets/render_entry_mechanism.py` writes the editable SVG using the standard library. With CairoSVG installed it also writes a high-resolution PNG:

```bash
python -m pip install cairosvg
python assets/render_entry_mechanism.py
```

CairoSVG may require a system Cairo library. The committed SVG/PNG can be viewed without installing the renderer. The diagram's authoritative implementation references are in [entry-mechanism.md](entry-mechanism.md).
