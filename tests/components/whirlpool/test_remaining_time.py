"""Test Whirlpool remaining-time estimation."""

from datetime import UTC, datetime, timedelta

from homeassistant.components.whirlpool.remaining_time import (
    RemainingTimeEstimate,
    format_remaining_minutes,
)

NOW = datetime(2026, 9, 29, 17, 0, tzinfo=UTC)


def test_running_countdown_advances_without_new_appliance_data() -> None:
    """Test a running countdown advances without fresh appliance data."""
    estimate = RemainingTimeEstimate()
    estimate.observe("running", 77 * 60, NOW)

    assert format_remaining_minutes(estimate.minutes(NOW)) == "1 hr 17 min"
    assert format_remaining_minutes(estimate.minutes(NOW + timedelta(minutes=1))) == (
        "1 hr 16 min"
    )
    assert estimate.minutes(NOW + timedelta(minutes=80)) == 0


def test_repeated_stale_value_does_not_push_deadline_forward() -> None:
    """Test repeated stale values do not extend the estimate."""
    estimate = RemainingTimeEstimate()
    estimate.observe("running", 600, NOW)
    estimate.observe("running", 600, NOW + timedelta(minutes=2))

    assert estimate.minutes(NOW + timedelta(minutes=3)) == 7

    estimate.observe("running", 300, NOW + timedelta(minutes=3))
    assert estimate.minutes(NOW + timedelta(minutes=3)) == 5


def test_pause_freezes_and_resume_restarts_countdown() -> None:
    """Test pause freezes and resume restarts the countdown."""
    estimate = RemainingTimeEstimate()
    estimate.observe("running", 600, NOW)
    estimate.observe("paused", 480, NOW + timedelta(minutes=2))

    assert estimate.minutes(NOW + timedelta(minutes=5)) == 8

    estimate.observe("running", 480, NOW + timedelta(minutes=5))
    assert estimate.minutes(NOW + timedelta(minutes=6)) == 7


def test_complete_shows_zero_and_idle_hides_old_time() -> None:
    """Test completed cycles show zero and idle clears the estimate."""
    estimate = RemainingTimeEstimate()

    assert estimate.minutes(NOW) is None

    estimate.observe("running", 60, NOW)
    estimate.observe("complete", 0, NOW + timedelta(minutes=1))
    assert format_remaining_minutes(estimate.minutes(NOW)) == "0 min"

    estimate.observe("idle", 0, NOW + timedelta(minutes=2))
    assert format_remaining_minutes(estimate.minutes(NOW)) is None
