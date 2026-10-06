"""Home Assistant metadata for Whirlpool Specialty washer cycles."""

from dataclasses import dataclass
from typing import Final

from whirlpool.washer import Washer


@dataclass(frozen=True)
class SpecialtyPreset:
    """UI-relevant values applied by one Specialty preset."""

    temperature: int
    spin_speed: int
    soil_level: int


SPECIALTY_PRESETS: Final[dict[str, SpecialtyPreset]] = {
    "coats_jackets": SpecialtyPreset(0, 4, 2),
    "diapers": SpecialtyPreset(4, 5, 2),
    "sleeping_bags": SpecialtyPreset(2, 3, 2),
    "comforters": SpecialtyPreset(2, 3, 0),
    "machine_wash_curtains": SpecialtyPreset(0, 3, 0),
    "swimwear": SpecialtyPreset(0, 3, 0),
    "activewear": SpecialtyPreset(2, 5, 2),
    "jeans": SpecialtyPreset(2, 5, 1),
    "blankets": SpecialtyPreset(3, 5, 1),
    "lingerie": SpecialtyPreset(1, 2, 0),
    "business_casual": SpecialtyPreset(1, 4, 1),
}


def is_specialty_model_supported(washer: Washer) -> bool:
    """Return whether the library exposes Specialty cycles for this washer."""
    return bool(washer.get_supported_specialty_cycles())


def supports_specialty_cycles(washer: Washer) -> bool:
    """Return whether Specialty cycles are currently available."""
    return bool(washer.get_supported_specialty_cycles())


async def set_specialty_cycle(washer: Washer, option: str) -> bool:
    """Select a Specialty cycle through the public library API."""
    return await washer.set_specialty_cycle(option)
