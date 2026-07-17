# Changelog

Alle signifikanten Änderungen an dieser Integration werden hier festgehalten.

## [0.4.1] - 2026-07-17
### Hinzugefügt
- `hacs.json` im Repository-Root für korrekte HACS-Erkennung hinzugefügt.

### Entfernt
- Ungenutzte Bilddateien `logo.png` und `dark_logo.png` aus dem Integration-Root entfernt (nur `brand/` wird verwendet).
- Ungenutzte `logo.svg` aus dem Repository-Root entfernt.

## [0.4.0] - 2026-07-17
### Geändert
- Forecast-Implementierung auf `async_forecast_daily()` umgestellt (deprecated `forecast` Property entfernt).
- Forecast-Felder auf `native_`-Präfix umgestellt (`native_temperature`, `native_templow`, `native_wind_speed`).
- `native_temperature_unit` und `native_pressure` als Properties hinzugefügt.
- `wind_bearing` und `native_wind_speed` als separate Properties hinzugefügt.

### Behoben
- Forecast-Datum wird nun korrekt aus `meta.generated` + Tages-Index generiert (RFC 3339 UTC).
- API liefert kein `date`-Feld im `days`-Array – jetzt aus `meta.generated` berechnet.
- Forecast-Caching eingeführt; Cache wird bei Coordinator-Update invalidiert.

## [0.3.0] - 2026-07-17
### Geändert
- `iot_class` von `local_polling` zu `cloud_polling` korrigiert.
- Unnötigen `importlib`-basierten Platform-Import entfernt (`async_forward_entry_setups` übernimmt dies).
- Beim ersten Refresh wird nun `ConfigEntryNotReady` statt `UpdateFailed` geworfen, sodass HA den Setup-Vorgang automatisch erneut versucht.
- Custom Attributes auf dem `DataUpdateCoordinator` (`entry_id`, `api_url`) entfernt; `entry` wird stattdessen über `hass.data` weitergegeben.
- Redundantes `available`-Property in `KraichtalWetterSensor` entfernt (wird von `CoordinatorEntity` geerbt).
- Deprecated `CONNECTION_CLASS` im Config Flow entfernt.
- Unbenutzte Imports in `coordinator.py` bereinigt.
- URL-Key-Anhänge-Logik durch korrekte URL-Parsung via `urllib.parse` ersetzt.

### Hinzugefügt
- Reauth-Flow: API-Key kann über die UI aktualisiert werden, wenn der aktuelle nicht mehr funktioniert.
- Options Flow: Abfrageintervall (`scan_interval`) kann nach der Installation geändert werden.
- Null-Schutz in `weather.py` für `coordinator.data` und `current`.
- `native_wind_speed_unit_of_measurement` in der Weather-Entität gesetzt.
- Forecast verwendet `date`-Feld der API als `datetime` (funktionierte nicht korrekt, siehe 0.4.0).
- Eindeutige `unique_id` zur Vermeidung doppelter Konfigurationen.

### Entfernt
- Unnötiges `import_executor` aus `manifest.json` entfernt.

## [0.2.3] - 2026-07-14
### Geändert
- Icon hinzugefügt

## [0.2.2] - 2026-07-14
### Geändert
- Rebranding finalisiert
- Release ready

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

