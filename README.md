# ICAIF 2026 · An evidence-driven trading desk

### What if the most important trading decision happens before the first trade?

A multi-agent portfolio-construction system built for the **[ACM ICAIF 2026 Trading Agent Competition](https://hackathon2.deepintomlf.ai/competitions/99/)**. Four specialists interpret separate evidence streams. A portfolio manager proposes initial weights. Code measures the risks, offers one chance to revise, and commits a validated book.

**[Try the entry demo](#try-the-entry-without-an-api-key)** · **[How the entry works](docs/entry-mechanism.md)** · **[Forecasting stack](docs/forecasting.md)** · **[Contest implementation](docs/contest-entry.md)** · **[Reproduction](docs/reproduction.md)**

[![Desk v3 entry mechanism: point-in-time evidence feeds independent analysts, a portfolio-manager draft, deterministic critique, one revision, and validated initial weights.](assets/entry-mechanism.svg)](docs/entry-mechanism.md)

*The implemented reports-only entry path. The daily ensemble and HAR forecasts provide evidence; they do not independently place trades. After entry, the contest strategy holds the book. [Full-resolution graphic](assets/entry-mechanism.png) · [Editable source](assets/render_entry_mechanism.py).*

## The interesting part is how the decision gets made

An agent that can produce portfolio weights is easy to describe. A system that can explain where they came from, quantify their risks, refuse an invalid proposal, and recover when a model fails is a more useful engineering problem.

| Layer | What it contributes |
|:--|:--|
| **Point-in-time evidence** | Market regime, macro context, earnings timing, eligible headlines, daily-model ranks, volatility forecasts, and broader-universe context |
| **Independent specialists** | Market, earnings, news, and quant analysts each receive their own input slice and produce structured reports |
| **Portfolio manager** | Synthesizes the reports into weights, an investment thesis, and conditions that code can interpret |
| **Quantified critique** | Checks concentration, expected volatility, market beta, recent drawdown, earnings exposure, and entry costs against inverse-volatility and risk-parity references at the same gross exposure |
| **Bounded revision** | The PM confirms or replaces the draft once; a replacement is validated and its risk report is logged |
| **Deterministic commitment** | Code owns the universe, caps, gross-exposure rules, precision, fallback, and final target weights |

This is a **propose → measure → revise once → commit** architecture. The reusable idea extends beyond trading: specialists supply evidence, a decision-maker allocates resources, and ordinary code retains authority over constraints and execution. [See the adaptation guide](docs/entry-mechanism.md#adapting-the-pattern).

## Models that inform the desk

**Daily cross-sectional ensemble.** AutoGluon combines tabular model families to rank forward returns. The data pipeline uses point-in-time universe membership, label-end purging between years, and purged contiguous inner folds to reduce leakage from overlapping return horizons. The desk receives ranks within the 30 contest stocks and context from the broader training universe.

**HAR volatility forecasters.** A log-HAR model uses daily, weekly, and monthly realized-variance features to forecast the next one and three sessions. Stock forecasts are pooled across names; the market basket has a separate fit. Walk-forward quarterly refits respect target end times, while a smearing correction addresses the bias from exponentiating log forecasts.

**Risk and context models.** Shrunk covariance, inverse-volatility and risk-parity books, market-regime readings, and OU residual signals provide interpretable context. The v3 self-check deliberately derives its risk report from historical closes and covariance rather than reintroducing an ablated HAR/model-rank stream.

[Explore the forecasting stack and its limitations](docs/forecasting.md).

## Try the entry without an API key

Python **3.13** is the reference environment. This lightweight path installs neither AutoGluon nor provider SDKs.

```bash
git clone https://github.com/pungyman/icaif2026.git
cd icaif2026
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/demo.txt
python examples/entry_demo.py
```

The demo runs the **real `V3Desk` entry path**, using synthetic market history and scripted analyst/PM responses. It shows a concentrated draft becoming a five-name book after the code-generated critique, then verifies that subsequent rounds hold.

```text
Route: brain / revised
Invested: 75.00%; unallocated target: 25.00%
Draft effective number of names: 2.9
Revised effective number of names: 4.6
Verified: one entry trade; later rounds hold.
```

Try all three outcomes:

```bash
python examples/entry_demo.py --scenario confirm
python examples/entry_demo.py --scenario revise --json
python examples/entry_demo.py --scenario fallback
```

The responses are scripted, not an LLM demonstration or an investment-performance result. No data downloads, model calls, contest submissions, or credentials are involved.

## What actually entered the competition

The implemented **Desk v3 stage 1** constructs an initial book and holds it through the window. The selected configuration uses four analyst reports, a compact PM view, one self-check, and every selected evidence stream except SEC filing text. The runner supports several provider adapters; the recorded official entry used Gemini 3.1 Pro through Vertex AI.

Two choices are separate:

1. **Composition:** the PM's relative allocation among stocks.
2. **Exposure:** a code-configured overlay that scales that allocation and leaves the rest in cash.

The [recorded October 12 entry](OFFICIAL_ENTRY_2026-10-12.md) bought **13 names at 0.1% total NAV exposure**, with 99.9% in cash. This differs from the 10% overlay discussed in earlier planning notes. The PM was not shown the post-decision overlay; the submitted weights reflect code's scaling. For example, a 12% NVDA share within the equity mix becomes a **0.012% NAV target** at the recorded overlay. These are historical contest settings, not recommended allocations.

**Status as of October 28, 2026:** the official trading period is still in progress; no final competition ranking is claimed here. A proposed later escalation hierarchy is documented in the research notes, but is **not implemented as Desk v3 stage 2**. Plan conditions are recorded at entry; the official stage-1 strategy does not act on them later.

[Contest rules, entry configuration, and evidence](docs/contest-entry.md).

## Built to make failures visible

- **No look-ahead:** observations cut at the decision deadline; labels and folds are purged by label end, not just row date.
- **Reject rather than repair:** an invalid proposed book is refused as a whole. Silently clipping its weights would execute a portfolio the PM never selected.
- **Measure against equal exposure:** self-check references use the draft's gross, keeping stock selection distinct from the cash decision.
- **Bounded calls:** deadlines, structured schemas, caching, cost accounting, and counted fallbacks sit around model calls.
- **Deterministic fallback:** if no usable entry survives, the desk selects an inverse-volatility book at the applicable configured exposure.
- **Contest parity:** final weights use a precision-safe grid and the organizers' own contract/metric implementation from the vendored starter kit.
- **Traceability:** draft, validation errors, risk report, PM check, any revision, and final weights are recorded separately.

## Find the implementation

| Start here | Implementation |
|:--|:--|
| Entry orchestration | [`icaif/agents/v3.py`](icaif/agents/v3.py) |
| Specialist/PM prompts and schemas | [`prompts_v3.py`](icaif/agents/prompts_v3.py), [`schemas.py`](icaif/agents/schemas.py), [`v2.py`](icaif/agents/v2.py) for shared analyst orchestration |
| Deterministic risk critique | [`icaif/agents/selfcheck.py`](icaif/agents/selfcheck.py) |
| Daily ensemble and purged folds | [`icaif/train.py`](icaif/train.py), [`daily_features.py`](icaif/daily_features.py), [`labels.py`](icaif/labels.py) |
| HAR forecasts and signal delivery | [`icaif/vol.py`](icaif/vol.py), [`icaif/agents/signals.py`](icaif/agents/signals.py) |
| Simulator, weights, and official formulas | [`icaif/sim.py`](icaif/sim.py), [`weights.py`](icaif/weights.py), [`kit.py`](icaif/kit.py) |
| Entry experiments | [`tools/entry_replay.py`](tools/entry_replay.py), [`tools/doe_report.py`](tools/doe_report.py), [`stage1_doe.md`](stage1_doe.md) |
| Recorded official entry | [`OFFICIAL_ENTRY_2026-10-12.md`](OFFICIAL_ENTRY_2026-10-12.md) |
| Existing detailed research notes | [`docs/development-notes.md`](docs/development-notes.md), [`mlsys/`](mlsys/README.md) |

## Reproduction and scope

The [reproduction guide](docs/reproduction.md) separates the offline demo, focused tests, full modeling environment, and contest artifacts. Raw licensed data, trained ensembles, historical feed snapshots, provider credentials, and cached model responses are not bundled. Recreating the exact official decision requires those original artifacts; rerunning a current hosted model is not an exact replay.

The repository includes earlier rule, v1, and v2 desks, experimental GNN work, dashboards, and operational tools for research traceability. The front-page mechanism and demo refer specifically to the implemented v3 entry. Existing notes are dated research records and may describe superseded configurations.

The organizers' [`starter-kit/`](starter-kit/README.md) remains unchanged, vendored from [DeepIntoStreams/2026ICAIF_Trading_Agent_Competition](https://github.com/DeepIntoStreams/2026ICAIF_Trading_Agent_Competition) at `ad237b0`. This is a participant's implementation, not the organizers' repository. [Attribution and citation](CITATION.cff).
