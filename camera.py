from homeassistant.components.camera import Camera
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Obico entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create and add the ObicoCamera entity
    async_add_entities([ObicoCamera(coordinator, entry)])

class ObicoCamera(CoordinatorEntity, Camera):
    """Representation of a camera entity showing error detections."""

    def __init__(self, coordinator, entry):
        """Initialize the camera entity."""
        CoordinatorEntity.__init__(self, coordinator)  # Initialize CoordinatorEntity
        Camera.__init__(self)  # Initialize Camera
        self._entry = entry
        self._attr_name = "Obico ML Detection Camera"
        self._attr_unique_id = f"{DOMAIN}_camera"
        self._camera_entity_id = entry.data["camera_entity"]
        self._last_image = None
        self._camera_available = False  # Flag to check camera availability

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        """Return the latest image with error detections."""
        return self.coordinator.data.get("image_with_errors")

    @property
    def available(self) -> bool:
        """Return if the camera is available."""
        return self.coordinator.last_update_success and self.hass.states.get(self._camera_entity_id) is not None
