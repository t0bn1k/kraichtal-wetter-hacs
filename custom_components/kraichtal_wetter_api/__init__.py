import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_API_KEY, CONF_API_URL, DEFAULT_API_URL, DEFAULT_SCAN_INTERVAL, DOMAIN, PLATFORMS
from .coordinator import KraichtalWetterApiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_url = entry.data.get(CONF_API_URL, DEFAULT_API_URL)
    # Backwards compatibility: older installs may have stored the API key as
    # 'api_key' or 'apikey'. Prefer the configured `CONF_API_KEY` (now 'key').
    api_key = entry.data.get(CONF_API_KEY) or entry.data.get("api_key") or entry.data.get("apikey")
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    session = async_get_clientsession(hass)
    client = KraichtalWetterApiClient(api_url, api_key, session)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Kraichtal Wetter API",
        update_method=client.async_update,
        update_interval=timedelta(seconds=scan_interval),
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise UpdateFailed(err)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "client": client,
    }

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
