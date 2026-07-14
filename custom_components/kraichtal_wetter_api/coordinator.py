import logging
from typing import Any

from aiohttp import ClientResponseError

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_API_KEY, CONF_API_URL

_LOGGER = logging.getLogger(__name__)


class KraichtalWetterApiClient:
    def __init__(self, api_url: str, api_key: str | None, session) -> None:
        self._api_url = api_url
        self._api_key = api_key
        self._session = session

    async def async_get_data(self) -> dict[str, Any]:
        url = self._api_url
        if self._api_key and "key=" not in url and "api_key=" not in url and "apikey=" not in url:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}key={self._api_key}"

        response = await self._session.get(url, timeout=10)
        response.raise_for_status()
        data = await response.json()

        if not data.get("ok", True):
            raise UpdateFailed("API returned an unsuccessful response")

        return data

    async def async_update(self) -> dict[str, Any]:
        try:
            data = await self.async_get_data()
            return data
        except ClientResponseError as err:
            _LOGGER.error("Kraichtal Wetter API HTTP error: %s", err)
            raise UpdateFailed(err)
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Kraichtal Wetter API update failed: %s", err)
            raise UpdateFailed(err)
