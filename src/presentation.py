"A module for the presentation layer"

import typing as t

from src.commands import Command

class Option:
    def __init__(self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        print(result)

    def __str__(self):
        return
