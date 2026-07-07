from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app as fastapi_app

BASELINE_ACTIVITIES = deepcopy(activities)


@pytest.fixture()
def client():
    activities.clear()
    activities.update(deepcopy(BASELINE_ACTIVITIES))
    with TestClient(fastapi_app) as test_client:
        yield test_client
