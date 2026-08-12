import streamlit as st
import os
import time
import json
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Healthcare Multi-Agent System",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("🏥 Healthcare Management Multi-Agent System")

st.write(
    """
    A multi-agent AI system that analyzes a healthcare management
    idea, identifies the market problem, defines a 4-week MVP,
    develops the brand strategy, checks healthcare risks, and
    generates a final product launch brief.
    """
)


# ============================================================
# GROQ API CONFIGURATION
# ============================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error(
        "⚠️ GROQ_API_KEY is missing. "
        "Please add your Groq API key to Streamlit Secrets."
    )
    st.stop()


client = Groq(api_key=api_key)


# ============================================================
# GENERIC AI AGENT FUNCTION
# ============================================================

def run_agent(agent_name, persona, user_input, json_mode=False):

    start_time = time.time()

    try:

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

        latency = round(
            time.time() - start_time,
            2
        )

        return (
            response.choices[0].message.content,
            latency
        )

    except Exception as e:

        return (
            f"ERROR in {agent_name}: {str(e)}",
            0
        )


# ============================================================
# USER CONFIGURATION
# ============================================================

st.header("📝 Step 1: Configure Your Healthcare Product")


# ------------------------------------------------------------
# HEALTHCARE MANAGEMENT TYPE
# ------------------------------------------------------------

healthcare_type = st.selectbox(
    "🏥 Select Healthcare Management Type",

    [
        "Hospital Management",
        "Clinic Management",
        "Patient Management",
        "Doctor Management",
        "Pharmacy Management",
        "Appointment Management",
        "Medical Records Management",
        "Healthcare Administration"
    ]
)


# ------------------------------------------------------------
# TARGET USERS
# ------------------------------------------------------------

target_users = st.multiselect(
    "👥 Select Target Users",

    [
        "Patients",
        "Doctors",
        "Nurses",
        "Hospital Administrators",
        "Clinic Staff",
        "Pharmacists",
        "Caregivers",
        "Receptionists",
        "Healthcare Managers"
    ],

    default=[
        "Patients"
    ]
)


# ------------------------------------------------------------
# FEATURE CHECKBOXES
# ------------------------------------------------------------

st.subheader("⚙️ Select Required Features")

col1, col2, col3 = st.columns(3)


with col1:

    appointment_booking = st.checkbox(
        "📅 Appointment Booking"
    )

    patient_records = st.checkbox(
        "📋 Patient Records"
    )

    doctor_search = st.checkbox(
        "👨‍⚕️ Doctor Search"
    )

    appointment_reminders = st.checkbox(
        "🔔 Appointment Reminders"
    )


with col2:

    prescription_management = st.checkbox(
        "💊 Prescription Management"
    )

    billing_management = st.checkbox(
        "💳 Billing Management"
    )

    notifications = st.checkbox(
        "📢 Notifications"
    )

    patient_feedback = st.checkbox(
        "⭐ Patient Feedback"
    )


with col3:

    healthcare_reports = st.checkbox(
        "📊 Healthcare Reports"
    )

    hospital_management = st.checkbox(
        "🏥 Hospital Management"
    )

    staff_management = st.checkbox(
        "👨‍💼 Staff Management"
    )

    availability_tracking = st.checkbox(
        "🗓️ Doctor Availability"
    )


# ============================================================
# COLLECT SELECTED FEATURES
# ============================================================

selected_features = []


if appointment_booking:
    selected_features.append(
        "Appointment Booking"
    )

if patient_records:
    selected_features.append(
        "Patient Records"
    )

if doctor_search:
    selected_features.append(
        "Doctor Search"
    )

if appointment_reminders:
    selected_features.append(
        "Appointment Reminders"
    )

if prescription_management:
    selected_features.append(
        "Prescription Management"
    )

if billing_management:
    selected_features.append(
        "Billing Management"
    )

if notifications:
    selected_features.append(
        "Notifications"
    )

if patient_feedback:
    selected_features.append(
        "Patient Feedback"
    )

if healthcare_reports:
    selected_features.append(
        "Healthcare Reports"
    )

if hospital_management:
    selected_features.append(
        "Hospital Management"
    )

if staff_management:
    selected_features.append(
        "Staff Management"
    )

if availability_tracking:
    selected_features.append(
        "Doctor Availability"
    )


# ============================================================
# RAW HEALTHCARE IDEA
# ============================================================

st.subheader("💡 Enter Your Healthcare Idea")

raw_idea = st.text_area(

    "Describe your healthcare management product idea:",

    value=(
        "A mobile app connecting patients with local healthcare "
        "providers for easy appointment booking and healthcare management."
    ),

    height=130
)


# ============================================================
# PREVIEW USER SELECTION
# ============================================================

st.subheader("📌 Selected Configuration")


preview_col1, preview_col2 = st.columns(2)


