import logging
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from aiohttp import ClientResponseError, ClientTimeout

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)

REQUEST_TIMEOUT = ClientTimeout(total=10)

# Status codes that mean the API key is wrong or no longer valid; these must
# trigger the reauth flow instead of a plain update failure.
AUTH_ERROR_STATUSES = (401, 403)


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

        async with self._session.get(url, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            data = await response.json()

        if not isinstance(data, dict):
            raise UpdateFailed("API returned an unexpected payload")

        if not data.get("ok", True):
            raise UpdateFailed("API returned an unsuccessful response")

        return data

    async def async_update(self) -> dict[str, Any]:
        try:
            return await self.async_get_data()
        except UpdateFailed:
            raise
        except ClientResponseError as err:
            # Do not log `err` directly, and do not chain it via `from err`:
            # aiohttp includes the full request URL (with the API key query
            # param) in its string repr, which would otherwise still leak
            # via the exception's __cause__ if the chain is ever printed.
            if err.status in AUTH_ERROR_STATUSES:
                _LOGGER.warning(
                    "Kraichtal Wetter rejected the API key (HTTP %s), starting reauth",
                    err.status,
                )
                raise ConfigEntryAuthFailed("Invalid API key") from None

            _LOGGER.error("Kraichtal Wetter HTTP error: %s %s", err.status, err.message)
            raise UpdateFailed(f"HTTP error {err.status}") from None
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Kraichtal Wetter update failed: %s", err)
            raise UpdateFailed(f"Update failed: {err}") from None
