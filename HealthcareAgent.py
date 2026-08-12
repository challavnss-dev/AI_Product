import streamlit as st
import os
import time
import json
from groq import Groq


# =========================================================
# STREAMLIT CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Healthcare Multi-Agent System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Management Multi-Agent System")

st.write(
    "A multi-agent AI system that analyzes a healthcare idea, "
    "defines the MVP, creates branding, checks risks, and "
    "generates a final launch plan."
)


# =========================================================
# GROQ CONNECTION
# =========================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error("⚠️ GROQ_API_KEY is missing.")
    st.stop()

client = Groq(api_key=api_key)


# =========================================================
# GENERIC AGENT FUNCTION
# =========================================================

def run_agent(agent_name, persona, user_input, json_mode=False):

    start_time = time.time()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": persona
            },
            {
                "role": "user",
                "content": user_input
            }
        ],

        temperature=0.2,

        response_format=(
            {"type": "json_object"}
            if json_mode
            else {"type": "text"}
        )
    )

    latency = round(time.time() - start_time, 2)

    return response.choices[0].message.content, latency


# =========================================================
# USER INPUT
# =========================================================

st.header("1️⃣ Healthcare Product Configuration")


healthcare_type = st.selectbox(
    "Select Healthcare Management Type",
    [
        "Hospital Management",
        "Clinic Management",
        "Patient Management",
        "Doctor Management",
        "Pharmacy Management",
        "Appointment Management"
    ]
)


target_users = st.multiselect(
    "Select Target Users",
    [
        "Patients",
        "Doctors",
        "Nurses",
        "Hospital Administrators",
        "Clinic Staff",
        "Pharmacists",
        "Caregivers"
    ],
    default=["Patients"]
)


st.subheader("Select Required Features")

col1, col2, col3 = st.columns(3)

with col1:

    appointment = st.checkbox(
        "📅 Appointment Booking"
    )

    records = st.checkbox(
        "📋 Patient Records"
    )

    doctor_search = st.checkbox(
        "👨‍⚕️ Doctor Search"
    )


with col2:

    reminders = st.checkbox(
        "🔔 Appointment Reminders"
    )

    prescription = st.checkbox(
        "💊 Prescription Management"
    )

    billing = st.checkbox(
        "💳 Billing"
    )


with col3:

    notifications = st.checkbox(
        "📢 Notifications"
    )

    reports = st.checkbox(
        "📊 Healthcare Reports"
    )

    hospital = st.checkbox(
        "🏥 Hospital Management"
    )


raw_idea = st.text_area(
    "Enter your healthcare idea",

    value=(
        "A mobile application that helps patients "
        "find healthcare providers and manage appointments."
    )
)


# =========================================================
# COLLECT FEATURES
# =========================================================

selected_features = []

if appointment:
    selected_features.append("Appointment Booking")

if records:
    selected_features.append("Patient Records")

if doctor_search:
    selected_features.append("Doctor Search")

if reminders:
    selected_features.append("Appointment Reminders")

if prescription:
    selected_features.append("Prescription Management")

if billing:
    selected_features.append("Billing")

if notifications:
    selected_features.append("Notifications")

if reports:
    selected_features.append("Healthcare Reports")

if hospital:
    selected_features.append("Hospital Management")


# =========================================================
# START MULTI-AGENT SYSTEM
# =========================================================

