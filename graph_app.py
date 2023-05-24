import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import typing as t

import src.commands as c

st.write("## Timely Insights for Patient Monitoring")

data = c.ListRecordsCommand().execute()

df = pd.DataFrame(data, columns=[
    "Id",
    "Patient id",
    "Date",
    "Heart rate",
    "Blood pressure",
    "Respiratory rate",
    "Oxygen saturation",
    "Temperature",
])


# Display the selection menu
option = st.sidebar.selectbox(
    "Select an option",
    [
        "Add a record",
        "List all records",
        "Get records by patient",
        "Delete record",
    ]
)

# Handle the selected option

if option == "Add a record":
    st.write("##### Add a Record")
    
    patient_id = st.text_input("Patient id")
    heart_rate = st.number_input("Heart rate")
    blood_pressure = st.text_input("Blood pressure")
    respiratory_rate = st.number_input("Respiratory rate")
    oxygen_saturation = st.number_input("Oxygen saturation")
    temperature = st.number_input("Temperature")
    
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

elif option == "List all records":
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
                "Heart rate",
                "Blood pressure",
                "Respiratory rate",
                "Oxygen saturation",
                "Temperature"
            ])
            styled_df = df_by_patient.style
            st.dataframe(styled_df)

            graph_option = st.selectbox("Select Graph:", ["Line Chart", "Bar Chart"])
            if graph_option == "Line Chart":
                st.line_chart(df_by_patient)
            elif graph_option == "Bar Chart":
                st.bar_chart(df_by_patient)
        else:
            st.write("No records found for the specified patient.")

            
elif option == "Delete record":
    st.write("#### Records by patient")
    record_ids = list(sorted(df["Id"]))
    id_ = st.selectbox("Select Record ID to delete:", record_ids)

    if st.button("Delete Record"):
        result = c.DeleteRecordCommand().execute(int(id_))
        st.write(result)


