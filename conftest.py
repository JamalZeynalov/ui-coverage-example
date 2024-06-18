import json
import os
from pathlib import Path
from typing import Dict, List

import rootpath

pytest_plugins = [
    "utils.fixtures.driver",
    "utils.fixtures.applications",
]

# pylint: disable=unused-argument
used_locators: Dict[str, List[str]] = {}
directory = rootpath.detect() / Path("ui_coverage")


def pytest_sessionstart(session):
    """Create the directory for storing used locators at the start of the session."""
    os.makedirs(directory, exist_ok=True)


def pytest_sessionfinish(session, exitstatus):
    """This hook is used to create used_locators JSON files for each xdist worker.
    All locators used in tests are stored in used_locators dictionary.
    After the test session is finished (for each thread), its dictionary is dumped to a JSON file.
    """
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", None)
    filepath = directory / f"used_locators_{worker_id}.json"

    if used_locators and worker_id:
        with open(filepath, "w") as file:
            json.dump(used_locators, file, indent=4, sort_keys=True)
