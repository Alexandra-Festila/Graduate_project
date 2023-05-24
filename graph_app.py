import streamlit as st
import pandas as pd

import typing as t

import src.commands as c

st.set_page_config(layout="wide")

data = c.ListRecordsCommand().execute()

df = pd.DataFrame(data, columns=[
    "Id",
    "Patient id",
    "Date",
    "Heart rate (BPM)",
    "Blood pressure (mmHg)",
    "Respiratory rate (brpm)",
    "Oxygen saturation (%)",
    "Temperature (°C)",
])


# Display the selection menu
option = st.sidebar.selectbox(
    "Select an option",
    [
        "Home",
        "Add a record",
        "List all records",
        "Get records by patient",
        "Delete record",
    ],
)

# Handle the selected option
if option == "Home":
    st.title("Timely Insights for Patient Monitoring")
    st.write("")
    
    with st.container():
        st.image("https://www.med-technews.com/downloads/7659/download/shutterstock_1721879812.jpg?cb=d87507a69004cdfef060f21cc5232404", width=750)

if option == "Add a record":
    st.write("##### Add a Record")
    
    patient_id = st.text_input("Patient id")
    heart_rate = st.number_input("Heart rate (BPM)", step=1)
    blood_pressure = st.text_input("Blood pressure (mmHg)")
    respiratory_rate = st.number_input("Respiratory rate (brpm)", step=1)
    oxygen_saturation = st.number_input("Oxygen saturation (%)", step=1)
    temperature = st.number_input("Temperature (°C)", step=1)
    
    if st.button("Add Record"):
        record_data: t.Dict[str, t.Union[str, int, float]] = {
            "patient_id": patient_id,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "respiratory_rate": respiratory_rate,
            "oxygen_saturation": oxygen_saturation,
            "temperature": temperature,
        }
        
        result = c.AddRecordCommand().execute(record_data)

        st.success(result)


if option == "List all records":
    st.write("#### All records")

    styled_df = df.style
    st.dataframe(styled_df)

elif option == "Get records by patient":
    st.write("#### Records by patient")

    patient_id = st.text_input("Enter Patient ID:")

    if st.button("Get Records"):
        records = c.GetPatientRecordsCommand().execute(int(patient_id))
        if records:
            df_by_patient = pd.DataFrame(records, columns=[
                "Id",
                "Patient id",
                "Date",
                "Heart rate (BPM)",
                "Blood pressure (mmHg)",
                "Respiratory rate (brpm)",
                "Oxygen saturation (%)",
                "Temperature (°C)"
            ])

            styled_df = df_by_patient.style

            with st.container():
                st.dataframe(styled_df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown("<p style='text-align: center;'>Heart rate</p>", unsafe_allow_html=True)
                st.line_chart(styled_df, x="Date", y="Heart rate (BPM)", width=0, height=0, use_container_width=True)
            with col2:
                st.markdown("<p style='text-align: center;'>Respiratory rate</p>", unsafe_allow_html=True)
                st.line_chart(styled_df, x="Date", y="Respiratory rate (brpm)", width=0, height=0, use_container_width=True)
            with col3:
                st.markdown("<p style='text-align: center;'>Oxygen saturation</p>", unsafe_allow_html=True)
                st.line_chart(styled_df, x="Date", y="Oxygen saturation (%)", width=0, height=0, use_container_width=True)
            with col4:
                st.markdown("<p style='text-align: center;'>Temperature</p>", unsafe_allow_html=True)
                st.line_chart(styled_df, x="Date", y="Temperature (°C)", width=0, height=0, use_container_width=True)

        else:
            st.write("No records found for the specified patient.")

            
elif option == "Delete record":
    record_ids = list(sorted(df["Id"]))
    id_ = st.selectbox("Select Record ID to delete:", record_ids)

    if st.button("Delete Record"):
        result = c.DeleteRecordCommand().execute(int(id_))
        st.write(result)


