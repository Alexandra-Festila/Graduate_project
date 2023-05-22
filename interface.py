from src import commands as c
from src import presentation as p

if __name__ == '__main__':
    c.CreateVitalSignsTableCommand().execute()
    print("Welcome to our patient monitoring app, designed exclusively for nurses to efficiently" 
            "manage and maintain accurate records of patient vital information and ensure the best possible care.")

options = {
    "A": p.Option(
        name="Add a record",
        command=c.AddRecordCommand(),
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
    ),
    "D": p.Option(
        name="Delete a single record",
        command=c.DeleteRecordCommand(),
    ),
    "R": p.Option(
        name="Delete all records of a patient",
        command=c.DeletePatientRecordsCommand
    ),
    "Q": p.Option(
        name="Quit",
        command=c.QuitCommand()
    )
}

p.print_options(options)
chose_option = p.get_option_choice(options)

chose_option.choose()