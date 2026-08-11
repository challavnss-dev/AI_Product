```python
import os
import json
from datetime import datetime

import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Hospital Management",
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
    st.error("GROQ_API_KEY is not configured.")
    st.info(
        "Add GROQ_API_KEY in Streamlit Cloud → "
        "Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# DEMO DATA
# ============================================================

if "patients" not in st.session_state:
    st.session_state.patients = [
        {
            "id": "P001",
            "name": "Rahul Kumar",
            "age": 35,
            "gender": "Male",
            "phone": "9876543210",
            "blood_group": "O+",
            "history": "No major history reported",
            "allergies": "None reported",
            "past_visits": [
                {
                    "date": "2026-07-15",
                    "department": "General Medicine",
                    "symptoms": "Fever and tiredness",
                    "notes": "Routine follow-up advised"
                }
            ]
        },
        {
            "id": "P002",
            "name": "Priya Sharma",
            "age": 29,
            "gender": "Female",
            "phone": "9876501234",
            "blood_group": "A+",
            "history": "Seasonal allergy reported",
            "allergies": "Dust",
            "past_visits": [
                {
                    "date": "2026-06-21",
                    "department": "General Medicine",
                    "symptoms": "Cold and cough",
                    "notes": "Follow-up completed"
                }
            ]
        }
    ]


if "appointments" not in st.session_state:
    st.session_state.appointments = [
        {
            "patient": "Rahul Kumar",
            "doctor": "Dr. Anil",
            "department": "General Medicine",
            "date": "2026-08-15",
            "time": "10:00",
            "status": "Confirmed"
        }
    ]


if "ai_requests" not in st.session_state:
    st.session_state.ai_requests = []


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 Hospital Management")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Patient Past Data",
        "AI Health Chatbot",
        "Doctor Appointments"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("📊 Hospital Dashboard")

    total_patients = len(
        st.session_state.patients
    )

    total_appointments = len(
        st.session_state.appointments
    )

    pending_requests = len(
        [
            request
            for request in st.session_state.ai_requests
            if request["status"] == "Pending Doctor Review"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Patients",
            total_patients
        )

    with col2:
        st.metric(
            "Appointments",
            total_appointments
        )

    with col3:
        st.metric(
            "Doctors",
            "25"
        )

    with col4:
        st.metric(
            "AI Review Requests",
            pending_requests
        )

    st.divider()

    st.subheader("📅 Upcoming Appointments")

    if st.session_state.appointments:

        st.dataframe(
            st.session_state.appointments,
            use_container_width=True
        )

    else:

        st.info(
            "No appointments available."
        )

    st.divider()

    st.subheader("🤖 AI Review Requests")

    if st.session_state.ai_requests:

        st.dataframe(
            st.session_state.ai_requests,
            use_container_width=True
        )

    else:

        st.info(
            "No AI review requests."
        )


# ============================================================
# PATIENT PAST DATA
# ============================================================

elif page == "Patient Past Data":

    st.title("👤 Patient Past Data")

    st.write(
        "Search for a patient and view their previous "
        "hospital records."
    )

    patient_search = st.text_input(
        "Search Patient",
        placeholder="Enter patient name or patient ID"
    )

    if patient_search:

        search_text = patient_search.lower()

        matching_patients = [
            patient
            for patient in st.session_state.patients
            if (
                search_text in patient["name"].lower()
                or search_text in patient["id"].lower()
            )
        ]

        if matching_patients:

            for patient in matching_patients:

                st.subheader(
                    f"👤 {patient['name']} "
                    f"({patient['id']})"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"**Age:** {patient['age']}"
                    )
                    st.write(
                        f"**Gender:** {patient['gender']}"
                    )

                with col2:
                    st.write(
                        f"**Blood Group:** "
                        f"{patient['blood_group']}"
                    )
                    st.write(
                        f"**Phone:** {patient['phone']}"
                    )

                with col3:
                    st.write(
                        f"**Allergies:** "
                        f"{patient['allergies']}"
                    )
                    st.write(
                        f"**History:** "
                        f"{patient['history']}"
                    )

                st.markdown(
                    "### 📋 Previous Visits"
                )

                if patient["past_visits"]:

                    st.dataframe(
                        patient["past_visits"],
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No previous visits available."
                    )

                st.divider()

        else:

            st.warning(
                "No patient found."
            )

    st.subheader("➕ Add Patient")

    with st.form("add_patient_form"):

        new_name = st.text_input(
            "Patient Name"
        )

        new_age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=18
        )

        new_gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        new_phone = st.text_input(
            "Phone Number"
        )

        new_blood = st.selectbox(
            "Blood Group",
            [
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

        new_history = st.text_area(
            "Medical History"
        )

        new_allergies = st.text_area(
            "Allergies"
        )

        submitted = st.form_submit_button(
            "Add Patient"
        )

        if submitted:

            if not new_name.strip():

                st.warning(
                    "Please enter the patient name."
                )

            else:

                patient_number = (
                    len(st.session_state.patients) + 1
                )

                new_patient = {
                    "id": f"P{patient_number:03d}",
                    "name": new_name,
                    "age": new_age,
                    "gender": new_gender,
                    "phone": new_phone,
                    "blood_group": new_blood,
                    "history": new_history,
                    "allergies": new_allergies,
                    "past_visits": []
                }

                st.session_state.patients.append(
                    new_patient
                )

                st.success(
                    "Patient added successfully."
                )


# ============================================================
# AI HEALTH CHATBOT
# ============================================================

elif page == "AI Health Chatbot":

    st.title("🤖 AI Health Chatbot")

    st.warning(
        "This demo does not provide a medical diagnosis. "
        "It identifies information that may require "
        "professional medical review."
    )

    st.write(
        "Enter the patient's information and symptoms. "
        "The AI will organize the information and determine "
        "whether a doctor review should be requested."
    )

    patient_name = st.text_input(
        "Patient Name"
    )

    patient_id = st.text_input(
        "Patient ID",
        placeholder="Example: P001"
    )

    symptoms = st.text_area(
        "Current Symptoms",
        height=150,
        placeholder=(
            "Describe the symptoms, when they started, "
            "and any relevant information."
        )
    )

    additional_information = st.text_area(
        "Additional Information",
        height=120,
        placeholder=(
            "Previous medical history, allergies, "
            "recent test information, etc."
        )
    )

    if st.button(
        "Analyze and Request Doctor Review",
        type="primary"
    ):

        if not patient_name.strip():

            st.warning(
                "Please enter the patient name."
            )

        elif not symptoms.strip():

            st.warning(
                "Please describe the symptoms."
            )

        else:

            prompt = f"""
You are an AI hospital administrative
and patient-triage assistant.

You are NOT a doctor.

Review the information below and organize
it for a qualified healthcare professional.

PATIENT NAME:
{patient_name}

PATIENT ID:
{patient_id}

SYMPTOMS:
{symptoms}

ADDITIONAL INFORMATION:
{additional_information}

IMPORTANT RULES:

1. Do not provide a definitive diagnosis.
2. Do not prescribe medication.
3. Do not recommend a treatment plan.
4. Do not invent symptoms or medical history.
5. Identify possible areas of concern only.
6. State clearly that a qualified healthcare
   professional must make the diagnosis.
7. Identify whether professional review
   should be requested based only on the
   information provided.
8. If symptoms appear potentially urgent,
   clearly advise immediate professional care.

Return ONLY valid JSON:

{{
    "summary": "short summary",
    "possible_concerns": [
        "concern 1",
        "concern 2"
    ],
    "doctor_review_required": true,
    "urgency": "Routine / Soon / Urgent",
    "recommended_department": "department",
    "reason_for_review": "short explanation"
}}
"""

            with st.spinner(
                "AI is reviewing the information..."
            ):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a cautious "
                                    "hospital administrative "
                                    "AI assistant. Never "
                                    "claim to diagnose patients."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        response_format={
                            "type": "json_object"
                        },
                        temperature=0.1
                    )

                    result = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    analysis = json.loads(
                        result
                    )

                    st.subheader(
                        "📋 AI Review"
                    )

                    st.write(
                        analysis.get(
                            "summary",
                            "Not provided"
                        )
                    )

                    st.markdown(
                        "### Possible Concerns"
                    )

                    for concern in analysis.get(
                        "possible_concerns",
                        []
                    ):

                        st.markdown(
                            f"- {concern}"
                        )

                    urgency = analysis.get(
                        "urgency",
                        "Routine"
                    )

                    if urgency == "Urgent":

                        st.error(
                            "⚠️ Urgent professional "
                            "medical review may be required."
                        )

                    elif urgency == "Soon":

                        st.warning(
                            "Professional medical review "
                            "should be considered soon."
                        )

                    else:

                        st.info(
                            "Routine professional review "
                            "may be appropriate."
                        )

                    review_required = analysis.get(
                        "doctor_review_required",
                        False
                    )

                    if review_required:

                        st.success(
                            "👨‍⚕️ Doctor review request created."
                        )

                        appointment_request = {
                            "patient": patient_name,
                            "patient_id": patient_id,
                            "department": analysis.get(
                                "recommended_department",
                                "General Medicine"
                            ),
                            "reason": analysis.get(
                                "reason_for_review",
                                "Professional review requested"
                            ),
                            "urgency": urgency,
                            "requested_at": datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            ),
                            "status": "Pending Doctor Review"
                        }

                        st.session_state.ai_requests.append(
                            appointment_request
                        )

                        st.subheader(
                            "📅 Appointment Request"
                        )

                        st.json(
                            appointment_request
                        )

                        st.info(
                            "The request has been sent to the "
                            "Doctor Appointments module. A "
                            "doctor or authorized hospital "
                            "staff member should confirm the "
                            "appointment."
                        )

                    else:

                        st.info(
                            "No doctor review request was "
                            "created from the information "
                            "provided."
                        )

                except json.JSONDecodeError:

                    st.error(
                        "The AI response could not be processed. "
                        "Please try again."
                    )

                except Exception as error:

                    st.error(
                        "AI service error."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# DOCTOR APPOINTMENTS
# ============================================================

elif page == "Doctor Appointments":

    st.title("👨‍⚕️ Doctor Appointments")

    st.subheader(
        "AI-Generated Doctor Review Requests"
    )

    if st.session_state.ai_requests:

        for index, request in enumerate(
            st.session_state.ai_requests
        ):

            with st.container(border=True):

                st.write(
                    f"**Patient:** "
                    f"{request['patient']}"
                )

                st.write(
                    f"**Patient ID:** "
                    f"{request['patient_id']}"
                )

                st.write(
                    f"**Department:** "
                    f"{request['department']}"
                )

                st.write(
                    f"**Urgency:** "
                    f"{request['urgency']}"
                )

                st.write(
                    f"**Reason:** "
                    f"{request['reason']}"
                )

                st.write(
                    f"**Status:** "
                    f"{request['status']}"
                )

                if request["status"] == (
                    "Pending Doctor Review"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "Confirm Appointment",
                            key=f"confirm_{index}"
                        ):

                            request["status"] = (
                                "Confirmed"
                            )

                            st.session_state.appointments.append(
                                {
                                    "patient": request["patient"],
                                    "doctor": "Doctor To Be Assigned",
                                    "department": request["department"],
                                    "date": "To Be Scheduled",
                                    "time": "To Be Scheduled",
                                    "status": "Confirmed"
                                }
                            )

                            st.success(
                                "Appointment confirmed."
                            )

                            st.rerun()

                    with col2:

                        if st.button(
                            "Reject Request",
                            key=f"reject_{index}"
                        ):

                            request["status"] = (
                                "Rejected"
                            )

                            st.warning(
                                "Request rejected."
                            )

                            st.rerun()

    else:

        st.info(
            "There are no AI-generated appointment requests."
        )

    st.divider()

    st.subheader(
        "📅 Confirmed Appointments"
    )

    if st.session_state.appointments:

        st.dataframe(
            st.session_state.appointments,
            use_container_width=True
        )

    else:

        st.info(
            "No confirmed appointments."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏥 AI Hospital Management System | "
    "Demo application. AI output is not a medical diagnosis "
    "and must be reviewed by qualified healthcare professionals."
)
```
