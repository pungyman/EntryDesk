#!/usr/bin/env python3
"""Run the real v3 entry/check/commit path on synthetic data and scripted role outputs.

No model calls, network access, credentials, market downloads, or submissions.
This is a plumbing demonstration, not an LLM or investment-performance benchmark.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from icaif import calendar, data, sim
from icaif.agents.brains import BrainError
from icaif.agents.schemas import AnalystReport, EntryWeight, PMCheck, PMEntry
from icaif.agents.v3 import V3Config, V3Desk


def synthetic_market(seed=8):
    names = sorted(data.load_universe())
    days = [d.date() for d in pd.bdate_range('2026-01-05', periods=70)
            if d.date() not in calendar.EARLY_CLOSES]
    rng = np.random.default_rng(seed)
    vol = np.linspace(0.002, 0.01, len(names))
    prices = np.full(len(names), 100.0)
    rows = []
    for day in days:
        rounds = calendar.rounds_for(day)
        for round_ in rounds:
            prices *= np.exp(rng.normal(0, vol))
            end = (calendar.at(day, calendar.session_close(day)) if round_ == rounds[-1]
                   else round_['execution'] + pd.Timedelta(hours=1))
            rows.extend(dict(ticker=n, start=round_['execution'], end=end,
                             open=p, high=p, low=p, close=p) for n, p in zip(names, prices))
    idx = [r['execution'] for day in days for r in calendar.rounds_for(day)]
    executions = pd.DataFrame(100.0, index=idx, columns=names)
    closes = pd.DataFrame(100.0, index=[calendar.at(d, calendar.session_close(d)) for d in days], columns=names)
    return sim.Market(executions, closes, pd.DataFrame(rows)), days[62]


class DemoBrain:
    name = 'scripted-demo-no-llm'

    def __init__(self, scenario):
        self.scenario = scenario

    def decide(self, role, system, payload, schema, timeout):
        if schema is AnalystReport:
            return AnalystReport(summary='Synthetic evidence summary; no real market claim.', names=[])
        if schema is PMEntry:
            if self.scenario == 'fallback':
                raise BrainError('Demonstrated provider failure: no usable draft')
            names = [row['name'] for row in payload['names'][:5]]
            values = [0.30, 0.25, 0.20, 0.0, 0.0]
            return PMEntry(weights=[EntryWeight(name=n, weight=w) for n, w in zip(names, values)],
                           thesis='Synthetic proposal used to demonstrate the entry protocol.', conditions=[])
        if schema is PMCheck:
            if self.scenario == 'confirm':
                return PMCheck(action='confirm', revised=None, rationale='Keep the synthetic draft.')
            names = [row['name'] for row in payload['names'][:5]]
            revised = PMEntry(weights=[EntryWeight(name=n, weight=w)
                                       for n, w in zip(names, [0.20, 0.20, 0.15, 0.10, 0.10])],
                              thesis='Spread the synthetic equity mix across five names.', conditions=[])
            return PMCheck(action='revise', revised=revised,
                           rationale='Reduce concentration after reading the deterministic risk report.')
        raise BrainError(f'Unexpected role {role}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=['confirm', 'revise', 'fallback'], default='revise')
    parser.add_argument('--json', action='store_true', help='Print the recorded entry artifact')
    args = parser.parse_args()
    market, start = synthetic_market()
    brain = DemoBrain(args.scenario)
    desk = V3Desk({'quick': brain, 'deep': brain},
                  V3Config(analysts='reports_only', anonymize=False, journal_strict=False))
    result = sim.run(desk, market, start, 3)
    entry = desk.entry
    if entry is None:
        raise RuntimeError('Synthetic entry did not complete')
    expected = {'confirm': 'draft', 'revise': 'revised', 'fallback': None}[args.scenario]
    assert entry['final'] == expected, entry
    assert len([p for p in result.periods if p['traded_notional'] > 0]) == 1
    assert all(0 <= w <= 0.30 for w in entry['weights'].values())
    assert sum(entry['weights'].values()) <= 1.0
    if args.json:
        print(json.dumps(entry, indent=2))
        return
    print('ICAIF Desk v3 | synthetic inputs | scripted responses | no LLM or submission')
    print(f"Route: {entry['source']} / {entry['final'] or 'inverse-vol fallback'}")
    print(f"Invested: {entry['gross']:.2%}; unallocated target: {1-entry['gross']:.2%}")
    print('Target weights:')
    for name, weight in sorted(entry['weights'].items(), key=lambda x: -x[1]):
        print(f'  {name:8} {weight:7.2%}')
    check = entry.get('self_check', {}).get('your_book', {})
    if check:
        print(f"Draft effective number of names: {check.get('effective_names')}")
        print(f"Draft expected annual volatility: {check.get('expected_vol_ann')}")
    revised = entry.get('revised_self_check', {}).get('your_book', {})
    if revised:
        print(f"Revised effective number of names: {revised.get('effective_names')}")
    print('Verified: one entry trade; later rounds hold. Synthetic returns are not reported.')
    print('Use --json to inspect the real entry record: draft, check, revision, final weights.')


if __name__ == '__main__':
    main()
