# Changelog

Alle signifikanten Änderungen an diesem Projekt werden in diesem Dokument festgehalten.

## [0.0.1] - 2026-07-14
### Hinzugefügt
- Erste Version der `Kraichtal Wetter API` Home Assistant Custom Integration.
- Unterstützung einer `config_flow`-basierten Einrichtung.
- Sensor-Plattform mit folgenden Entitäten:
  - `sensor.kraichtal_wetter_temp`
  - `sensor.kraichtal_wetter_feels_like`
  - `sensor.kraichtal_wetter_humidity`
  - `sensor.kraichtal_wetter_pressure`
  - `sensor.kraichtal_wetter_wind`
  - `sensor.kraichtal_wetter_gust_max`
  - `sensor.kraichtal_wetter_rain`
  - `sensor.kraichtal_wetter_solar`
- Weather-Plattform mit `weather.kraichtal_wetter_forecast`.
- Dokumentation für HACS und Dashboard-Visualisierung.
- Release-Strategie und Testplan hinzugefügt.

## Unveröffentlicht
- Weitere Stabilitäts- und Fehlertests.
- Optionales `CHANGELOG`-Anpassungsformat.
