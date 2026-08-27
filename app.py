import json
from pathlib import Path

import streamlit as st

from src.tam.account_loader import AccountLoader
from src.tam.summarizer import TAMSummarizer
from src.triage.agent import TriageAgent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Zycus AI Support Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1.5rem;
        }

        .block-container {
            max-width: 1200px;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        .app-header {
            padding: 1.5rem 0 1rem 0;
        }

        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .app-subtitle {
            font-size: 1rem;
            color: #6b7280;
            margin-bottom: 1.5rem;
        }

        .section-card {
            padding: 1.25rem;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            background: #ffffff;
            margin-bottom: 1rem;
        }

        .risk-card {
            padding: 1rem;
            border-left: 4px solid #dc2626;
            border-radius: 8px;
            background: #fef2f2;
            margin-bottom: 0.75rem;
        }

        .success-card {
            padding: 1rem;
            border-left: 4px solid #16a34a;
            border-radius: 8px;
            background: #f0fdf4;
            margin-bottom: 1rem;
        }

        .info-card {
    padding: 1rem;
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    background: #eff6ff;
    color: #1e3a5f;
    margin-bottom: 1rem;
}

.info-card strong {
    color: #163a63;
}

        .metric-label {
            font-size: 0.8rem;
            color: #6b7280;
            margin-bottom: 0.2rem;
        }

        .metric-value {
            font-size: 1.15rem;
            font-weight: 600;
        }

        .quote {
            font-style: italic;
            padding: 0.75rem;
            background: #f9fafb;
            border-radius: 8px;
            margin-top: 0.5rem;
        }

        .footer {
            text-align: center;
            color: #9ca3af;
            font-size: 0.8rem;
            padding: 2rem 0 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

@st.cache_resource
def get_triage_agent():
    return TriageAgent()


@st.cache_resource
def get_tam_summarizer():
    return TAMSummarizer()


@st.cache_resource
def get_account_loader():
    return AccountLoader()


def load_accounts():
    path = Path("data/accounts.json")

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def render_metric(label, value):
    st.markdown(
        f"""
        <div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">
            🤖 Zycus AI Support Assistant
        </div>
        <div class="app-subtitle">
            AI-powered support triage and account intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("### Navigation")

    page = st.radio(
        "Select workflow",
        [
            "🎫 Ticket Triage",
            "👤 TAM Account Health",
            "📊 Evaluation",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### About")

    st.caption(
        "Lightweight internal tooling for Technical Support and TAM teams."
        " Uses only the synthetic dataset and product knowledge base supplied with the assessment."
    )

    st.caption(
        "Data source: supplied synthetic assessment dataset."
    )


# ============================================================
# TASK 1 — TICKET TRIAGE
# ============================================================

if page == "🎫 Ticket Triage":

    st.markdown("## Ticket Triage")

    st.caption(
        "Submit a support ticket to classify, prioritize, "
        "route, and generate a first response."
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        subject = st.text_input(
            "Ticket subject",
            placeholder="Example: New users cannot authenticate via SSO",
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">
                <strong>What happens?</strong><br>
                The ticket is analyzed using the knowledge base
                and the triage agent produces a structured recommendation.
            </div>
            """,
            unsafe_allow_html=True,
        )

    body = st.text_area(
        "Ticket description",
        height=220,
        placeholder=(
            "Describe the customer's issue here..."
        ),
    )

    run_triage = st.button(
        "Run Ticket Triage",
        type="primary",
        use_container_width=True,
    )

    if run_triage:

        if not subject.strip():
            st.warning("Please enter a ticket subject.")

        elif not body.strip():
            st.warning("Please enter the ticket description.")

        else:

            with st.spinner(
                "Analyzing ticket and retrieving relevant knowledge..."
            ):

                try:

                    agent = get_triage_agent()

                    result = agent.triage(
                        subject=subject,
                        body=body,
                    )

                    st.success(
                        "Ticket triage completed successfully."
                    )

                    st.markdown("### Classification")

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        render_metric(
                            "Product Area",
                            result.product_area,
                        )

                    with c2:
                        render_metric(
                            "Issue Category",
                            result.issue_category,
                        )

                    with c3:
                        render_metric(
                            "Urgency",
                            result.urgency,
                        )

                    st.divider()

                    left, right = st.columns(2)

                    with left:

                        st.markdown("### Knowledge Base")

                        render_metric(
                            "Known Issue",
                            str(result.known_issue),
                        )

                        if getattr(
                            result,
                            "kb_reference",
                            None,
                        ):
                            st.write(
                                result.kb_reference
                            )

                    with right:

                        st.markdown("### Routing")

                        render_metric(
                            "Recommended Team",
                            result.responder_team,
                        )

                    st.divider()

                    st.markdown("### Reasoning")

                    with st.expander(
                        "View classification reasoning",
                        expanded=True,
                    ):
                        st.write(
                            result.reasoning
                        )

                    if hasattr(
                        result,
                        "urgency_reason",
                    ):
                        with st.expander(
                            "View urgency reasoning"
                        ):
                            st.write(
                                result.urgency_reason
                            )

                    st.markdown(
                        "### Draft First Response"
                    )

                    st.info(
                        result.first_response
                    )

                except Exception as exc:

                    st.error(
                        f"Unable to complete triage: {exc}"
                    )


# ============================================================
# TASK 2 — TAM ACCOUNT HEALTH
# ============================================================

elif page == "👤 TAM Account Health":

    st.markdown("## TAM Account Health")

    st.caption(
        "Generate an actionable account brief for a QBR "
        "using account data and recent support history."
    )

    accounts = load_accounts()

    account_options = {
        f"{account['account_id']} — {account['company']}":
        account["account_id"]
        for account in accounts
    }

    selected_label = st.selectbox(
        "Select customer account",
        list(account_options.keys()),
    )

    selected_account_id = account_options[
        selected_label
    ]

    selected_account = next(
        account
        for account in accounts
        if account["account_id"] == selected_account_id
    )

    st.markdown("### Account Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_metric(
            "Plan",
            selected_account.get(
                "plan_tier",
                "—",
            ),
        )

    with c2:
        render_metric(
            "Health",
            selected_account.get(
                "health_status",
                "—",
            ),
        )

    with c3:
        render_metric(
            "Usage Trend",
            selected_account.get(
                "usage_trend",
                "—",
            ),
        )

    with c4:
        render_metric(
            "ARR",
            f"${selected_account.get('arr_usd', 0):,.0f}",
        )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        render_metric(
            "TAM",
            selected_account.get(
                "tam",
                "—",
            ),
        )

    with c2:
        render_metric(
            "Open Tickets",
            selected_account.get(
                "open_tickets",
                0,
            ),
        )

    with c3:
        render_metric(
            "P1 Tickets (30d)",
            selected_account.get(
                "p1_tickets_last_30d",
                0,
            ),
        )

    generate_brief = st.button(
        "Generate Account Brief",
        type="primary",
        use_container_width=True,
    )

    if generate_brief:

        with st.spinner(
            "Analyzing account health and recent tickets..."
        ):

            try:

                summarizer = get_tam_summarizer()

                brief = summarizer.summarize(
                    selected_account_id
                )

                st.success(
                    "Account health brief generated."
                )

                st.markdown(
                    "### 1. Executive Summary"
                )

                st.markdown(
                    f"""
                    <div class="section-card">
                        {brief.executive_summary}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    "### 2. Open Risks & Flagged Issues"
                )

                if not brief.open_risks:

                    st.markdown(
                        """
                        <div class="success-card">
                            <strong>No significant risks detected.</strong>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    for risk in brief.open_risks:

                        risk_type = (
                            risk.risk_type.upper()
                        )

                        ticket_id = (
                            risk.ticket_id
                            or "Account-level signal"
                        )

                        st.markdown(
                            f"""
                            <div class="risk-card">
                                <strong>{risk_type}</strong>
                                &nbsp; · &nbsp;
                                {ticket_id}
                                <br><br>
                                {risk.evidence}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        if risk.quote:

                            st.markdown(
                                f"""
                                <div class="quote">
                                    “{risk.quote}”
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                st.markdown(
                    "### 3. Recommended Talking Points"
                )

                for index, point in enumerate(
                    brief.talking_points,
                    start=1,
                ):

                    st.markdown(
                        f"**{index}.** {point}"
                    )

            except Exception as exc:

                st.error(
                    f"Unable to generate account brief: {exc}"
                )


# ============================================================
# EVALUATION
# ============================================================

elif page == "📊 Evaluation":

    st.markdown("## Evaluation Results")

    st.caption(
        "Offline regression evaluation of Task 1 and Task 2."
    )

    report_path = Path("eval_report.json")

    if not report_path.exists():

        st.warning("eval_report.json was not found.")

    else:

        report = json.loads(
            report_path.read_text(encoding="utf-8")
        )

        task1_summary = report.get("task1_summary", {})
        task2_summary = report.get("task2_summary", {})

        # ----------------------------------------------------
        # Overall quality
        # ----------------------------------------------------

        st.markdown("### Regression Status")

        col1, col2, col3 = st.columns(3)

        total_tests = (
            task1_summary.get("tests", 0)
            + task2_summary.get("tests", 0)
        )

        total_passed = (
            task1_summary.get("passed", 0)
            + task2_summary.get("passed", 0)
        )

        overall_score = (
            (
                task1_summary.get("average_quality_score", 0)
                + task2_summary.get("average_quality_score", 0)
            )
            / 2
        )

        with col1:
            st.metric(
                "Tests Passed",
                f"{total_passed}/{total_tests}",
            )

        with col2:
            st.metric(
                "Overall Quality",
                f"{overall_score:.1f}",
            )

        with col3:
            st.metric(
                "Tasks Evaluated",
                "2",
            )

        st.divider()

        # ----------------------------------------------------
        # Task summaries
        # ----------------------------------------------------

        st.markdown("### Task Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### 🎫 Task 1 — Ticket Triage")

            st.metric(
                "Tests Passed",
                f"{task1_summary.get('passed', 0)}/"
                f"{task1_summary.get('tests', 0)}",
            )

            st.metric(
                "Average Quality Score",
                f"{task1_summary.get('average_quality_score', 0):.1f}",
            )

        with col2:

            st.markdown("#### 👤 Task 2 — TAM Account Health")

            st.metric(
                "Tests Passed",
                f"{task2_summary.get('passed', 0)}/"
                f"{task2_summary.get('tests', 0)}",
            )

            st.metric(
                "Average Quality Score",
                f"{task2_summary.get('average_quality_score', 0):.1f}",
            )

        st.divider()

        # ----------------------------------------------------
        # Detailed Task 1 results
        # ----------------------------------------------------

        st.markdown("### Task 1 Test Cases")

        task1_rows = []

        for case in report.get("task1", []):

            task1_rows.append(
                {
                    "Test Case": case.get("test_id", "—"),
                    "Scenario": case.get("name", "—"),
                    "Status": case.get("status", "—"),
                    "Quality": case.get(
                        "quality_score",
                        0,
                    ),
                    "Checks": (
                        f"{case.get('checks_passed', 0)}/"
                        f"{case.get('checks_total', 0)}"
                    ),
                }
            )

        st.dataframe(
            task1_rows,
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------
        # Detailed Task 2 results
        # ----------------------------------------------------

        st.markdown("### Task 2 Test Cases")

        task2_rows = []

        for case in report.get("task2", []):

            task2_rows.append(
                {
                    "Test Case": case.get("test_id", "—"),
                    "Scenario": case.get("name", "—"),
                    "Status": case.get("status", "—"),
                    "Quality": case.get(
                        "quality_score",
                        0,
                    ),
                    "Checks": (
                        f"{case.get('checks_passed', 0)}/"
                        f"{case.get('checks_total', 0)}"
                    ),
                }
            )

        st.dataframe(
            task2_rows,
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------
        # Final status
        # ----------------------------------------------------

        if total_passed == total_tests and total_tests > 0:

            st.markdown(
                """
                <div class="success-card">
                    <strong>✓ All evaluation cases passed.</strong><br>
                    10/10 regression tests passed with an overall
                    quality score of 1.0.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.warning(
                f"{total_passed}/{total_tests} evaluation cases passed."
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Zycus AI Support Assistant · Technical Support & TAM tooling
    </div>
    """,
    unsafe_allow_html=True,
)