# Changelog

Alle signifikanten Änderungen an dieser Integration werden hier festgehalten.

## [0.2.1] - 2026-07-14
### Geändert
- Rebranding finalisiert
- Release ready

## [0.2.0] - 2026-07-14
### Geändert
- Integration umbenannt und als `Kraichtal Wetter` angezeigt.
- Alle `kraichtal_wetter`-Entitäten werden nun als ein Gerät in der Integrationen-Übersicht gruppiert.
- Erweiterung der Sensorabdeckung um zusätzliche API-Felder wie `dewpoint`, `wind_dir`, `tmax_today`, `tmin_today`, `rain_today`, `warnings`, `obs_date`, `obs_time`, `realtime` und `station_today.*`.
- Fix: Nested current-Felder über `station_today.*` korrekt aufgelöst.

## [0.0.2] - 2026-07-14
### Geändert
- Konfigurationsfeld von `api_key` zu `key` umgestellt (abwärtskompatibel).
- Korrekte Anhängung des API-Parameters `key=` an die URL.
- Integration-Icon als `logo.png` hinzugefügt.

## [0.0.1] - 2026-07-14
### Hinzugefügt
- Erste Version der Home Assistant Custom Integration für die Kraichtal Wetter API.
- Unterstützung einer `config_flow`-basierten Einrichtung.
- Erste Sensor-Entitäten und `weather.kraichtal_wetter_forecast`.

