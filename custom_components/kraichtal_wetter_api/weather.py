from __future__ import annotations

from homeassistant.components.weather import WeatherEntity
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
    async_add_entities([KraichtalWetterWeather(coordinator)], True)


class KraichtalWetterWeather(CoordinatorEntity, WeatherEntity):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_name = "Kraichtal Wetter Forecast"
        self._attr_unique_id = "kraichtal_wetter_forecast"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, getattr(coordinator, "entry_id", "kraichtal_wetter_api"))},
            name="Kraichtal Wetter API",
            manufacturer="Kraichtal Wetter",
            model="Kraichtal Wetter Station",
            configuration_url=getattr(coordinator, "api_url", ""),
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def temperature(self) -> float | None:
        return self.coordinator.data["current"].get("temp")

    @property
    def humidity(self) -> float | None:
        return self.coordinator.data["current"].get("humidity")

    @property
    def pressure(self) -> float | None:
        return self.coordinator.data["current"].get("pressure")

    @property
    def condition(self) -> str | None:
        icon = self.coordinator.data["current"].get("icon")
        return ICON_MAP.get(icon, "sunny")

    @property
    def forecast(self):
        forecast = []
        for day in self.coordinator.data.get("days", []):
            forecast.append(
                {
                    "datetime": None,
                    "condition": ICON_MAP.get(day.get("icon"), "partlycloudy"),
                    "temperature": day.get("tmax"),
                    "templow": day.get("tmin"),
                    "precipitation_probability": day.get("pop"),
                    "wind_speed": day.get("wind"),
                    "wind_bearing": day.get("wind_dir"),
                }
            )
        return forecast
