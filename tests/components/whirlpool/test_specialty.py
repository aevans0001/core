"""Test Whirlpool Specialty cycle handling."""

import pytest

from homeassistant.components.whirlpool.specialty import (
    ATTR_CYCLE_NAME,
    ATTR_CYCLE_SELECT,
    ATTR_DOWNLOAD_AND_GO,
    ATTR_SOIL_LEVEL,
    ATTR_SPECIALTY_CYCLE_ID,
    ATTR_SPIN_SPEED,
    ATTR_TEMPERATURE,
    build_specialty_payload,
)


def test_specialty_payload() -> None:
    """Test the exact DDM-derived Specialty payload."""
    assert build_specialty_payload("diapers") == {
        ATTR_DOWNLOAD_AND_GO: "1",
        ATTR_SPECIALTY_CYCLE_ID: "1",
        ATTR_CYCLE_SELECT: "92",
        ATTR_SOIL_LEVEL: "2",
        ATTR_SPIN_SPEED: "5",
        ATTR_TEMPERATURE: "4",
        ATTR_CYCLE_NAME: "Diapers",
    }


def test_unknown_specialty_cycle() -> None:
    """Test an unknown Specialty cycle is rejected before a write."""
    with pytest.raises(ValueError):
        build_specialty_payload("not_a_cycle")
