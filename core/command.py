#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

import logger_app
import types

#############################################
#############################################
##
##  Prepare #logger
##
#############################################
#############################################

logger = logger_app.prepareLogger(__name__)

#############################################
#############################################
##
##  Exceptions
##
#############################################
#############################################

class CommandException(Exception):
    ...


class CommandNotFound(Exception):
    ...

class CommandAlreadyExist(Exception):
    ...

class CommandArgumentError(Exception):
    ...

#############################################
#############################################
##
##  Main classes and functions
##
#############################################
#############################################

class Command:
    def __init__(self, name: str, description: str, command: types.FunctionType, args: dict[str, tuple[type, any]]) -> None:
        self.name = name
        self.description = description
        self.args = args
        
        if not callable(command):
            raise CommandException(f"<{command}> is not callable!")
        self.command = command
    
    def __call__(self, **kwargs) -> None:
        if len(kwargs.keys()) != len(self.args.keys()):
            missed_args = set(self.args.keys()).difference(set(kwargs.keys()))
            for key in missed_args:
                kwargs[key] = self.args[key][1]
        self.command(**kwargs)


class CommandTable:
    def __init__(self, commands: list[Command] | None):
        self.commands = {command.name: command for command in commands} if commands else {}
    
    def add_command(self, command: Command) -> None:
        if command.name in self.commands.keys():
            raise CommandAlreadyExist(f"Command <{command.name}> already exist!")
    
    def get_commands_name(self) -> list[str]:
        return [command.name for command in self.commands.values()]
    
    def get_command(self, name: str) -> Command:
        if name not in self.commands.keys():
            similar = self._get_similar_command(name)
            if similar:
                raise CommandNotFound(f"Command <{name}> not found in CommandTable! Maybe you meant <{similar}>?")
            raise CommandNotFound(f"Command <{name}> not found in CommandTable!")
        return self.commands.get(name)
    
    def _get_similar_command(self, name: str) -> str:
        count, coefficient, similar = 100, 0, None
        for command in self.get_commands_name():
            _count = self._calculate_levenshtein_distance(name, command)
            _coefficient = self._calculate_jacquard_resemblance(name, command)
            if _count < count:
                count, similar = _count, command
            if _coefficient > coefficient:
                coefficient, similar = _coefficient, command
        return similar
    
    def _calculate_levenshtein_distance(self, string1: str, string2: str) -> int:
        lower_string, bigger_string = (string1, string2) if len(string1) < len(string2) else (string1, string2)
        count = 0
        for i in range(len(bigger_string)):
            if i >= len(lower_string):
                count += 1
                continue
            if lower_string[i] == bigger_string[i]:
                continue
            count += 1
        return count

    def _calculate_jacquard_resemblance(self, string1: str, string2: str) -> float:
        a = set(string1)
        b = set(string2)
        shared = a.intersection(b)
        total = a.union(b)
        return len(shared) / len(total)