import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

def _create_schema(config_entry=None):
    if config_entry:
        return vol.Schema({
            vol.Required("url", default=config_entry.options.get("url", "http://XXXXXXXX-obico-ml-ha-addon:3333/detect/")): str,
            vol.Required("interval", default=config_entry.options.get("interval", 10)): int,
            vol.Required("camera_entity", default=config_entry.options.get("camera_entity", "camera.your_entity")): str,
            vol.Optional("threshold", default=config_entry.options.get("threshold", 0.2)): float,
        })
    else:
        return vol.Schema({
            vol.Required("url", default="http://XXXXXXXX-obico-ml-ha-addon:3333/detect/"): str,
            vol.Required("interval", default=10): int,
            vol.Required("camera_entity", default="camera.your_entity"): str,
            vol.Optional("threshold", default=0.2): float,
        })

class ObicoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Obico ML", data=user_input)

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