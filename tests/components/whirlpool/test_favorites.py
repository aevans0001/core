"""Test Whirlpool Home Assistant-local Favorites."""

import pytest

from homeassistant.components.whirlpool.favorites import (
    ATTR_DRYNESS,
    ATTR_MANUAL_DRY_TIME,
    ATTR_TEMPERATURE,
    DryerFavorite,
    dryer_favorite_writes,
    normalize_name,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Gym Clothes", "Gym Clothes"),
        ("  Gym   Clothes  ", "Gym Clothes"),
        ("socks", "socks"),
    ],
)
def test_normalize_favorite_name(raw: str, expected: str) -> None:
    """Test Favorite names are normalized without changing their meaning."""
    assert normalize_name(raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "None", " none "])
def test_invalid_favorite_name(raw: str) -> None:
    """Test unusable Favorite names are rejected."""
    with pytest.raises(ValueError):
        normalize_name(raw)


def test_dryer_favorite_writes() -> None:
    """Test a dryer Favorite becomes validated single-attribute writes."""
    recipe = DryerFavorite(
        what="regular",
        how="normal",
        temperature="warm_mid",
        dryness="normal",
    )

    writes = dryer_favorite_writes(recipe)

    assert writes == [
        {ATTR_TEMPERATURE: "4"},
        {ATTR_DRYNESS: "4"},
    ]


def test_dryer_favorite_manual_time_validation() -> None:
    """Test manual dry time is validated against the destination cycle."""
    recipe = DryerFavorite(
        what="regular",
        how="timed_dry",
        manual_dry_time="60",
    )

    assert dryer_favorite_writes(recipe)[-1] == {ATTR_MANUAL_DRY_TIME: "3600"}

    invalid = DryerFavorite(
        what="regular",
        how="normal",
        manual_dry_time="60",
    )
    with pytest.raises(ValueError):
        dryer_favorite_writes(invalid)
