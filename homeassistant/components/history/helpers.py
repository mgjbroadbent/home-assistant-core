"""Helpers for the history integration."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime as dt

from homeassistant.components.recorder import get_instance
from homeassistant.core import HomeAssistant


def entities_may_have_state_changes_after(
    hass: HomeAssistant, entity_ids: Iterable, start_time: dt, no_attributes: bool
) -> bool:
    """Check the state machine to see if entities have changed since start time."""
    for entity_id in entity_ids:
        state = hass.states.get(entity_id)
        if state is None:
            return True

        state_time = state.last_changed if no_attributes else state.last_updated
        if state_time > start_time:
            return True

    return False


def has_states_before(hass: HomeAssistant, run_time: dt) -> bool:
    """Check if the recorder has states as old or older than run_time.

    Returns True if there may be such states.
    """
    oldest_ts = get_instance(hass).states_manager.oldest_ts
    return oldest_ts is not None and run_time.timestamp() >= oldest_ts
