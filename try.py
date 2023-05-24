import src.commands as c

patient_id = input("Enter Patient ID:")

records = c.GetPatientRecordsCommand().execute(int(patient_id))
print(records)
