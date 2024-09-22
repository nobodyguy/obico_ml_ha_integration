from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Obico entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create and add the ObicoSwitch entity
    async_add_entities([ObicoSwitch(coordinator, entry)])

class ObicoSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a switch to enable/disable communication with the API."""

    def __init__(self, coordinator, entry):
        """Initialize the switch."""
        CoordinatorEntity.__init__(self, coordinator)
        SwitchEntity.__init__(self)
        self._entry = entry
        self._attr_name = "Obico ML Communication"
        self._attr_unique_id = f"{DOMAIN}_api_communication"
        self._is_on = coordinator.api_enabled

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the API communication on."""
        self._is_on = True
        self.coordinator.api_enabled = True  # Enable API communication
        self.coordinator.async_request_refresh()  # Fetch data immediately
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the API communication off."""
        self._is_on = False
        self.coordinator.api_enabled = False  # Disable API communication
        self.async_write_ha_state()
