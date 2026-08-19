import logging
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from aiohttp import ClientResponseError, ClientTimeout

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)

REQUEST_TIMEOUT = ClientTimeout(total=10)

# Status codes that mean the API key is wrong or no longer valid; these must
# trigger the reauth flow instead of a plain update failure. Confirmed against
# the API: 401 = key missing, 403 = key invalid.
AUTH_ERROR_STATUSES = (401, 403)

# Query parameter names the API historically accepted for the key.
KEY_PARAM_NAMES = ("key", "api_key", "apikey")


def _split_api_key(api_url: str) -> tuple[str, str | None]:
    """Split a key carried in the URL off into a separate value.

    The API accepts the key either as a `key` query parameter or as an
    `X-API-Key` header. We always use the header: aiohttp embeds the request
    URL in `ClientResponseError`'s string form, so a key in the query string
    can reach the log through any traceback or exception chain — which is
    exactly how it leaked before 0.4.4. Headers are not part of that output.
    """
    parsed = urlparse(api_url)
    params = parse_qs(parsed.query)

    key = next((params[name][0] for name in KEY_PARAM_NAMES if params.get(name)), None)
    for name in KEY_PARAM_NAMES:
        params.pop(name, None)

    flat = {k: v[0] for k, v in params.items()}
    return urlunparse(parsed._replace(query=urlencode(flat))), key


class KraichtalWetterClient:
    def __init__(self, api_url: str, api_key: str | None, session) -> None:
        # Any key configured into the URL is moved to the header too, so no
        # code path can put it back into a request URL.
        self._api_url, url_key = _split_api_key(api_url)
        self._api_key = api_key or url_key
        self._session = session

    @property
    def _headers(self) -> dict[str, str]:
        return {"X-API-Key": self._api_key} if self._api_key else {}

    async def async_get_data(self) -> dict[str, Any]:
        async with self._session.get(
            self._api_url, headers=self._headers, timeout=REQUEST_TIMEOUT
        ) as response:
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
            # Never log `err` itself and never chain it via `from err`: its
            # string form carries the request URL. The key no longer rides in
            # that URL (see _split_api_key), but keep both guards so a future
            # query parameter cannot quietly become a leak again.
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
