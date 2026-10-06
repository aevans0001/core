"""Test Whirlpool Specialty cycle metadata."""

from homeassistant.components.whirlpool.specialty import SPECIALTY_PRESETS


def test_specialty_preset_metadata() -> None:
    """Test DDM-derived UI metadata for a Specialty preset."""
    preset = SPECIALTY_PRESETS["diapers"]

    assert preset.temperature == 4
    assert preset.spin_speed == 5
    assert preset.soil_level == 2


def test_all_specialty_presets_present() -> None:
    """Test all validated Download & Go presets remain exposed."""
    assert set(SPECIALTY_PRESETS) == {
        "activewear",
        "blankets",
        "business_casual",
        "coats_jackets",
        "comforters",
        "diapers",
        "jeans",
        "lingerie",
        "machine_wash_curtains",
        "sleeping_bags",
        "swimwear",
    }