with preview_col1:

    st.info(
        f"**Healthcare Type:** {healthcare_type}"
    )

    st.info(
        "**Target Users:** "
        + (
            ", ".join(target_users)
            if target_users
            else "None selected"
        )
    )


with preview_col2:

    st.info(
        "**Selected Features:** "
        + (
            ", ".join(selected_features)
            if selected_features
            else "None selected"
        )
    )


# ============================================================
# START MULTI-AGENT SYSTEM
# ============================================================

st.divider()


start_button = st.button(
    "🚀 Start Multi-Agent Healthcare Analysis",
    type="primary",
    use_container_width=True
)


if start_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not raw_idea.strip():

        st.warning(
            "⚠️ Please enter a healthcare product idea."
        )

        st.stop()


    if not target_users:

        st.warning(
            "⚠️ Please select at least one target user."
        )

        st.stop()


    if not selected_features:

        st.warning(
            "⚠️ Please select at least one feature."
        )

        st.stop()


    # --------------------------------------------------------
    # TOTAL LATENCY
    # --------------------------------------------------------

    total_latency = 0


    # ========================================================
    # ORCHESTRATION STATUS
    # ========================================================

    with st.status(
        "🤖 Running Healthcare Multi-Agent System...",
        expanded=True
    ) as status:


        # ====================================================
        # AGENT 1 — MARKET RESEARCHER
        # ====================================================

        st.write(
            "🔍 **Agent 1: Healthcare Market Researcher**"
        )

        researcher_persona = """

You are Agent 1: Healthcare Market Researcher.

Your job is to analyze the user's healthcare management
product idea.

Identify:

1. Target Audience
2. Market Gap
3. Core Problem

Consider the healthcare type, target users, and selected
features.

Focus specifically on healthcare management.

Do not provide medical diagnosis or treatment advice.

Return exactly three bullet points:

- Target Audience: ...
- Market Gap: ...
- Core Problem: ...

Do not add conversational text.
"""


        researcher_input = f"""

RAW HEALTHCARE IDEA:
{raw_idea}

HEALTHCARE MANAGEMENT TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

SELECTED FEATURES:
{selected_features}
"""


        research, latency = run_agent(
            "Healthcare Market Researcher",
            researcher_persona,
            researcher_input
        )


        total_latency += latency


        with st.expander(
            f"🔍 Agent 1 Results ({latency}s)",
            expanded=True
        ):

            st.write(research)


        # ====================================================
        # AGENT 2 — TECHNICAL PRODUCT MANAGER
        # ====================================================

        st.write(
            "⚙️ **Agent 2: Healthcare Technical Product Manager**"
        )


        tech_persona = """

You are Agent 2: Healthcare Technical Product Manager.

Your job is to convert the market research into a realistic
4-week Minimum Viable Product.

Choose exactly THREE core MVP features.

Prioritize features selected by the user.

The features must be realistic to implement within four weeks.

Do not add unnecessary features.

Do not include autonomous medical diagnosis.

Do not include unsupported treatment recommendations.

Format:

1. Feature Name: Description
2. Feature Name: Description
3. Feature Name: Description
"""


        tech_input = f"""

MARKET RESEARCH:
{research}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

USER SELECTED FEATURES:
{selected_features}

RAW IDEA:
{raw_idea}
"""


        tech_scope, latency = run_agent(
            "Healthcare Technical Product Manager",
            tech_persona,
            tech_input
        )


        total_latency += latency


        with st.expander(
            f"⚙️ Agent 2 Results ({latency}s)",
            expanded=True
        ):

            st.write(tech_scope)


        # ====================================================
        # AGENT 3 — BRAND STRATEGIST
        # ====================================================

        st.write(
            "✨ **Agent 3: Healthcare Brand Strategist**"
        )


        brand_persona = """

You are Agent 3: Healthcare Brand Strategist.

Your job is to create the brand positioning for the
healthcare management product.

Return exactly two lines:

Brand Positioning:
Two sentences describing the product's value proposition.

Brand Tone:
Exactly three keywords.

The brand should communicate:

- Trust
- Reliability
- Accessibility
- Simplicity
- Patient-centered care

Do not make unsupported medical claims.
"""


        brand_input = f"""

MARKET RESEARCH:
{research}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

SELECTED FEATURES:
{selected_features}

RAW IDEA:
{raw_idea}
"""


        brand_strategy, latency = run_agent(
            "Healthcare Brand Strategist",
            brand_persona,
            brand_input
        )


        total_latency += latency


        with st.expander(
            f"✨ Agent 3 Results ({latency}s)",
            expanded=True
        ):

            st.write(brand_strategy)


        # ====================================================
        # AGENT 4 — QUALITY & SAFETY CRITIC
        # ====================================================

        st.write(
            "⚖️ **Agent 4: Healthcare Quality & Safety Critic**"
        )


        critic_persona = """

You are Agent 4: Healthcare Quality and Safety Critic.

Your job is to review the proposed technical MVP and
brand strategy.

Look for conflicts involving:

- Patient safety
- Privacy
- Sensitive healthcare information
- Unrealistic medical claims
- Reliability
- Feature overload
- User expectations

Explain what should be changed if a problem exists.

If there are no major conflicts, write:

No conflicts identified.
"""


        critic_input = f"""

TECHNICAL MVP:

{tech_scope}


BRAND STRATEGY:

{brand_strategy}


HEALTHCARE TYPE:

{healthcare_type}


TARGET USERS:

{target_users}


SELECTED FEATURES:

{selected_features}
"""


        critique, latency = run_agent(
            "Healthcare Quality and Safety Critic",
            critic_persona,
            critic_input
        )


        total_latency += latency


        with st.expander(
            f"⚖️ Agent 4 Results ({latency}s)",
            expanded=True
        ):

            st.write(critique)


        # ====================================================
        # AGENT 5 — LEAD SYNTHESIZER
        # ====================================================

        st.write(
            "🚀 **Agent 5: Lead Healthcare Product Synthesizer**"
        )


        synthesizer_persona = """

You are Agent 5: Lead Healthcare Product Synthesizer.

You are responsible for producing the final healthcare
product launch brief.

Combine:

1. Market Research
2. Technical MVP
3. Brand Strategy
4. Quality Critique

Resolve the concerns identified by Agent 4.

Return ONLY valid JSON.

Use exactly this structure:

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

Rules:

- Keep the product focused on healthcare management.
- Keep the MVP realistic for four weeks.
- Do not make unsupported medical claims.
- Do not provide medical diagnosis.
- Do not provide autonomous treatment recommendations.
- Return valid JSON only.
"""


        synthesizer_input = f"""

RAW IDEA:
{raw_idea}


HEALTHCARE TYPE:
{healthcare_type}


TARGET USERS:
{target_users}


SELECTED FEATURES:
{selected_features}


MARKET RESEARCH:
{research}


TECHNICAL MVP:
{tech_scope}


BRAND STRATEGY:
{brand_strategy}


QUALITY CRITIQUE:
{critique}
"""


        final_brief, latency = run_agent(
            "Lead Healthcare Product Synthesizer",
            synthesizer_persona,
            synthesizer_input,
            json_mode=True
        )


        total_latency += latency


        # ----------------------------------------------------
        # UPDATE STATUS
        # ----------------------------------------------------

        status.update(
            label=(
                "✅ Multi-Agent Healthcare Analysis Complete!"
                f" Total Time: {round(total_latency, 2)} seconds"
            ),
            state="complete",
            expanded=False
        )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    st.divider()

    st.header("🎯 Final Healthcare Product Brief")


    try:

        result = json.loads(final_brief)


        # ----------------------------------------------------
        # PRODUCT NAME
        # ----------------------------------------------------

        st.title(
            f"🏥 {result.get('product_name', 'Healthcare Product')}"
        )


        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        info_col1, info_col2 = st.columns(2)


        with info_col1:

            st.success(
                f"**Healthcare Type:** "
                f"{result.get('healthcare_type', '')}"
            )


        with info_col2:

            st.success(
                f"**Target Audience:** "
                f"{result.get('target_audience', '')}"
            )


        # ----------------------------------------------------
        # MVP FEATURES
        # ----------------------------------------------------

        st.subheader(
            "⚙️ Four-Week MVP Features"
        )


        features = result.get(
            "four_week_v1_features",
            []
        )


        for feature in features:

            st.checkbox(
                feature,
                value=True,
                disabled=True
            )


        # ----------------------------------------------------
        # BRAND POSITIONING
        # ----------------------------------------------------

        st.subheader(
            "✨ Brand Positioning"
        )


        st.info(
            result.get(
                "brand_positioning",
                "No brand positioning generated."
            )
        )


        # ----------------------------------------------------
        # RESOLVED TRADEOFFS
        # ----------------------------------------------------

        st.subheader(
            "⚖️ Resolved Tradeoffs"
        )


        st.warning(
            result.get(
                "resolved_tradeoffs",
                "No tradeoffs identified."
            )
        )


        # ----------------------------------------------------
        # AGENT SUMMARY
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "🤖 Multi-Agent Execution Summary"
        )


        summary_col1, summary_col2, summary_col3 = st.columns(3)


        with summary_col1:

            st.metric(
                "Agents Used",
                "5"
            )


        with summary_col2:

            st.metric(
                "MVP Features",
                len(features)
            )


        with summary_col3:

            st.metric(
                "Total Processing Time",
                f"{round(total_latency, 2)}s"
            )


        # ----------------------------------------------------
        # FINAL JSON
        # ----------------------------------------------------

        with st.expander(
            "🔎 View Final JSON"
        ):

            st.json(result)


    except Exception as e:

        st.error(
            "⚠️ The final AI response could not be parsed as JSON."
        )

        st.write(
            f"Error: {str(e)}"
        )

        st.subheader(
            "Raw AI Response"
        )

        st.code(
            final_brief
        )
