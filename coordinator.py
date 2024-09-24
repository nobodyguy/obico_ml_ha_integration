from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.network import get_url
from homeassistant.core import HomeAssistant
import aiohttp
import logging
import base64

_LOGGER = logging.getLogger(__name__)

class ObicoDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, url: str, camera_entity: str, interval: int, threshold: float):
        self._url = url
        self._camera_entity = camera_entity
        self._threshold = threshold
        self.api_enabled = False  # Initially enabled

        super().__init__(
            hass,
            _LOGGER,
            name="Obico ML",
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self):
        if not self.api_enabled:
            _LOGGER.info("API communication is disabled.")
            return None

        # Get image URL from the camera entity
        camera_state = self.hass.states.get(self._camera_entity)
        if camera_state is None:
            _LOGGER.warning(f"Camera entity {self._camera_entity} not found or unavailable")
            return None
        camera_image_url = camera_state.attributes.get("entity_picture")
        if camera_image_url is None:
            raise ValueError(f"Camera entity {self._camera_entity} does not provide an image URL")

        camera_image_url = f"{get_url(self.hass)}{camera_image_url}"

        # Make the request to the detection API
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(camera_image_url) as response:
                    original_image_data = await response.read()  # Raw image data (bytes)
                    original_image_base64 = base64.b64encode(original_image_data).decode('utf-8')
                    
                payload = {
                    "img": original_image_base64,
                    "threshold": self._threshold
                }
                async with session.post(self._url, json=payload) as detection_response:
                    if detection_response.status != 200:
                        raise Exception(f"API call failed: {detection_response.status}")
                    
                    detection_data = await detection_response.json()
                    detections = detection_data.get("detections", [])
                    error_detected = detections != []

                    # Calculate average confidence
                    avg_confidence = 0
                    if detections:
                        confidences = [detection[1] for detection in detections]
                        avg_confidence = (sum(confidences) / len(confidences)) * 100
                        avg_confidence = round(avg_confidence, 2)

                    image_with_errors_base64 = detection_data.get("image_with_detections", None)
                    if image_with_errors_base64:
                        image_with_errors = base64.b64decode(image_with_errors_base64)

                    return {
                        "image_with_errors": image_with_errors,
                        "error_detected": error_detected,
                        "avg_confidence": avg_confidence,
                    }
            except Exception as err:
                _LOGGER.error(f"Error fetching data from Obico API: {err}")
                raise
