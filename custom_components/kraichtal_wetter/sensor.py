from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSOR_TYPES = [
    SensorEntityDescription(
        key="temp",
        name="Außentemperatur",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="feels_like",
        name="Gefühlt",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-lines",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="dewpoint",
        name="Taupunkt",
        native_unit_of_measurement="°C",
        icon="mdi:water-percent",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="humidity",
        name="Luftfeuchtigkeit",
        native_unit_of_measurement="%",
        icon="mdi:water-percent",
        device_class="humidity",
    ),
    SensorEntityDescription(
        key="pressure",
        name="Luftdruck",
        native_unit_of_measurement="hPa",
        icon="mdi:gauge",
        device_class="pressure",
    ),
    SensorEntityDescription(
        key="wind",
        name="Windgeschwindigkeit",
        native_unit_of_measurement="km/h",
        icon="mdi:weather-windy",
    ),
    SensorEntityDescription(
        key="wind_dir",
        name="Windrichtung",
        native_unit_of_measurement="°",
        icon="mdi:compass",
    ),
    SensorEntityDescription(
        key="gust_max",
        name="Böen max",
        native_unit_of_measurement="km/h",
        icon="mdi:weather-windy",
    ),
    SensorEntityDescription(
        key="solar",
        name="Solarstrahlung",
        native_unit_of_measurement="W/m²",
        icon="mdi:weather-sunny",
    ),
    SensorEntityDescription(
        key="rain",
        name="Niederschlag aktuell",
        native_unit_of_measurement="mm",
        icon="mdi:weather-rainy",
    ),
    SensorEntityDescription(
        key="tmax_today",
        name="Maximale Temperatur heute",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-high",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="tmin_today",
        name="Minimale Temperatur heute",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-low",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="rain_today",
        name="Niederschlag heute",
        native_unit_of_measurement="mm",
        icon="mdi:weather-rainy",
    ),
    SensorEntityDescription(
        key="warnings",
        name="Warnungen",
        icon="mdi:alarm",
    ),
    SensorEntityDescription(
        key="obs_date",
        name="Beobachtungsdatum",
        icon="mdi:calendar",
    ),
    SensorEntityDescription(
        key="obs_time",
        name="Beobachtungszeit",
        icon="mdi:clock",
    ),
    SensorEntityDescription(
        key="realtime",
        name="Echtzeitdaten",
        icon="mdi:clock-fast",
    ),
    SensorEntityDescription(
        key="station_today.tmax",
        name="Station heute Tmax",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-high",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="station_today.tmin",
        name="Station heute Tmin",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-low",
        device_class="temperature",
    ),
    SensorEntityDescription(
        key="station_today.gust",
        name="Station heute Böe",
        native_unit_of_measurement="km/h",
        icon="mdi:weather-windy",
    ),
    SensorEntityDescription(
        key="station_today.press_max",
        name="Station heute Luftdruck max",
        native_unit_of_measurement="hPa",
        icon="mdi:gauge",
        device_class="pressure",
    ),
    SensorEntityDescription(
        key="station_today.press_min",
        name="Station heute Luftdruck min",
        native_unit_of_measurement="hPa",
        icon="mdi:gauge",
        device_class="pressure",
    ),
]


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    async_add_entities(
        [KraichtalWetterSensor(coordinator, entry, description) for description in SENSOR_TYPES],
        True,
    )


def _resolve_current_value(data: dict[str, object], key: str):
    current = data.get("current") or {}
    if not isinstance(current, dict):
        return None

    if "." not in key:
        return current.get(key)

    value = current
    for part in key.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


class KraichtalWetterSensor(CoordinatorEntity, SensorEntity):
    entity_description: SensorEntityDescription

    def __init__(self, coordinator, entry, description: SensorEntityDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"Kraichtal Wetter {description.name}"
        self._attr_unique_id = f"kraichtal_wetter_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Kraichtal Wetter",
            manufacturer="Kraichtal Wetter",
            model="Kraichtal Wetter Station",
            configuration_url=entry.data.get("api_url", ""),
        )

    @property
    def native_value(self):
        return _resolve_current_value(self.coordinator.data, self.entity_description.key)
