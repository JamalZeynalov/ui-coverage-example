import rootpath
from dotenv import load_dotenv
from environs import Env

load_dotenv(f"{rootpath.detect()}/.env")
env = Env()

# Project settings
ENVIRONMENT_NAME = env.str("ENVIRONMENT", default="stage_local")


# Timeouts
LONG_TIMEOUT = 60000
DEFAULT_TIMEOUT = 20000
SHORT_TIMEOUT = 5000
MIN_TIMEOUT = 3000
MICRO_TIMEOUT = 1000
NO_TIMEOUT = 0.01
