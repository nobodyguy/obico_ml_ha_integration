from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Obico entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create and add the ObicoConfidenceSensor entity
    async_add_entities([ObicoConfidenceSensor(coordinator, entry)])

class ObicoConfidenceSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for average failure detection confidence."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        CoordinatorEntity.__init__(self, coordinator)
        SensorEntity.__init__(self)
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "Obico ML Failure Detection Confidence"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_failure_detection_confidence"

    @property
    def state(self):
        # If there is no data or no detections, return None to indicate N/A
        if self.coordinator.api_enabled is False:
            return None
        avg_confidence = self.coordinator.data.get("avg_confidence", None)
        return avg_confidence

    @property
    def unit_of_measurement(self):
        return "%"

    @property
    def device_class(self):
        return "measurement"

    @property
    def available(self):
        """Return True if the sensor is available (i.e., data is valid)."""
        # Sensor is available if coordinator has valid data
        return self.coordinator.data is not None
