# Provider Migration Rollout Strategy

## Baseline
Measure the incumbent against a representative, human-reviewed evaluation set. Segment results by call type, noise condition, domain vocabulary, and other business-relevant cohorts.

## Shadow
Send eligible traffic to both systems while only the incumbent output feeds production workflows. Compare quality, latency, failures, and cost without introducing downstream risk.

## Canary
Route a small controlled percentage to the candidate. Define rollback gates before launch, such as elevated error rate, p95 latency regression, critical-field regression, or downstream validation failures.

## Expand
Increase traffic in stages only after quality and operational gates remain stable. Continue segmented monitoring because aggregate averages can hide regressions.

## Cutover
Make the candidate primary after acceptance criteria are met. Retain the adapter boundary and rollback path until the migration is operationally stable.

## Discovery questions

- Which workflows are business-critical?
- Which transcription errors create downstream harm?
- What is the incumbent baseline?
- Which metrics are launch blockers versus monitoring signals?
- Who owns the evaluation dataset and sign-off?
- What traffic is safe for the first canary?
- What is the rollback threshold?
- Which downstream contract must remain stable during migration?
