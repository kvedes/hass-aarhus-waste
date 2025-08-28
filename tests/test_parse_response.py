import pytest
import json
from custom_components.aarhuswaste.model import Schedule

@pytest.fixture
def data():
    _data = """[
    {
        "standId": "0000",
        "standName": "Vej 20, 8000 Aarhus",
        "plannedLoads": [
            {
                "date": "2025-09-17T00:00:00+00:00",
                "fractions": [
                    "Restaffald",
                    "Madaffald"
                ]
            },
            {
                "date": "2025-09-23T00:00:00+00:00",
                "fractions": [
                    "Papir",
                    "Pap",
                    "Tekstiler"
                ]
            },
            {
                "date": "2025-09-29T00:00:00+00:00",
                "fractions": [
                    "Plast",
                    "Mad- og drikkekartoner",
                    "Glas",
                    "Metal"
                ]
            }]}]"""
    return json.loads(_data)


def test_deserialization(data) -> None:
    # Arrange / Act
    uut = Schedule.from_dict(data)

    # Assert
    assert len(uut.pickups) == 3