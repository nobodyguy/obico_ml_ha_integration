from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS
from .coordinator import ObicoDataUpdateCoordinator
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Legacy setup function. We use config flow for setup."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Obico detection from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Import data from config entry
    coordinator = ObicoDataUpdateCoordinator(
        hass,
        url=entry.data["url"],
        camera_entity=entry.data["camera_entity"],
        interval=entry.data["interval"],
        threshold=entry.data["threshold"],
    )

    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator so it can be accessed by entities
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