if st.button(
    "🚀 Start Multi-Agent Healthcare Analysis",
    type="primary"
):

    if not raw_idea:
        st.warning("Please enter a healthcare idea.")
        st.stop()

    if not target_users:
        st.warning("Please select target users.")
        st.stop()

    if not selected_features:
        st.warning("Please select at least one feature.")
        st.stop()


    total_latency = 0


    # =====================================================
    # AGENT 1
    # =====================================================

    st.divider()

    st.header("🤖 Agent 1 — Healthcare Market Researcher")

    researcher_persona = """
You are Agent 1, a Healthcare Market Researcher.

Your responsibility is to analyze the healthcare product idea.

Identify:

- Target Audience
- Market Gap
- Core Problem

Focus on healthcare management.

Return exactly three bullet points.
"""

    research, latency = run_agent(
        "Healthcare Market Researcher",
        researcher_persona,

        f"""
HEALTHCARE IDEA:
{raw_idea}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

SELECTED FEATURES:
{selected_features}
"""
    )

    total_latency += latency

    st.write(research)

    st.caption(
        f"Agent 1 completed in {latency} seconds"
    )


    # =====================================================
    # AGENT 2
    # =====================================================

    st.divider()

    st.header("🤖 Agent 2 — Healthcare Technical PM")

    tech_persona = """
You are Agent 2, a Healthcare Technical Product Manager.

Your responsibility is to convert market research into
a realistic 4-week MVP.

Select exactly three core features.

Prioritize features selected by the user.

Do not add unnecessary features.

Do not provide medical diagnosis or treatment.
"""

    tech_scope, latency = run_agent(
        "Healthcare Technical PM",
        tech_persona,

        f"""
MARKET RESEARCH:
{research}

USER SELECTED FEATURES:
{selected_features}

HEALTHCARE TYPE:
{healthcare_type}
"""
    )

    total_latency += latency

    st.write(tech_scope)

    st.caption(
        f"Agent 2 completed in {latency} seconds"
    )


    # =====================================================
    # AGENT 3
    # =====================================================

    st.divider()

    st.header("🤖 Agent 3 — Healthcare Brand Strategist")

    brand_persona = """
You are Agent 3, a Healthcare Brand Strategist.

Your responsibility is to create a trustworthy healthcare
brand strategy.

Return:

Brand Positioning:
Two sentences explaining the value proposition.

Brand Tone:
Exactly three keywords.

Focus on trust, accessibility, reliability and
patient-centered healthcare.
"""

    brand_strategy, latency = run_agent(
        "Healthcare Brand Strategist",
        brand_persona,

        f"""
MARKET RESEARCH:
{research}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}
"""
    )

    total_latency += latency

    st.write(brand_strategy)

    st.caption(
        f"Agent 3 completed in {latency} seconds"
    )


    # =====================================================
    # AGENT 4
    # =====================================================

    st.divider()

    st.header("🤖 Agent 4 — Healthcare Quality Critic")

    critic_persona = """
You are Agent 4, a Healthcare Quality and Safety Critic.

Your responsibility is to review the proposed MVP and
brand strategy.

Look for conflicts involving:

- Patient safety
- Privacy
- Sensitive healthcare information
- Unrealistic medical claims
- Reliability
- Excessive features

Return a concise critique.

If there are no major issues, say:
No conflicts identified.
"""

    critique, latency = run_agent(
        "Healthcare Quality Critic",
        critic_persona,

        f"""
TECHNICAL MVP:
{tech_scope}

BRAND STRATEGY:
{brand_strategy}

HEALTHCARE TYPE:
{healthcare_type}

SELECTED FEATURES:
{selected_features}
"""
    )

    total_latency += latency

    st.write(critique)

    st.caption(
        f"Agent 4 completed in {latency} seconds"
    )


    # =====================================================
    # AGENT 5
    # =====================================================

    st.divider()

    st.header("🤖 Agent 5 — Lead Healthcare Synthesizer")

    synthesizer_persona = """
You are Agent 5, the Lead Healthcare Product Synthesizer.

Your responsibility is to combine the outputs from all
previous agents.

Resolve the critic's concerns.

Return ONLY valid JSON.

Use this schema:

{
    "product_name": "string",
    "healthcare_type": "string",
    "target_audience": "string",
    "four_week_v1_features": [
        "feature 1",
        "feature 2",
        "feature 3"
    ],
    "brand_positioning": "string",
    "resolved_tradeoffs": "string"
}

The product must remain a healthcare management product.

Do not make unsupported medical claims.
"""

    final_brief, latency = run_agent(
        "Lead Healthcare Synthesizer",
        synthesizer_persona,

        f"""
MARKET RESEARCH:
{research}

TECHNICAL MVP:
{tech_scope}

BRAND STRATEGY:
{brand_strategy}

QUALITY CRITIQUE:
{critique}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

SELECTED FEATURES:
{selected_features}
""",

        json_mode=True
    )

    total_latency += latency


    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    st.divider()

    st.header("🎯 Final Multi-Agent Result")

    try:

        result = json.loads(final_brief)

        st.subheader(
            f"🏥 {result.get('product_name')}"
        )

        st.write(
            f"**Healthcare Type:** "
            f"{result.get('healthcare_type')}"
        )

        st.write(
            f"**Target Audience:** "
            f"{result.get('target_audience')}"
        )

        st.subheader(
            "⚙️ 4-Week MVP Features"
        )

        for feature in result.get(
            "four_week_v1_features",
            []
        ):

            st.checkbox(
                feature,
                value=True,
                disabled=True
            )

        st.subheader(
            "✨ Brand Positioning"
        )

        st.info(
            result.get(
                "brand_positioning",
                ""
            )
        )

        st.subheader(
            "⚖️ Resolved Tradeoffs"
        )

        st.warning(
            result.get(
                "resolved_tradeoffs",
                ""
            )
        )


    except Exception:

        st.error(
            "Unable to parse the final JSON response."
        )

        st.write(final_brief)


    st.success(
        f"✅ All 5 agents completed. "
        f"Total processing time: {round(total_latency, 2)} seconds"
    )
