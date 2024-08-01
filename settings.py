import os

APP_NAME = "Time to Vote"
AIDIGEST_PAGE = "https://theaidigest.org/"
FEEDBACK_PAGE = ""

DEVELOPER = "Odin"
PARTNERS = "..."

CREATE_LOG_FILES = False

#####

DELIBERATION_TIME = 240



#####

# Get the directory of the current script (which is in the project root folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(SCRIPT_DIR, 'files')
LOGS_DIR = os.path.join(SCRIPT_DIR, 'logs')

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR, exist_ok=True)

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR, exist_ok=True)