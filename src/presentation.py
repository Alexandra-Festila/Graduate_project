"A module for the presentation layer"
import os
import typing as t

from src.commands import Command

class Option:
    def __init__(
        self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None
    ):
    def __init__(
        self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        print(result)

    def __str__(self):
        return self.name


def print_options(options: t.Dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f"[{shortcut}] {option}")
    print()

def option_choice_valid(choice: str, options: t.Dict[str, Option]) -> bool:
    result = choice in options or choice.upper() in options
    return result

def get_option_choice(options: t.Dict[str, Option]) -> Option:
    choice = input("Please select an option from the menu above: ")
    while not option_choice_valid(choice, options):
        print()
        print("Invalid menu selection, please choose a valid option.")
        choice = input("Please select an option.")
    return options[choice.upper()]

def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)