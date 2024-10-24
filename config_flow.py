import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_INTERVAL, DEFAULT_THRESHOLD, DEFAULT_URL

def _create_schema(config_entry=None):
    if config_entry:
        return vol.Schema({
            vol.Required("url", default=config_entry.options.get("url", DEFAULT_URL)): str,
            vol.Required("interval", default=config_entry.options.get("interval", DEFAULT_INTERVAL)): int,
            vol.Required("camera_entity", default=config_entry.options.get("camera_entity", "camera.your_entity")): str,
            vol.Optional("threshold", default=config_entry.options.get("threshold", DEFAULT_THRESHOLD)): float,
        })
    else:
        return vol.Schema({
            vol.Required("url", default=DEFAULT_URL): str,
            vol.Required("interval", default=DEFAULT_INTERVAL): int,
            vol.Required("camera_entity", default="camera.your_entity"): str,
            vol.Optional("threshold", default=DEFAULT_THRESHOLD): float,
        })

class ObicoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            camera_id = user_input["camera_entity"].replace("camera.", "")
            await self.async_set_unique_id(f"{DOMAIN}_{camera_id}", raise_on_progress=False)
            return self.async_create_entry(title=f"Obico ML - {camera_id}", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=_create_schema()
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ObicoOptionsFlow(config_entry)


class ObicoOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_create_schema(self.config_entry)
        )
