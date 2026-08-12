import streamlit as st
import os
import time
import json
from groq import Groq

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Healthcare Management Launch Syndicate",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Management Launch Syndicate")
st.write(
    "Multi-Agent Orchestration: Scoping a 4-week V1 healthcare "
    "management launch by balancing Product Management and Healthcare Strategy."
)

# ---------------------------------------------------------
# GROQ API CONFIGURATION
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# AGENT FUNCTION
# ---------------------------------------------------------

def run_agent(persona, prompt_input, json_mode=False):
    start_time = time.time()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt_input}
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


# ---------------------------------------------------------
# RAW HEALTHCARE IDEA
# ---------------------------------------------------------

raw_idea = st.text_input(
    "Enter your healthcare management idea:",
    value=(
        "A mobile app connecting patients with local healthcare "
        "providers for easy appointment booking and medical care."
    )
)


# ---------------------------------------------------------
# START MULTI-AGENT PROCESS
# ---------------------------------------------------------

if st.button(
    "🏥 Initiate Healthcare Launch Sprint",
    type="primary"
):

    if not raw_idea:
        st.warning("Please provide a healthcare management idea.")

    else:

        total_latency = 0

        with st.status(
            "Orchestrating Healthcare Agency Team...",
            expanded=True
        ) as status:

            # =====================================================
            # AGENT 1: HEALTHCARE MARKET RESEARCHER
            # =====================================================

            st.write(
                "🔍 **Agent 1 (Healthcare Market Researcher):** "
                "Analyzing patients, providers, and healthcare gaps..."
            )

            researcher_prompt = """
You are a Healthcare Market Researcher.

INPUT: A raw healthcare management product idea.

OUTPUT FORMAT: Return exactly 3 bullet points:

- Target Audience: [who the healthcare product is for]
- Market Gap: [what is currently missing in healthcare management]
- Core Problem: [the main healthcare management pain point]

Focus on patients, healthcare providers, clinics, and healthcare
administration where relevant.

Do not add any conversational text.
"""

            research, lat = run_agent(
                researcher_prompt,
                f"RAW HEALTHCARE IDEA:\n{raw_idea}"
            )

            total_latency += lat

            with st.expander(
                f"Healthcare Research Data ({lat}s)"
            ):
                st.write(research)


            # =====================================================
            # AGENT 2: HEALTHCARE TECH PRODUCT MANAGER
            # =====================================================

            st.write(
                "⚙️ **Agent 2 (Healthcare Tech PM):** "
                "Scoping the 4-week functional V1..."
            )

            tech_pm_prompt = """
You are a Healthcare Technical Product Manager.

INPUT: Healthcare Market Research data.

OUTPUT FORMAT: Return exactly 3 core MVP features that can
realistically be built in 4 weeks.

Format as:

1. [Feature Name]: [Brief description]
2. [Feature Name]: [Brief description]
3. [Feature Name]: [Brief description]

Focus on practical healthcare management features such as
appointment management, provider discovery, reminders, or
basic patient information management.

Ruthlessly cut feature bloat.

Do not include medical diagnosis or autonomous treatment
recommendations.
"""

            tech_scope, lat = run_agent(
                tech_pm_prompt,
                f"HEALTHCARE RESEARCH:\n{research}"
            )

            total_latency += lat

            with st.expander(
                f"Healthcare Tech Scope ({lat}s)"
            ):
                st.write(tech_scope)


            # =====================================================
            # AGENT 3: HEALTHCARE BRAND STRATEGIST
            # =====================================================

            st.write(
                "✨ **Agent 3 (Healthcare Brand Strategist):** "
                "Developing trust-focused messaging..."
            )

            brand_prompt = """
You are a Healthcare Brand Strategist.

INPUT: Healthcare Market Research data.

OUTPUT FORMAT: Return exactly two lines:

Brand Positioning: [2 sentence value proposition focused on
trust, accessibility, convenience, and better healthcare management]

Brand Tone: [3 keywords, e.g., Trustworthy, Caring, Reliable]

The brand must avoid making unsupported medical claims.
"""

            brand_strategy, lat = run_agent(
                brand_prompt,
                f"HEALTHCARE RESEARCH:\n{research}"
            )

            total_latency += lat

            with st.expander(
                f"Healthcare Brand Strategy ({lat}s)"
            ):
                st.write(brand_strategy)


            # =====================================================
            # AGENT 4: HEALTHCARE QUALITY GATE CRITIC
            # =====================================================

            st.write(
                "⚖️ **Agent 4 (Healthcare Quality Gate):** "
                "Checking safety, privacy, and product conflicts..."
            )

            critic_prompt = """
You are a Healthcare Quality Gate Critic.

INPUT:
1. Healthcare Tech PM scope
2. Healthcare Brand Strategy

OUTPUT FORMAT:
Return a short paragraph identifying conflicts between the
technical scope and brand promises.

Pay particular attention to:

- Patient safety
- Privacy and sensitive health information
- Reliability
- Unrealistic medical claims
- Whether the MVP promises more than it can deliver

If there are no conflicts, state:

'No conflicts identified'
"""

            critique, lat = run_agent(
                critic_prompt,
                f"""
HEALTHCARE TECH SCOPE:
{tech_scope}

HEALTHCARE BRAND STRATEGY:
{brand_strategy}
"""
            )

            total_latency += lat

            with st.expander(
                f"Healthcare Quality Critique ({lat}s)"
            ):
                st.write(critique)


            # =====================================================
            # AGENT 5: HEALTHCARE LEAD SYNTHESIZER
            # =====================================================

            st.write(
                "🚀 **Agent 5 (Healthcare Lead Synthesizer):** "
                "Finalizing Go-To-Market Healthcare Brief..."
            )

            reviser_prompt = """
You are the Lead Healthcare Product Synthesizer.

Take the healthcare technology scope, brand strategy,
and quality critique.

Resolve the identified conflicts and output a structured
JSON Go-To-Market Launch Brief.

Schema:

{
  "product_name": "string",
  "target_audience": "string",
  "four_week_v1_features": [
    "list of strict MVP features"
  ],
  "brand_positioning": "string",
  "resolved_tradeoffs": "string explaining how the
  critic's concerns were solved"
}

Requirements:

- Focus on healthcare management.
- Keep the MVP realistic for 4 weeks.
- Prioritize patient convenience and provider coordination.
- Do not make unsupported medical diagnosis or treatment claims.
- Do not promise medical outcomes.
- Return valid JSON only.
"""

            final_brief, lat = run_agent(
                reviser_prompt,
                f"""
HEALTHCARE TECH:
{tech_scope}

HEALTHCARE BRAND:
{brand_strategy}

HEALTHCARE CRITIQUE:
{critique}
""",
                json_mode=True
            )

            total_latency += lat

            status.update(
                label=(
                    f"Healthcare Launch Sprint Complete! "
                    f"Total Latency: {round(total_latency, 2)}s"
                ),
                state="complete",
                expanded=False
            )


        # =====================================================
        # DISPLAY FINAL RESULT
        # =====================================================

        try:

            json_data = json.loads(final_brief)

            st.subheader(
                f"🏥 {json_data.get('product_name')} "
                f"- Healthcare Go-To-Market Brief"
            )

            st.write(
                f"**Target Audience:** "
                f"{json_data.get('target_audience')}"
            )

            st.markdown(
                "**4-Week Functional V1 Features:**"
            )

            for feature in json_data.get(
                "four_week_v1_features", []
            ):
                st.markdown(f"- {feature}")

            st.info(
                f"**Brand Positioning:** "
                f"{json_data.get('brand_positioning')}"
            )

            st.warning(
                f"**Resolved Tradeoffs:** "
                f"{json_data.get('resolved_tradeoffs')}"
            )

        except Exception as e:

            st.error(
                "The final response could not be parsed as JSON."
            )

            st.markdown(final_brief)
