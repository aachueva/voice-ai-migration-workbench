import json
from pathlib import Path

from src.evaluation import EvaluationCase, score_case


def main() -> None:
    data = json.loads(Path("data/sample_eval_cases.json").read_text())
    for item in data:
        case = EvaluationCase(
            case_id=item["case_id"],
            reference=item["reference"],
            hypothesis=item["hypothesis"],
            critical_terms=tuple(item.get("critical_terms", [])),
        )
        print(json.dumps(score_case(case)))


if __name__ == "__main__":
    main()
