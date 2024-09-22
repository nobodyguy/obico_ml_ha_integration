DOMAIN = "obico_ml"
PLATFORMS = ["binary_sensor", "switch", "camera"]
DEFAULT_NAME = "Obico ML"
DEFAULT_URL = "http://XXXXXXXX-obico-ml-ha-addon:3333/detect/"
DEFAULT_INTERVAL = 60  # in seconds
DEFAULT_THRESHOLD = 0.5

CONF_URL = "url"
CONF_INTERVAL = "interval"
CONF_CAMERA_ENTITY = "camera_entity"
CONF_THRESHOLD = "threshold"

ATTR_ERROR_DETECTED = "error_detected"
ATTR_IMAGE_WITH_ERRORS = "image_with_errors"
