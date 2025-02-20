#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

from dotenv import load_dotenv
import logging
import os

#############################################
#############################################
##
##  Load .env config and check items
##
#############################################
#############################################

if load_dotenv("log.env"):
    required_items = {"logging-level", "logging-time-formatter", "logging-text-formatter",
                      "logging-text-formatter-colored", "logging-use-color-filter"}
    optimal_items = {}
    
    not_found = set()
    for item in required_items:
        if item not in os.environ.keys():
            print(f"\033[33mLoggingApp: not found required item <{item}> in log.env file!\033[0m")
            not_found.add(item)
    
    if len(not_found) != 0:
        exit("\033[31mLoggingApp: add missed required items!\033[0m")
    
    for item in optimal_items:
        if item not in os.environ.keys() and os.environ.get("print-missed-items", True):
            print(f"\033[33mLoggingApp: not found optimal item <{item}> in .env file!\033[0m")
    
    print("\033[32mLoggingApp: log.env config loaded!\033[0m")
else:
    exit("\033[31mLoggingApp: not found log.env file with config!\033[0m")

#############################################
#############################################
##
##  Prepare logging
##
#############################################
#############################################

if int(os.environ.get("logging-use-color-filter", True)):
    logging.basicConfig(
        level=int(os.environ.get("logging-level", 20)),
        datefmt=os.environ.get("logging-time-formatter", ""),
        format=os.environ.get("logging-text-formatter-colored", "")
    )
else:
    logging.basicConfig(
        level=int(os.environ.get("logging-level", 20)),
        datefmt=os.environ.get("logging-time-formatter", ""),
        format=os.environ.get("logging-text-formatter", "")
    )

#############################################
#############################################
##
##  Main classes and functions
##
#############################################
#############################################

class ColorFilter(logging.Filter):
    colors = {
        "DEBUG"     : "\033[34m",
        "INFO"      : "\033[36m",
        "WARN"      : "\033[33m",
        "WARNING"   : "\033[33m",
        "ERROR"     : "\033[31m",
        "CRITICAL"  : "\033[31m",
    }
    def filter(self, record: logging.LogRecord) -> bool:
        record.color = self.colors.get(record.levelname)
        record.end   = "\033[0m"
        return True

def basicConfig(*args, **kwargs) -> None:
    logging.basicConfig(*args, **kwargs)

def createColorFilter() -> ColorFilter:
    return ColorFilter()

def addFilter(logger: logging.Logger, filter: ColorFilter):
    logger.addFilter(filter)

def getLogger(name: str) -> logging.Logger:
    return logging.getLogger(name)

def prepareLogger(name: str) -> logging.Logger:
    logger = getLogger(name)
    if os.environ.get("logging-use-color-filter", True):
        filter = createColorFilter()
        addFilter(logger, filter)
    return logger