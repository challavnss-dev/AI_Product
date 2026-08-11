import os
import json

import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# GROQ API CONFIGURATION
# ============================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("❌ GROQ_API_KEY is not configured.")
    st.info(
        "Go to Streamlit Cloud → App Settings → Secrets "
        "and add your GROQ_API_KEY."
    )
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# TITLE
# ============================================================

st.title("🏥 AI Hospital Management System")

st.write(
    "A simple hospital management application with "
    "patient management, appointments, and AI assistance."
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👤 Patient Management",
        "📅 Appointment Management",
        "🤖 AI Patient Summary",
        "💡 Hospital MVP Planner"
    ]
)


# ============================================================
# TAB 1: PATIENT MANAGEMENT
# ============================================================

with tab1:

    st.header("👤 Patient Management")

    st.subheader("Register Patient")

    col1, col2 = st.columns(2)

    with col1:

        patient_name = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
        )

        patient_age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=18,
            step=1
        )

        patient_gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other",
                "Prefer not to say"
            ]
        )

        patient_phone = st.text_input(
            "Phone Number",
            placeholder="Enter phone number"
        )

    with col2:

        blood_group = st.selectbox(
            "Blood Group",
            [
                "Not Provided",
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]
        )

        allergies = st.text_area(
            "Known Allergies",
            placeholder="Enter known allergies"
        )

        medical_history = st.text_area(
            "Medical History",
            placeholder="Enter medical history"
        )

    symptoms = st.text_area(
        "Reported Symptoms",
        height=100,
        placeholder="Enter symptoms reported by the patient"
    )

    if st.button(
        "Register Patient",
        type="primary",
        key="register_patient"
    ):

        if not patient_name.strip():

            st.warning(
                "Please enter the patient's name."
            )

        else:

            patient_data = {
                "Patient Name": patient_name,
                "Age": patient_age,
                "Gender": patient_gender,
                "Phone": patient_phone,
                "Blood Group": blood_group,
                "Allergies": allergies,
                "Medical History": medical_history,
                "Reported Symptoms": symptoms
            }

            st.success(
                "✅ Patient registered successfully!"
            )

            st.subheader("Patient Details")

            st.json(patient_data)


# ============================================================
# TAB 2: APPOINTMENT MANAGEMENT
# ============================================================

with tab2:

    st.header("📅 Appointment Management")

    st.subheader("Schedule Appointment")

    col1, col2 = st.columns(2)

    with col1:

        appointment_patient = st.text_input(
            "Patient Name",
            placeholder="Enter patient name",
            key="appointment_patient"
        )

        doctor_name = st.text_input(
            "Doctor Name",
            placeholder="Enter doctor name"
        )

        department = st.selectbox(
            "Department",
            [
                "General Medicine",
                "Cardiology",
                "Neurology",
                "Orthopedics",
                "Pediatrics",
                "Dermatology",
                "ENT",
                "Gynecology",
                "Emergency"
            ]
        )

    with col2:

        appointment_date = st.date_input(
            "Appointment Date"
        )

        appointment_time = st.time_input(
            "Appointment Time"
        )

        appointment_reason = st.text_area(
            "Appointment Reason",
            placeholder="Enter reason for appointment"
        )

    if st.button(
        "Schedule Appointment",
        type="primary",
        key="schedule_appointment"
    ):

        if (
            not appointment_patient.strip()
            or not doctor_name.strip()
        ):

            st.warning(
                "Please enter both patient name "
                "and doctor name."
            )

        else:

            appointment_data = {
                "Patient": appointment_patient,
                "Doctor": doctor_name,
                "Department": department,
                "Date": str(appointment_date),
                "Time": str(appointment_time),
                "Reason": appointment_reason
            }

            st.success(
                "✅ Appointment scheduled successfully!"
            )

            st.subheader("Appointment Details")

            st.json(appointment_data)


# ============================================================
# TAB 3: AI PATIENT SUMMARY
# ============================================================

