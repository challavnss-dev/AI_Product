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
# GROQ API
# ============================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("❌ GROQ_API_KEY is missing.")
    st.info(
        "Add GROQ_API_KEY in Streamlit Cloud → "
        "Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title("🏥 AI Hospital Management System")

st.write(
    "A simple AI-powered hospital management application "
    "for managing patients, appointments and hospital projects."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 Hospital Menu")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Patient Management",
        "Appointment Management",
        "AI Patient Summary",
        "Hospital MVP Planner"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.header("📊 Hospital Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Patients",
            "120"
        )

    with col2:
        st.metric(
            "Doctors",
            "25"
        )

    with col3:
        st.metric(
            "Appointments",
            "48"
        )

    with col4:
        st.metric(
            "Departments",
            "9"
        )

    st.divider()

    st.subheader("🏥 Hospital System")

    st.info(
        "Use the menu on the left to manage patients, "
        "appointments and AI-powered hospital features."
    )

    st.warning(
        "Demo application: patient information entered "
        "here is not permanently stored."
    )


# ============================================================
# PATIENT MANAGEMENT
# ============================================================

elif menu == "Patient Management":

    st.header("👤 Patient Management")

    st.subheader("Register New Patient")

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
            "Allergies",
            placeholder="Enter known allergies"
        )

        medical_history = st.text_area(
            "Medical History",
            placeholder="Enter medical history"
        )

    symptoms = st.text_area(
        "Reported Symptoms",
        placeholder="Enter reported symptoms"
    )

    if st.button(
        "Register Patient",
        type="primary"
    ):

        if not patient_name.strip():

            st.warning(
                "Please enter the patient's name."
            )

        else:

            patient = {
                "Patient Name": patient_name,
                "Age": patient_age,
                "Gender": patient_gender,
                "Phone": patient_phone,
                "Blood Group": blood_group,
                "Allergies": allergies,
                "Medical History": medical_history,
                "Symptoms": symptoms
            }

            st.success(
                "✅ Patient registered successfully!"
            )

            st.subheader("Patient Details")

            st.json(patient)


# ============================================================
# APPOINTMENT MANAGEMENT
# ============================================================

elif menu == "Appointment Management":

    st.header("📅 Appointment Management")

    st.subheader("Schedule Appointment")

    col1, col2 = st.columns(2)

    with col1:

        appointment_patient = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
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
            placeholder="Enter appointment reason"
        )

    if st.button(
        "Schedule Appointment",
        type="primary"
    ):

        if not appointment_patient.strip():

            st.warning(
                "Please enter the patient name."
            )

        elif not doctor_name.strip():

            st.warning(
                "Please enter the doctor name."
            )

        else:

            appointment = {
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

            st.subheader(
                "Appointment Details"
            )

            st.json(appointment)


# ============================================================
# AI PATIENT SUMMARY
# ============================================================

elif menu == "AI Patient Summary":

    st.header("🤖 AI Patient Summary")

    st.write(
        "Enter patient information and generate a "
        "structured administrative summary."
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
        type="primary"
    ):

        if not patient_record.strip():

            st.warning(
                "Please enter patient information."
            )

        else:

            prompt = f"""
You are an AI administrative assistant
for a hospital.

Create a structured summary using ONLY
the information provided by the user.

PATIENT INFORMATION:

{patient_record}

STRICT RULES:

1. Do not invent information.
2. Do not diagnose the patient.
3. Do not prescribe medication.
4. Do not recommend treatment.
5. Do not modify test results.
6. Do not assume missing information.
7. Write "Not Provided" when information
   is missing.
8. Keep the summary professional and concise.

FORMAT:

PATIENT INFORMATION
Name:
Age:
Other Information:

SYMPTOMS
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
                                    "administrative assistant. "
                                    "Only summarize information "
                                    "provided by the user."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
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
                        "✅ Summary generated successfully!"
                    )

                    st.subheader(
                        "📋 Patient Summary"
                    )

                    st.markdown(summary)

                except Exception as error:

                    st.error(
                        "Unable to generate the summary."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# HOSPITAL MVP PLANNER
# ============================================================

elif menu == "Hospital MVP Planner":

    st.header("💡 Hospital MVP Planner")

    st.write(
        "Use AI to convert a hospital project idea "
        "into a realistic hackathon MVP."
    )

    hospital_idea = st.text_input(
        "Hospital Project Idea",
        placeholder=(
            "Example: A system for managing "
            "patients and doctor appointments"
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
        type="primary"
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
for the following hospital project.

PROJECT IDEA:

{hospital_idea}

AVAILABLE TECHNOLOGIES:

{", ".join(available_tools)}

INSTRUCTIONS:

1. Identify the core problem.
2. Define exactly 3 MVP features.
3. Features must be realistic for 24 hours.
4. Use only the available technologies.
5. Focus on hospital management.
6. Do not include autonomous medical diagnosis.
7. Do not require hardware.
8. Return JSON only.

Return this exact structure:

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
                                    "technical product manager."
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

                    result = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    data = json.loads(result)

                    st.success(
                        "✅ Hospital MVP generated!"
                    )

                    st.subheader(
                        "🏥 "
                        + data.get(
                            "project_title",
                            "Hospital Management System"
                        )
                    )

                    st.markdown(
                        "### 🎯 Problem Statement"
                    )

                    st.write(
                        data.get(
                            "problem_statement",
                            "Not Provided"
                        )
                    )

                    st.markdown(
                        "### 🚀 MVP Features"
                    )

                    features = data.get(
                        "mvp_features",
                        []
                    )

                    for feature in features:

                        st.markdown(
                            f"- ✅ {feature}"
                        )

                    st.markdown(
                        "### 🛠️ Technology Plan"
                    )

                    st.info(
                        data.get(
                            "technology_plan",
                            "Not Provided"
                        )
                    )

                    st.markdown(
                        "### 🔮 Future Features"
                    )

                    future_features = data.get(
                        "future_features",
                        []
                    )

                    for feature in future_features:

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
                        "Unable to generate the MVP."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏥 AI Hospital Management System | "
    "AI-generated content is for administrative "
    "support and should be reviewed by authorized "
    "hospital professionals."
)
```
