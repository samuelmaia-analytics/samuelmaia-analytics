from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import get_settings
from core.analytics_engineering import run_analytics_engineering_checks
from core.governance_policy import build_governance_policy_report
from core.pipeline import build_portfolio_snapshot
from core.runtime_config import build_runtime_config_summary


settings = get_settings()

st.title("Governance and Quality")
st.caption("Operational governance, quality controls, and contract-aware portfolio evidence.")

snapshot = build_portfolio_snapshot(settings)
quality_report = snapshot["quality_report"]
runtime_config = build_runtime_config_summary(settings)
policy_report = build_governance_policy_report(settings)
analytics_report = run_analytics_engineering_checks(settings)

col1, col2, col3 = st.columns(3)
col1.metric("Total Checks", f"{quality_report['total_checks']}")
col2.metric("Passed Checks", f"{quality_report['passed_checks']}")
col3.metric("Pass Rate", f"{quality_report['pass_rate']:.1f}%")

st.subheader("Detailed Quality Results")
st.dataframe(quality_report["results"], width="stretch", hide_index=True)

st.subheader("Governance Signals")
st.markdown(
    """
    - Versioned contracts validate generated artifacts
    - Structured observability events are emitted on pipeline runs
    - Semantic metrics are exported for downstream SQL and dbt-style usage
    - Repository registry tracks local reference assets and their readiness
    """
)

st.subheader("Runtime Configuration")
auth = runtime_config["auth"]
genai = runtime_config["genai"]
thresholds = runtime_config["change_driver_thresholds"]

cfg1, cfg2, cfg3 = st.columns(3)
cfg1.metric("Auth Mode", str(auth["mode"]).upper())
cfg2.metric("GenAI Provider", str(genai["provider"]))
cfg3.metric("Change Critical Threshold", f"{thresholds['critical']:.1f}")

st.caption("Sanitized runtime summary for operational review. Secrets are never rendered.")
st.json(runtime_config)

st.subheader("Policy Checks")
pol1, pol2 = st.columns(2)
pol1.metric("Policy Status", str(policy_report["status"]).upper())
pol2.metric("Checks", f"{len(policy_report['checks'])}")
st.caption(policy_report["summary"])
st.dataframe(policy_report["checks"], width="stretch", hide_index=True)

st.subheader("Analytics Engineering Checks")
ae1, ae2, ae3 = st.columns(3)
ae1.metric("AE Status", str(analytics_report["status"]).upper())
ae2.metric("Models Built", f"{analytics_report['models_built']}")
ae3.metric("Failed Tests", f"{analytics_report['failed_tests']}")
st.caption("dbt-like local validation over the SQLite warehouse for sources, models, and SQL tests.")
st.dataframe(analytics_report["results"], width="stretch", hide_index=True)
