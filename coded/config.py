import os
from pathlib import Path
from dotenv import load_dotenv

import cpat_model.constants as c

load_dotenv()

# Read environment variables
DATA_ENVIRONMENT = os.getenv("DATA_ENVIRONMENT", "dummy").lower()
REAL_DATA_PATH = os.getenv("REAL_DATA_PATH")
# the data live in the repository's data/ folder; a relative path is taken from coded/
DUMMY_DATA_PATH = os.getenv("DUMMY_DATA_PATH", "../data/dummy")

# Toggle logic
if DATA_ENVIRONMENT == "real":
    if not REAL_DATA_PATH:
        raise ValueError("REAL_DATA_PATH must be set when DATA_ENVIRONMENT is 'real'")
    DATA_PATH = Path(REAL_DATA_PATH)
else:
    DATA_PATH = (Path(__file__).resolve().parent / DUMMY_DATA_PATH).resolve()


SCENARIOS = {
    'Scenario 0': {},
    'Scenario 1': {
        'scenario_type': c.CARBON_TAX
    },
}
