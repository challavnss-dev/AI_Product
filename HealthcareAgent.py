import streamlit as st
import os
import time
import json
from groq import Groq

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Healthcare Management Launch Syndicate",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Management Launch Syndicate")
st.write(
    "Multi-Agent AI system for planning a healthcare management "
    "product and creating a 4-week MVP."
)

# =========================================================
# GROQ API CONFIGURATION
# =========================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error(
        "⚠️ Groq API Key missing! "
        "Please configure GROQ_API_KEY in Streamlit Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# =========================================================
# AI AGENT FUNCTION
# =========================================================

def run_agent(persona, prompt_input, json_mode=False):

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
                "content": prompt_input
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
# USER INPUT SECTION
# =========================================================

st.header("📝 Healthcare Product Configuration")

# ---------------------------------------------------------
# OPTION SELECTION
# ---------------------------------------------------------

st.subheader("1. Select Healthcare Management Type")

healthcare_type = st.radio(
    "Choose one:",
    [
        "Hospital Management",
        "Clinic Management",
        "Patient Management",
        "Doctor Management",
        "Pharmacy Management",
        "Appointment Management"
    ]
)


# ---------------------------------------------------------
# CHECKBOXES
# ---------------------------------------------------------

st.subheader("2. Select Features You Want")

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

with col2:
    reminders = st.checkbox(
        "🔔 Appointment Reminders"
    )

    prescription_management = st.checkbox(
        "💊 Prescription Management"
    )

    hospital_management = st.checkbox(
        "🏥 Hospital Management"
    )

with col3:
    billing = st.checkbox(
        "💳 Billing Management"
    )

    notifications = st.checkbox(
        "📢 Notifications"
    )

    reports = st.checkbox(
        "📊 Healthcare Reports"
    )


# ---------------------------------------------------------
# TARGET USER SELECTION
# ---------------------------------------------------------

st.subheader("3. Select Target Users")

