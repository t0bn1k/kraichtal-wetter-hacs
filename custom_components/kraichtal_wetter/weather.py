from __future__ import annotations

from datetime import datetime, timedelta, timezone

from homeassistant.components.weather import (
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import UnitOfSpeed, UnitOfTemperature
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
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator)
        self._attr_name = "Kraichtal Wetter Forecast"
        self._attr_unique_id = "kraichtal_wetter_forecast"
        self._forecast_cache: list[Forecast] | None = None
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
    def native_temperature(self) -> float | None:
        return self._current().get("temp")

    @property
    def humidity(self) -> float | None:
        return self._current().get("humidity")

    @property
    def native_pressure(self) -> float | None:
        return self._current().get("pressure")

    @property
    def condition(self) -> str | None:
        icon = self._current().get("icon")
        return ICON_MAP.get(icon, "sunny")

    @property
    def wind_bearing(self) -> float | None:
        return self._current().get("wind_dir")

    @property
    def native_wind_speed(self) -> float | None:
        return self._current().get("wind")

    def _build_forecast(self) -> list[Forecast] | None:
        data = self.coordinator.data
        if not isinstance(data, dict):
            return None

        meta = data.get("meta", {})
        generated = meta.get("generated")
        if generated:
            try:
                base_date = datetime.fromisoformat(generated).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            except (ValueError, TypeError):
                base_date = datetime.now(timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
        else:
            base_date = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        forecast = []
        for idx, day in enumerate(data.get("days", [])):
            if not isinstance(day, dict):
                continue

            day_date = base_date + timedelta(days=idx)
            datetime_str = day_date.strftime("%Y-%m-%dT00:00:00+00:00")

            forecast.append(
                {
                    "datetime": datetime_str,
                    "condition": ICON_MAP.get(day.get("icon"), "partlycloudy"),
                    "native_temperature": day.get("tmax"),
                    "native_templow": day.get("tmin"),
                    "precipitation_probability": day.get("pop"),
                    "native_wind_speed": day.get("wind"),
                    "wind_bearing": day.get("wind_dir"),
                }
            )
        return forecast or None

    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast in native units."""
        if self._forecast_cache is not None:
            return self._forecast_cache

        self._forecast_cache = self._build_forecast()
        return self._forecast_cache

    async def async_update(self) -> None:
        """Update the entity and invalidate forecast cache."""
        await super().async_update()
        self._forecast_cache = None
