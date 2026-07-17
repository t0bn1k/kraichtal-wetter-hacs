import logging
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from aiohttp import ClientResponseError

from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)


class KraichtalWetterClient:
    def __init__(self, api_url: str, api_key: str | None, session) -> None:
        self._api_url = api_url
        self._api_key = api_key
        self._session = session

    def _build_url(self) -> str:
        parsed = urlparse(self._api_url)
        params = parse_qs(parsed.query)

        has_key = any(k in params for k in ("key", "api_key", "apikey"))

        if self._api_key and not has_key:
            params["key"] = [self._api_key]

        flat = {k: v[0] for k, v in params.items()}
        return urlunparse(parsed._replace(query=urlencode(flat)))

    async def async_get_data(self) -> dict[str, Any]:
        url = self._build_url()

        response = await self._session.get(url, timeout=10)
        response.raise_for_status()
        data = await response.json()

        if not data.get("ok", True):
            raise UpdateFailed("API returned an unsuccessful response")

        return data

    async def async_update(self) -> dict[str, Any]:
        try:
            return await self.async_get_data()
        except UpdateFailed:
            raise
        except ClientResponseError as err:
            _LOGGER.error("Kraichtal Wetter HTTP error: %s", err)
            raise UpdateFailed(err)
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Kraichtal Wetter update failed: %s", err)
            raise UpdateFailed(err)