target_users = st.multiselect(
    "Who will use this application?",
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


# ---------------------------------------------------------
# RAW IDEA
# ---------------------------------------------------------

st.subheader("4. Enter Your Healthcare Idea")

raw_idea = st.text_area(
    "Describe your idea:",
    value=(
        "A mobile app that helps patients find healthcare providers "
        "and manage their appointments."
    ),
    height=120
)


# =========================================================
# COLLECT SELECTED FEATURES
# =========================================================

selected_features = []

if appointment_booking:
    selected_features.append("Appointment Booking")

if patient_records:
    selected_features.append("Patient Records")

if doctor_search:
    selected_features.append("Doctor Search")

if reminders:
    selected_features.append("Appointment Reminders")

if prescription_management:
    selected_features.append("Prescription Management")

if hospital_management:
    selected_features.append("Hospital Management")

if billing:
    selected_features.append("Billing Management")

if notifications:
    selected_features.append("Notifications")

if reports:
    selected_features.append("Healthcare Reports")


# =========================================================
# DISPLAY USER SELECTION
# =========================================================

st.subheader("📌 Your Selection")

st.write(
    f"**Healthcare Type:** {healthcare_type}"
)

st.write(
    f"**Target Users:** "
    f"{', '.join(target_users) if target_users else 'None selected'}"
)

st.write(
    f"**Selected Features:** "
    f"{', '.join(selected_features) if selected_features else 'None selected'}"
)


# =========================================================
# START AI PROCESS
# =========================================================

if st.button(
    "🚀 Initiate Healthcare Launch Sprint",
    type="primary"
):

    if not raw_idea:
        st.warning("Please enter a healthcare idea.")

    elif not target_users:
        st.warning("Please select at least one target user.")

    elif not selected_features:
        st.warning("Please select at least one feature.")

    else:

        total_latency = 0

        with st.status(
            "🤖 Orchestrating Healthcare AI Agents...",
            expanded=True
        ) as status:

            # =================================================
            # AGENT 1
            # =================================================

            st.write(
                "🔍 **Agent 1: Healthcare Market Researcher**"
            )

            researcher_prompt = """
You are a Healthcare Market Researcher.

Analyze the healthcare management product idea.

Return exactly three bullet points:

- Target Audience: [who the product is for]
- Market Gap: [what is missing]
- Core Problem: [main healthcare management problem]

Consider the user's selected healthcare type,
target users, and requested features.

Do not add conversational text.
"""

            research_input = f"""
RAW IDEA:
{raw_idea}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

SELECTED FEATURES:
{selected_features}
"""

            research, lat = run_agent(
                researcher_prompt,
                research_input
            )

            total_latency += lat

            with st.expander(
                f"🔍 Research Results ({lat}s)"
            ):
                st.write(research)


            # =================================================
            # AGENT 2
            # =================================================

            st.write(
                "⚙️ **Agent 2: Healthcare Technical Product Manager**"
            )

            tech_pm_prompt = """
You are a Healthcare Technical Product Manager.

Using the market research and user's selected features,
create exactly 3 realistic MVP features that can be built
within four weeks.

Prioritize the features selected by the user.

Format:

1. [Feature Name]: [Description]
2. [Feature Name]: [Description]
3. [Feature Name]: [Description]

Do not add unnecessary features.

Do not provide medical diagnosis or autonomous treatment.
"""

            tech_scope, lat = run_agent(
                tech_pm_prompt,
                f"""
RESEARCH:
{research}

SELECTED HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}

USER SELECTED FEATURES:
{selected_features}
"""
            )

            total_latency += lat

            with st.expander(
                f"⚙️ MVP Technical Scope ({lat}s)"
            ):
                st.write(tech_scope)


            # =================================================
            # AGENT 3
            # =================================================

            st.write(
                "✨ **Agent 3: Healthcare Brand Strategist**"
            )

            brand_prompt = """
You are a Healthcare Brand Strategist.

Create a healthcare brand strategy based on the research.

Return exactly two lines:

Brand Positioning: [2 sentence value proposition]

Brand Tone: [3 keywords]

The brand should communicate trust, accessibility,
simplicity, reliability, and patient-centered care.

Do not make unsupported medical claims.
"""

            brand_strategy, lat = run_agent(
                brand_prompt,
                f"""
RESEARCH:
{research}

HEALTHCARE TYPE:
{healthcare_type}

TARGET USERS:
{target_users}
"""
            )

            total_latency += lat

            with st.expander(
                f"✨ Brand Strategy ({lat}s)"
            ):
                st.write(brand_strategy)


            # =================================================
            # AGENT 4
            # =================================================

            st.write(
                "⚖️ **Agent 4: Healthcare Quality Gate**"
            )

            critic_prompt = """
You are a Healthcare Quality Gate Critic.

Review the technical scope and brand strategy.

Identify possible conflicts involving:

- Patient safety
- Privacy
- Healthcare data
- Reliability
- Unrealistic medical claims
- Feature overload
- User expectations

Return a short paragraph.

If there are no major conflicts, say:
"No conflicts identified"
"""

            critique, lat = run_agent(
                critic_prompt,
                f"""
TECHNICAL SCOPE:
{tech_scope}

BRAND STRATEGY:
{brand_strategy}

HEALTHCARE TYPE:
{healthcare_type}

SELECTED FEATURES:
{selected_features}
"""
            )

            total_latency += lat

            with st.expander(
                f"⚖️ Quality Critique ({lat}s)"
            ):
                st.write(critique)


            # =================================================
            # AGENT 5
            # =================================================

            st.write(
                "🚀 **Agent 5: Lead Healthcare Synthesizer**"
            )

            reviser_prompt = """
You are the Lead Healthcare Product Synthesizer.

Combine the research, technical scope, brand strategy,
and quality critique.

Create a final 4-week healthcare management launch brief.

Return VALID JSON ONLY.

Schema:

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

Keep the MVP realistic.

Do not make unsupported medical claims.
Do not provide medical diagnosis or treatment recommendations.
"""

            final_brief, lat = run_agent(
                reviser_prompt,
                f"""
RESEARCH:
{research}

TECHNICAL SCOPE:
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

            total_latency += lat

            status.update(
                label=(
                    f"✅ Healthcare Launch Complete! "
                    f"Total Latency: {round(total_latency, 2)}s"
                ),
                state="complete",
                expanded=False
            )


        # =====================================================
        # FINAL RESULT
        # =====================================================

        st.divider()

        st.header("🏥 Final Healthcare Launch Brief")

        try:

            json_data = json.loads(final_brief)

            st.subheader(
                f"🚀 {json_data.get('product_name')}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.info(
                    f"**Healthcare Type:** "
                    f"{json_data.get('healthcare_type')}"
                )

            with col2:
                st.info(
                    f"**Target Audience:** "
                    f"{json_data.get('target_audience')}"
                )

            st.subheader(
                "⚙️ 4-Week MVP Features"
            )

            for feature in json_data.get(
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

            st.success(
                json_data.get(
                    "brand_positioning",
                    ""
                )
            )

            st.subheader(
                "⚖️ Resolved Tradeoffs"
            )

            st.warning(
                json_data.get(
                    "resolved_tradeoffs",
                    ""
                )
            )

        except Exception:

            st.error(
                "Unable to parse the final AI response."
            )

            st.markdown(final_brief)
