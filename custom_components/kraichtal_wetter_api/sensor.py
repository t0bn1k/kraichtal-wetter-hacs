from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSOR_TYPES = [
    EntityDescription(
        key="temp",
        name="Außentemperatur",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
    ),
    EntityDescription(
        key="feels_like",
        name="Gefühlt",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer-lines",
    ),
    EntityDescription(
        key="humidity",
        name="Luftfeuchtigkeit",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:water-percent",
    ),
    EntityDescription(
        key="pressure",
        name="Luftdruck",
        native_unit_of_measurement="hPa",
        icon="mdi:gauge",
    ),
    EntityDescription(
        key="wind",
        name="Windgeschwindigkeit",
        native_unit_of_measurement="km/h",
        icon="mdi:weather-windy",
    ),
    EntityDescription(
        key="gust_max",
        name="Böen max",
        native_unit_of_measurement="km/h",
        icon="mdi:weather-windy",
    ),
    EntityDescription(
        key="rain",
        name="Niederschlag aktuell",
        native_unit_of_measurement="mm",
        icon="mdi:weather-rainy",
    ),
    EntityDescription(
        key="solar",
        name="Solarstrahlung",
        native_unit_of_measurement="W/m²",
        icon="mdi:weather-sunny",
    ),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities(
        [KraichtalWetterSensor(coordinator, description) for description in SENSOR_TYPES],
        True,
    )


class KraichtalWetterSensor(CoordinatorEntity, SensorEntity):
    entity_description: EntityDescription

    def __init__(self, coordinator, description: EntityDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"Kraichtal Wetter {description.name}"
        self._attr_unique_id = f"kraichtal_wetter_{description.key}"

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        return self.coordinator.data["current"].get(self.entity_description.key)
