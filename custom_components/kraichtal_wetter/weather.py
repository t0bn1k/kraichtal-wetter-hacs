from __future__ import annotations

from homeassistant.components.weather import WeatherEntity, WeatherEntityFeature
from homeassistant.const import UnitOfSpeed
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


ICON_MAP = {
    "suncloud": "partlycloudy",
    "storm": "lightning",
    "sunstorm": "storm",
    "storm-rain": "pouring",
    "cloud": "cloudy",
    "ovc": "cloudy",
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([KraichtalWetterWeather(coordinator, entry)], True)


class KraichtalWetterWeather(CoordinatorEntity, WeatherEntity):
    _attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator)
        self._attr_name = "Kraichtal Wetter Forecast"
        self._attr_unique_id = "kraichtal_wetter_forecast"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Kraichtal Wetter",
            manufacturer="Kraichtal Wetter",
            model="Kraichtal Wetter Station",
            configuration_url=entry.data.get("api_url", ""),
        )

    def _current(self) -> dict:
        data = self.coordinator.data
        if not isinstance(data, dict):
            return {}
        current = data.get("current")
        return current if isinstance(current, dict) else {}

    @property
    def temperature(self) -> float | None:
        return self._current().get("temp")

    @property
    def humidity(self) -> float | None:
        return self._current().get("humidity")

    @property
    def pressure(self) -> float | None:
        return self._current().get("pressure")

    @property
    def condition(self) -> str | None:
        icon = self._current().get("icon")
        return ICON_MAP.get(icon, "sunny")

    @property
    def forecast(self):
        data = self.coordinator.data
        if not isinstance(data, dict):
            return None

        forecast = []
        for day in data.get("days", []):
            if not isinstance(day, dict):
                continue
            forecast.append(
                {
                    "datetime": day.get("date"),
                    "condition": ICON_MAP.get(day.get("icon"), "partlycloudy"),
                    "temperature": day.get("tmax"),
                    "templow": day.get("tmin"),
                    "precipitation_probability": day.get("pop"),
                    "wind_speed": day.get("wind"),
                    "wind_bearing": day.get("wind_dir"),
                }
            )
        return forecast or None
