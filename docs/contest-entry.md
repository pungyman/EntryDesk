# Contest implementation and recorded entry

This is a participant's code for [ACM ICAIF 2026 Trading Agent Competition, Codabench 99](https://hackathon2.deepintomlf.ai/competitions/99/), not the organizers' implementation.

## Task and protocol

The contest manages a $1,000,000 starting portfolio across 30 U.S.-listed stocks with seven scheduled decision rounds per trading day. It is long-only: at most 30% per name, at most 100% gross, and unallocated capital remains cash. Executed trades incur a 0.1% notional cost. The official trading window is October 12–30, 2026. Eligibility also depends on the organizers' final-materials and reproducibility requirements.

The official page and vendored `starter-kit/docs/` are the rule references. The starter kit's own validation and metric calculator are reused through `icaif/kit.py`; the simulator that produces their inputs is this project's implementation.

## Recorded configuration

The October 12 record in [`OFFICIAL_ENTRY_2026-10-12.md`](../OFFICIAL_ENTRY_2026-10-12.md) describes:

- Desk v3 stage 1: an initial allocation, followed by holding.
- Four specialist reports; the PM sees reports plus compact context.
- The selected streams exclude SEC filings; HAR forecasts and daily ranks remain available to the appropriate evidence views.
- A schema-validated draft, code-generated self-check, and one confirm/revise call.
- Gemini 3.1 Pro via Vertex AI for the recorded role calls.
- Code's post-decision exposure overlay of **0.001**, i.e. **0.1% of NAV** invested, with 99.9% in cash before fees.
- Thirteen names in the initial equity mix. The record includes the composition, rationale, and submission timing.

The PM's composition and the code's exposure overlay are distinct. The PM was not shown the final overlay. A recorded 12% equity-sleeve allocation to NVDA becomes a 0.012% NAV target. The actual cash account is reduced by entry fees.

Earlier notes describe a 10% overlay and other development settings. The October 12 entry record and subsequent dated journal supersede those examples for describing what was submitted. Do not run an older sample command and assume it recreates Official.

## What is implemented

The v3 entry, validations, self-check, fallback, entry journal, and hold behavior are implemented and tested. Earlier desks implement other monitoring/review policies, but v3's proposed stage-2 escalation hierarchy is only a plan. Its entry plan conditions are stored and not acted on during Official's stage-1 hold.

## Results status

As of October 28, 2026, the official trading period is in progress. This repository claims no final rank, award, or final reproducibility approval. Research notes contain replay and modeled-field results; those are not official leaderboard results.

## Running versus inspecting

Use the offline demo to inspect the mechanism. The operational tools, live runner, credential handling, and contest submission support are preserved for provenance, but are not part of the demo. Reading this repository, running tests, or reproducing a synthetic decision does not submit a contest decision.

No contest credentials, private data, or live model responses are bundled. The organizers' final submission requirements and LLM/external-data rules remain the authoritative references for a competition reproduction package.
