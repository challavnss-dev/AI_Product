import streamlit as st
import os
import json
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
st.write("Manage patients, appointments, medical records, and hospital workflows with AI.")

# =========================================================
# GROQ API CONFIGURATION
# =========================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error(
        "⚠️ Groq API Key not found! "
        "Please configure GROQ_API_KEY in your environment or Streamlit secrets."
    )
    st.stop()

client = Groq(api_key=api_key)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Patient Management",
    "📅 Appointment Management",
    "🤖 AI Patient Summary",
    "💡 Hospital MVP Scoper"
])


# =========================================================
# TAB 1: PATIENT MANAGEMENT
# =========================================================

with tab1:

    st.header("👤 Patient Registration")

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
            value=25
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"]
        )

    with col2:
        phone = st.text_input(
            "Phone Number",
            placeholder="Enter phone number"
        )

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
            placeholder="Enter known allergies or 'None'"
        )

    medical_history = st.text_area(
        "Medical History",
        height=120,
        placeholder="Enter relevant medical history..."
    )

    symptoms = st.text_area(
        "Current Symptoms",
        height=120,
        placeholder="Enter patient's reported symptoms..."
    )

    if st.button("Register Patient", type="primary"):

        if not patient_name:
            st.warning("Please enter the patient's name.")

        else:
            patient_data = {
                "patient_name": patient_name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "blood_group": blood_group,
                "allergies": allergies,
                "medical_history": medical_history,
                "symptoms": symptoms
            }

            st.success("✅ Patient registered successfully!")

            st.subheader("Patient Record")

            st.json(patient_data)


# =========================================================
# TAB 2: APPOINTMENT MANAGEMENT
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
                "Dermatology",
                "Pediatrics",
                "Gynecology",
                "ENT",
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
            placeholder="Enter reason..."
        )

    if st.button("Schedule Appointment", type="primary"):

        if not appointment_patient or not doctor_name:
            st.warning(
                "Please enter both patient name and doctor name."
            )

        else:

            appointment = {
                "patient": appointment_patient,
                "doctor": doctor_name,
                "department": department,
                "date": str(appointment_date),
                "time": str(appointment_time),
                "reason": appointment_reason
            }

            st.success("✅ Appointment scheduled successfully!")

            st.subheader("Appointment Details")

            st.json(appointment)


# =========================================================
# TAB 3: AI PATIENT SUMMARY
# =========================================================

with tab3:

    st.header("🤖 AI Patient Record Summarizer")

    st.info(
        "Enter existing patient information to generate a structured "
        "summary for review by authorized hospital staff."
    )

    patient_record = st.text_area(
        "Patient Medical Record",
        height=300,
        placeholder="""
Example:

Patient Name: John Doe
Age: 45
Symptoms: Fever, cough
Medical History: Type 2 Diabetes
Recent Tests: Blood pressure 130/85
Doctor Notes: Follow-up recommended
        """
    )

    if st.button("Generate Patient Summary", type="primary"):

        if not patient_record:

            st.warning("Please enter a patient record.")

        else:

            summary_prompt = f"""
You are an AI assistant for a hospital management system.

Your task is to organize the supplied patient record into a
clear and concise medical summary for review by authorized
healthcare professionals.

PATIENT RECORD:
{patient_record}

STRICT RULES:

1. ONLY use information explicitly provided in the patient record.
2. Do NOT invent symptoms, diagnoses, medications, test results,
   allergies, or medical history.
3. Do NOT make a new medical diagnosis.
4. Do NOT prescribe medication or treatment.
5. Clearly identify information that is missing.
6. Keep the summary professional and concise.
7. This output is a draft for review by qualified healthcare staff.

Use the following structure:

Patient Information:
Presenting Symptoms:
Medical History:
Test/Investigation Information:
Doctor Notes:
Follow-up Information:
Missing Information:
"""

            with st.spinner("Generating patient summary..."):

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a hospital administrative AI assistant. "
                                "Never invent patient information."
                            )
                        },
                        {
                            "role": "user",
                            "content": summary_prompt
                        }
                    ],
                    temperature=0.2
                )

                summary = res.choices[0].message.content

                st.success("✅ Patient summary generated!")

                st.markdown("### 📋 AI-Generated Summary")

                st.markdown(summary)


# =========================================================
# TAB 4: HOSPITAL MVP SCOPER
# =========================================================

with tab4:

    st.header("💡 Hospital Management MVP Scoper")

    st.write(
        "Describe your hospital-management idea and let AI "
        "define a realistic 24-hour hackathon MVP."
    )

    raw_idea = st.text_input(
        "Enter your hospital project idea:",
        placeholder=(
            "e.g., An AI system that helps hospitals manage "
            "patients and appointments"
        )
    )

    tools_available = st.multiselect(
        "Select tools you know how to use:",
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

    if st.button("Scope Hospital MVP", type="primary"):

        if not raw_idea:

            st.warning("Please enter a hospital project idea.")

        elif not tools_available:

            st.warning("Please select at least one technology.")

        else:

            scoping_prompt = f"""
You are a Senior Technical Product Manager.

You are helping a student team build a Hospital Management
System as a 24-hour hackathon MVP.

PROJECT IDEA:
{raw_idea}

AVAILABLE TECH STACK:
{', '.join(tools_available)}

INSTRUCTIONS:

1. Identify the core hospital-management problem in one sentence.
2. Define exactly 3 MVP features.
3. Features must be realistic for a 24-hour hackathon.
4. Use ONLY the selected technology stack.
5. Prioritize features useful for hospital staff or patients.
6. Avoid unnecessary advanced features.
7. Do not assume hardware or external services that were not selected.
8. Return STRICT JSON only.

Use exactly this schema:

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
                "AI is defining the hospital MVP..."
            ):

                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a technical product manager "
                                "specializing in healthcare software MVPs."
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

                try:

                    json_data = json.loads(
                        res.choices[0].message.content
                    )

                    st.success("✅ Hospital MVP scoped successfully!")

                    st.subheader(
                        f"🏥 Project: {json_data.get('project_title')}"
                    )

                    st.write(
                        f"**Core Problem:** "
                        f"{json_data.get('problem_statement')}"
                    )

                    st.markdown("### 🚀 MVP Features")

                    for feature in json_data.get(
                        "mvp_features", []
                    ):
                        st.markdown(
                            f"- ✅ {feature}"
                        )

                    st.markdown("### 🛠️ Technology Plan")

                    st.info(
                        json_data.get(
                            "tech_stack_mapping"
                        )
                    )

                    st.markdown("### 🔮 Future Features")

                    for feature in json_data.get(
                        "future_features", []
                    ):
                        st.markdown(
                            f"- 🔹 {feature}"
                        )

                except json.JSONDecodeError:

                    st.error(
                        "The AI returned invalid JSON. "
                        "Please try again."
                    )