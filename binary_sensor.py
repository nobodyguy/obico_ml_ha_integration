from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ATTR_ERROR_DETECTED

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Obico binary sensor entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create and add the ObicoBinarySensor entity
    async_add_entities([ObicoBinarySensor(coordinator, entry)])

class ObicoBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a binary sensor for 3D print error detection."""

    def __init__(self, coordinator, entry):
        """Initialize the binary sensor entity."""
        CoordinatorEntity.__init__(self, coordinator)
        BinarySensorEntity.__init__(self)
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "Obico ML Failure Detected"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_error_detection"
        self._attr_is_on = False

    @property
    def is_on(self) -> bool:
        """Return True if an error was detected."""
        if self.coordinator.api_enabled:
            return self.coordinator.data.get(ATTR_ERROR_DETECTED, False)
        
        return False

    @property
    def available(self) -> bool:
        """Return True if the coordinator's last update was successful."""
        return self.coordinator.last_update_success