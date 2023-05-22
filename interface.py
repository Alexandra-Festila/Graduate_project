from src import commands as c
from src import presentation as p

def loop():
    options = {
        "A": p.Option(
            name="Add a record",
            command=c.AddRecordCommand(),
            prep_call=p.get_new_records
        ),
        "L": p.Option(
            name="List records by date",
            command=c.ListRecordsCommand(),
        ),
        "I": p.Option(
            name="List records by patient ID",
            command=c.ListRecordsCommand(order_by="patient_id"),
        ),
        "P": p.Option(
            name="Get all records of a patient",
            command=c.GetPatientRecordsCommand(),
            prep_call=p.get_patient_id
        ),
        "D": p.Option(
            name="Delete a single record",
            command=c.DeleteRecordCommand(),
            prep_call=p.get_record_id
        ),
        "R": p.Option(
            name="Delete all records of a patient",
            command=c.DeletePatientRecordsCommand,
            prep_call=p.get_patient_id
        ),
        "Q": p.Option(
            name="Quit",
            command=c.QuitCommand()
        )
    }

    p.clear_screen()
    p.print_options(options)
    chose_option = p.get_option_choice(options)
    p.clear_screen()
    chose_option.choose()

    _ = input("Press ENTER to return to menu.")

if __name__ == "__main__":
    c.CreateVitalSignsTableCommand().execute()
    while True:
        loop()