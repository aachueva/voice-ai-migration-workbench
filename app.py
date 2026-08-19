"""Streamlit UI for the Voice AI Migration & Evaluation Workbench."""

import json
from pathlib import Path

import streamlit as st

from src.evaluation import EvaluationCase, score_case

st.set_page_config(page_title="Migration Control Center", layout="wide")
st.title("Migration Control Center")
st.caption("Compare transcription quality, preserve downstream workflows, and plan a reversible provider migration.")

with st.sidebar:
    st.header("Migration controls")
    mode = st.selectbox("Migration mode", ["Baseline", "Shadow", "Canary", "Candidate primary"])
    st.info(f"Current mode: {mode}")

st.subheader("Evaluation overview")
st.write(
    "This portfolio prototype compares an incumbent and candidate speech-to-text system using "
    "human-reference accuracy and business-critical terminology. All included examples are synthetic."
)

with open("data/sample_eval_cases.json", encoding="utf-8") as f:
    cases = json.load(f)

rows = []
for raw in cases:
    case = EvaluationCase(
        case_id=raw["case_id"],
        reference=raw["reference"],
        hypothesis=raw["hypothesis"],
        critical_terms=tuple(raw.get("critical_terms", [])),
    )
    rows.append(score_case(case))

c1, c2, c3 = st.columns(3)
avg_wer = sum(float(r["wer"]) for r in rows) / len(rows)
avg_recall = sum(float(r["critical_term_recall"]) for r in rows) / len(rows)
c1.metric("Average WER", f"{avg_wer * 100:.1f}%")
c2.metric("Critical-term recall", f"{avg_recall * 100:.1f}%")
c3.metric("Rollout stage", mode)

st.subheader("Evaluation cases")
st.dataframe(rows, use_container_width=True)

st.subheader("Production gates")
g1, g2, g3 = st.columns(3)
g1.metric("Quality", "WER + critical fields")
g2.metric("Reliability", "p95 latency + failures")
g3.metric("Rollout", "Canary + rollback")

st.caption("Provider-neutral portfolio prototype. No customer, proprietary, or hiring-assessment data is included.")
