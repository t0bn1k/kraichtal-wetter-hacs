from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_API_URL, CONF_API_KEY, DEFAULT_SCAN_INTERVAL, DEFAULT_API_URL, DOMAIN


class KraichtalWetterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        if user_input is not None:
            # Normalize legacy field names: allow users coming from older
            # installs (where the field may be 'api_key') to continue working.
            data = dict(user_input)
            if "api_key" in data and CONF_API_KEY not in data:
                data[CONF_API_KEY] = data.pop("api_key")
            # Set the baked-in URL so users only provide the key.
            data[CONF_API_URL] = DEFAULT_API_URL
            return self.async_create_entry(title="Kraichtal Wetter", data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
        )

    def _get_schema(self):
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol

        return vol.Schema(
            {
                # URL is fixed by the integration; user only provides the key.
                vol.Optional(CONF_API_KEY): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_int,
            }
        )
