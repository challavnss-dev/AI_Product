```python
import os
import json
import streamlit as st
from groq import Groq


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI Hospital Management System")
st.write(
    "Manage patients, appointments, and AI-assisted hospital records."
)


# =========================================================
# GROQ API CONFIGURATION
# =========================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found.")
    st.info(
        "Please add GROQ_API_KEY to Streamlit Cloud Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# =========================================================
# APPLICATION TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👤 Patient Management",
        "📅 Appointment Management",
        "🤖 AI Patient Summary",
        "💡 Hospital MVP Scoper"
    ]
)


# =========================================================
# TAB 1 - PATIENT MANAGEMENT
# =========================================================

with tab1:

    st.header("👤 Patient Management")

    col1, col2 = st.columns(2)

    with col1:

        patient_name = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=25,
            step=1
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other",
                "Prefer not to say"
            ]
        )

        phone = st.text_input(
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
            placeholder="Enter allergies or None"
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

            st.warning("Please enter the patient's name.")

        else:

            patient_data = {
                "Patient Name": patient_name,
                "Age": age,
                "Gender": gender,
                "Phone": phone,
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


# =========================================================
# TAB 2 - APPOINTMENT MANAGEMENT
# =========================================================

with tab2:

    st.header("📅 Appointment Management")

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
            "Reason for Appointment",
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
                "Please enter both patient and doctor names."
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


# =========================================================
# TAB 3 - AI PATIENT SUMMARY
# =========================================================

with tab3:

    st.header("🤖 AI Patient Summary")

    st.info(
        "Enter an existing patient record to generate a "
        "structured administrative summary."
    )

    patient_record = st.text_area(
        "Patient Record",
        height=300,
        placeholder=(
            "Example:\n\n"
            "Patient Name: John Doe\n"
            "Age: 45\n"
            "Symptoms: Fever and cough\n"
            "Medical History: Type 2 Diabetes\n"
            "Allergies: None reported\n"
            "Test Results: Temperature 101.2 F\n"
            "Doctor Notes: Follow-up recommended"
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
You are an AI assistant for a hospital management system.

Create a clear and structured summary of the patient
record provided below.

PATIENT RECORD:
{patient_record}

STRICT RULES:

1. Use ONLY information provided in the patient record.
2. Never invent patient information.
3. Do not create a medical diagnosis.
4. Do not prescribe medicines.
5. Do not recommend treatments.
6. Do not change test results.
7. If information is missing, write "Not Provided".
8. Keep the summary professional and concise.
9. This is an AI-generated draft and must be reviewed
   by authorized healthcare professionals.

Use this structure:

PATIENT INFORMATION:
- Name:
- Age:
- Other Information:

REPORTED SYMPTOMS:
- 

MEDICAL HISTORY:
- 

ALLERGIES:
- 

TEST / INVESTIGATION INFORMATION:
- 

DOCTOR NOTES:
- 

FOLLOW-UP INFORMATION:
- 

MISSING INFORMATION:
- 
"""

            with st.spinner(
                "Generating AI patient summary..."
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
                                    "Never invent medical information."
                                )
                            },
                            {
                                "role": "user",
                                "content": summary_prompt
                            }
                        ],
                        temperature=0.2
                    )

                    summary = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.success(
                        "✅ AI summary generated successfully!"
                    )

                    st.subheader(
                        "📋 Patient Summary"
                    )

                    st.markdown(summary)

                except Exception as error:

                    st.error(
                        f"Error generating summary: {error}"
                    )


# =========================================================
# TAB 4 - HOSPITAL MVP SCOPER
# =========================================================

with tab4:

    st.header("💡 Hospital Management MVP Scoper")

    st.write(
        "Describe your hospital project idea and let AI "
        "create a realistic 24-hour hackathon MVP."
    )

    raw_idea = st.text_input(
        "Hospital Project Idea",
        placeholder=(
            "Example: An application to manage patients "
            "and hospital appointments"
        )
    )

    tools_available = st.multiselect(
        "Available Technology",
        [
            "Python",
            "Streamlit",
            "HTML/CSS",
            "React",
            "Groq API",
            "Gemini API",
            "Supabase",
            "Firebase",
            "SQL"
        ],
        default=[
            "Python",
            "Streamlit",
            "Groq API"
        ]
    )

    if st.button(
        "Scope Hospital MVP",
        type="primary",
        key="scope_hospital_mvp"
    ):

        if not raw_idea.strip():

            st.warning(
                "Please enter a hospital project idea."
            )

        elif not tools_available:

            st.warning(
                "Please select at least one technology."
            )

        else:

            scoping_prompt = f"""
You are a Senior Technical Product Manager.

Create a realistic 24-hour hackathon MVP for this
Hospital Management project.

PROJECT IDEA:
{raw_idea}

AVAILABLE TECHNOLOGY:
{", ".join(tools_available)}

INSTRUCTIONS:

1. Identify the core problem in one sentence.
2. Define exactly 3 MVP features.
3. All features must be achievable within 24 hours.
4. Use ONLY the selected technologies.
5. Focus on useful hospital-management functionality.
6. Do not require hardware.
7. Do not require unavailable external APIs.
8. Do not include autonomous medical diagnosis.
9. Return valid JSON only.

Use exactly this JSON structure:

{{
    "project_title": "string",
    "problem_statement": "string",
    "mvp_features": [
        "Feature 1",
        "Feature 2",
        "Feature 3"
    ],
    "tech_stack_mapping": "string",
    "future_features": [
        "Feature 1",
        "Feature 2"
    ]
}}
"""

            with st.spinner(
                "Creating hospital MVP..."
            ):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a technical product "
                                    "manager specializing in "
                                    "hospital software."
                                )
                            },
                            {
                                "role": "user",
                                "content": scoping_prompt
                            }
                        ],
                        response_format={
                            "type": "json_object"
                        },
                        temperature=0.4
                    )

                    result = json.loads(
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.success(
                        "✅ Hospital MVP created successfully!"
                    )

                    st.subheader(
                        "🏥 "
                        + result.get(
                            "project_title",
                            "Hospital Management System"
                        )
                    )

                    st.markdown(
                        "### 🎯 Problem Statement"
                    )

                    st.write(
                        result.get(
                            "problem_statement",
                            "Not Provided"
                        )
                    )

                    st.markdown(
                        "### 🚀 MVP Features"
                    )

                    for feature in result.get(
                        "mvp_features",
                        []
                    ):

                        st.markdown(
                            f"- ✅ {feature}"
                        )

                    st.markdown(
                        "### 🛠️ Technology Mapping"
                    )

                    st.info(
                        result.get(
                            "tech_stack_mapping",
                            "Not Provided"
                        )
                    )

                    st.markdown(
                        "### 🔮 Future Features"
                    )

                    for feature in result.get(
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
                        f"Error creating MVP: {error}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏥 AI Hospital Management System | "
    "AI-generated summaries are for administrative assistance "
    "and require review by authorized healthcare professionals."
)
```
