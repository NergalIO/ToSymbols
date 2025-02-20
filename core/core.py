#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

from . import command
import logger_app
import threading
import os

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

#############################################
#############################################
##
##  Main classes and functions
##
#############################################
#############################################

class Columner:
    def __call__(self, headlines: list[str], lines: list[list[str]]) -> str:
        try:
            if sum([len(line) for line in lines]) / len(lines) != len(headlines):
                raise ValueError("Length of headlines must be like length of lines!")
        except Exception as e:
            return '\n\t' + '\t'.join([headline.upper() for headline in headlines]) + '\n'
        
        lengths = [len(headline) for headline in headlines]
        for line in lines:
            for i in range(len(line)):
                lengths[i] = max(lengths[i], len(line[i]))
        
        text = f"\n\t"
        headlines_text = ""
        for i, headline in enumerate([headline.upper() for headline in headlines]):
            headlines_text += headline + ' ' * (lengths[i] - len(headline) + 2)
        headlines_text += "\n"
        
        lines_text = f""
        for line in lines:
            _line = "\n\t"
            for i, item in enumerate(line):
                _line += item + ' ' * (lengths[i] - len(item) + 2)
            lines_text += _line
        
        return text + headlines_text + lines_text + '\n'

class Core:
    def __init__(self, command: command.CommandTable):
        self.commands = command
    
    def add_command(self, command: command.Command) -> None:
        try:
            self.commands.add_command(command)
        except Exception as e:
            logger.error(f"Catched exception while adding command <{command}>! {e}")
    
    def __call__(self, command: str, **kwargs) -> None:
        try:
            self.commands.get_command(command)(**kwargs)
        except Exception as e:
            logger.error(f"Catched exception while calling command <{command}> with kwargs={kwargs}! {e}")


class Console(Core):
    def __init__(self, commands: list[command.Command] = []):
        commands.extend([
            command.Command("clear"       , "Clear console"                  , self._clear       , {}),
            command.Command("thread"      , "Start a command in other thread", self._thread      , {"cmd": str}),
            command.Command("show_threads", "Show active threads"            , self._show_threads, {}),
            command.Command("help"        , "Get help menu"                  , self._help        , {}),
            command.Command("exit"        , "Close console"                  , self._exit        , {}),
        ])
        super().__init__(command.CommandTable(commands))
        self.status = False
        
        self.columner = Columner()
        
        self.threads = []
    
    def loop(self) -> None:
        self.status = True
        while self.status:
            try:
                command, *args = input("\ntest > ").split("|")
                self.__call__(command, **self._args_to_kwargs(*args))
            except KeyboardInterrupt:
                continue
            except Exception as e:
                logger.critical(f"{e}")
    
    def _args_to_kwargs(self, *args) -> dict[str, any]:
        kwargs = {}
        for arg in args:
            key, value = arg.split("=")
            
            try:
                arg, _type = value.split("::")
            except Exception as e:
                arg, _type = value, "str"  
            
            match _type:
                case "int":
                    kwargs[key] = int(arg)
                case _:
                    kwargs[key] = arg
        return kwargs
    
    def _clear(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _thread(self, cmd: str, **kwargs) -> None:
        try:  
            _command = self.commands.get_command(cmd)
            
            thread = threading.Thread(target=_command, name=_command.name, kwargs=kwargs)
            thread.start()
            
            self.threads.append(thread)
        except Exception as e:
            logger.error(e)
            return
    
    def _show_threads(self) -> None:
        print(self.columner(
            ['thread', 'command', 'status'],
            [[str(thread.native_id), thread.name, str(thread.is_alive())] for thread in self.threads]
        ))
    
    def _help(self) -> None:
        print("\n\tYou called help menu for console.core...")
        print("\tIf argument must be int, you would write it like: [command]|[name]=[argument]::int\n")
        
        print(self.columner(
            ['command', 'description', 'arguments'],
            [[command.name, command.description, str(command.args)] for command in self.commands.commands.values()]
        ))
    
    def _exit(self) -> None:
        #logger.info("User close console")
        self.status = False
        