with tab3:

    st.header("🤖 AI Patient Summary")

    st.write(
        "Enter a patient record and use Groq AI to create "
        "a structured administrative summary."
    )

    patient_record = st.text_area(
        "Patient Record",
        height=300,
        placeholder=(
            "Patient Name: John Doe\n"
            "Age: 45\n"
            "Symptoms: Fever and cough\n"
            "Medical History: Diabetes\n"
            "Allergies: None reported\n"
            "Test Results: Temperature 101.2 F\n"
            "Doctor Notes: Follow-up required"
        )
    )

    if st.button(
        "Generate AI Summary",
        type="primary",
        key="generate_summary"
    ):

        if not patient_record.strip():

            st.warning(
                "Please enter a patient record."
            )

        else:

            summary_prompt = f"""
You are an AI administrative assistant
for a hospital management system.

Create a clear and structured summary
from the patient information below.

PATIENT RECORD:
{patient_record}

STRICT RULES:

1. Use only information explicitly provided.
2. Never invent patient information.
3. Do not provide a medical diagnosis.
4. Do not prescribe medication.
5. Do not recommend treatment.
6. Do not change test results.
7. If information is missing, write
   "Not Provided".
8. Keep the summary concise and professional.

Use this structure:

PATIENT INFORMATION
Name:
Age:
Other Information:

REPORTED SYMPTOMS
-

MEDICAL HISTORY
-

ALLERGIES
-

TEST INFORMATION
-

DOCTOR NOTES
-

FOLLOW-UP INFORMATION
-

MISSING INFORMATION
-
"""

            with st.spinner(
                "Generating AI summary..."
            ):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a hospital "
                                    "administrative AI assistant. "
                                    "Only summarize information "
                                    "provided by the user."
                                )
                            },
                            {
                                "role": "user",
                                "content": summary_prompt
                            }
                        ],
                        temperature=0.2
                    )

                    ai_summary = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.success(
                        "✅ AI summary generated!"
                    )

                    st.subheader(
                        "📋 Patient Summary"
                    )

                    st.markdown(ai_summary)

                except Exception as error:

                    st.error(
                        f"AI Error: {error}"
                    )


# ============================================================
# TAB 4: HOSPITAL MVP PLANNER
# ============================================================

with tab4:

    st.header("💡 Hospital MVP Planner")

    st.write(
        "Enter a hospital project idea and generate "
        "a realistic 24-hour hackathon MVP."
    )

    hospital_idea = st.text_input(
        "Hospital Project Idea",
        placeholder=(
            "Example: An application to manage "
            "patients and hospital appointments"
        )
    )

    available_tools = st.multiselect(
        "Available Technologies",
        [
            "Python",
            "Streamlit",
            "HTML/CSS",
            "Groq API",
            "SQL",
            "Supabase",
            "Firebase",
            "React"
        ],
        default=[
            "Python",
            "Streamlit",
            "Groq API"
        ]
    )

    if st.button(
        "Generate Hospital MVP",
        type="primary",
        key="generate_mvp"
    ):

        if not hospital_idea.strip():

            st.warning(
                "Please enter a hospital project idea."
            )

        elif not available_tools:

            st.warning(
                "Please select at least one technology."
            )

        else:

            mvp_prompt = f"""
You are a Senior Technical Product Manager.

Create a realistic 24-hour hackathon MVP
for a Hospital Management System.

PROJECT IDEA:
{hospital_idea}

AVAILABLE TECHNOLOGIES:
{", ".join(available_tools)}

REQUIREMENTS:

1. Identify the core problem.
2. Define exactly 3 MVP features.
3. Features must be achievable in 24 hours.
4. Use only the available technologies.
5. Focus on hospital administration.
6. Do not include autonomous diagnosis.
7. Do not require hardware.
8. Return valid JSON only.

Return exactly:

{{
    "project_title": "string",
    "problem_statement": "string",
    "mvp_features": [
        "Feature 1",
        "Feature 2",
        "Feature 3"
    ],
    "technology_plan": "string",
    "future_features": [
        "Feature 1",
        "Feature 2"
    ]
}}
"""

            with st.spinner(
                "Generating hospital MVP..."
            ):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert "
                                    "technical product manager "
                                    "for hospital software."
                                )
                            },
                            {
                                "role": "user",
                                "content": mvp_prompt
                            }
                        ],
                        response_format={
                            "type": "json_object"
                        },
                        temperature=0.4
                    )

                    mvp_data = json.loads(
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.success(
                        "✅ Hospital MVP generated!"
                    )

                    st.subheader(
                        "🏥 "
                        + mvp_data.get(
                            "project_title",
                            "Hospital Management System"
                        )
                    )

                    st.markdown(
                        "### 🎯 Problem Statement"
                    )

                    st.write(
                        mvp_data.get(
                            "problem_statement",
                            "Not Provided"
                        )
                    )

                    st.markdown(
                        "### 🚀 MVP Features"
                    )

                    for feature in mvp_data.get(
                        "mvp_features",
                        []
                    ):

                        st.markdown(
                            f"- ✅ {feature}"
                        )

                    st.markdown(
                        "### 🛠️ Technology Plan"
                    )

                    st.info(
                        mvp_data.get(
                            "technology_plan",
                            "Not Provided"
                        )
                    )

                    st.markdown(
                        "### 🔮 Future Features"
                    )

                    for feature in mvp_data.get(
                        "future_features",
                        []
                    ):

                        st.markdown(
                            f"- 🔹 {feature}"
                        )

                except json.JSONDecodeError:

                    st.error(
                        "The AI returned invalid JSON. "
                        "Please try again."
                    )

                except Exception as error:

                    st.error(
                        f"MVP Error: {error}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏥 Hospital Management System | "
    "AI-generated summaries are administrative drafts "
    "and should be reviewed by authorized professionals."
)
```
