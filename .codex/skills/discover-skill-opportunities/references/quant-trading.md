# Quantitative trading opportunity patterns

## High-value recurring clusters

| Cluster | Evidence signals | Likely reusable contents | Validation |
|---|---|---|---|
| Data ingestion and quality control | Repeated vendor pulls, adjustments, missing-data repair | adapters, schema, freshness and survivorship checks | point-in-time and quality tests pass |
| Hypothesis and factor research | Reused transformations, neutralization, IC analysis | research protocol, factor library, notebook template | out-of-sample and robustness tests |
| Backtest review | Repeated leakage, cost, turnover, exposure checks | backtest audit rubric, metric scripts | no look-ahead; costs and constraints modeled |
| Portfolio construction and risk | Recurring optimization, limits, rebalance logic | constraint schema, exposure reports, stress tests | limits, concentration and scenario tests pass |
| Signal-to-execution handoff | Repeated order sizing, liquidity and slippage checks | execution contract, broker adapter, kill-switch checklist | paper/shadow execution reconciliation |
| Strategy monitoring and attribution | Recurring drift, PnL decomposition, alert review | monitoring thresholds, attribution scripts | alerts and attribution reconcile to books |

## Good skill boundaries

Separate research, validation, portfolio construction, and live execution when permissions and failure costs differ. Prefer deterministic code for calculations; use a skill to orchestrate evidence, decisions, controls, and interpretation.

## Candidate evidence

Look for copied notebooks, repeated data repairs, parameter sweeps without protocol, recurring post-hoc explanations, manual broker reconciliation, or the same risk questions before each deployment.

## Risk controls

Require point-in-time data, transaction costs, liquidity, corporate-action handling, survivorship checks, out-of-sample tests, sensitivity analysis, and explicit market timestamps. Never infer live executability from stale or incomplete data. Require human approval and platform controls for orders, leverage, capital allocation, and production deployment.
