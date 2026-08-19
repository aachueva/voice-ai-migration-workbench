from __future__ import annotations

import re
from dataclasses import dataclass


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def word_error_rate(reference: str, hypothesis: str) -> float:
    ref, hyp = _tokens(reference), _tokens(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    previous = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        current = [i]
        for j, h in enumerate(hyp, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (r != h)))
        previous = current
    return previous[-1] / len(ref)


def critical_term_recall(reference: str, hypothesis: str, terms: tuple[str, ...]) -> float:
    relevant = [t for t in terms if t.lower() in reference.lower()]
    if not relevant:
        return 1.0
    found = sum(t.lower() in hypothesis.lower() for t in relevant)
    return found / len(relevant)


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    reference: str
    hypothesis: str
    critical_terms: tuple[str, ...] = ()


def score_case(case: EvaluationCase) -> dict[str, float | str]:
    return {
        "case_id": case.case_id,
        "wer": round(word_error_rate(case.reference, case.hypothesis), 4),
        "critical_term_recall": round(critical_term_recall(case.reference, case.hypothesis, case.critical_terms), 4),
    }
