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

## [0.0.2] - 2026-07-14
### Geändert
- Anpassung der Konfigurationsoption von `api_key` zu `key` (abwärtskompatibel)
- Fehlerbehebung: korrekte Anhängung des API-Parameters `key=` an die API-URL (vermeidet 401 Unauthorized)
- Integration-Icon als `logo.png` hinzugefügt (128×128) für HACS-/Integration-Anzeige
- Dokumentation und Beispiele in `README.md` und `plan.md` aktualisiert

## [0.1.7] - 2026-07-14
### Geändert
- Fix: Home Assistant konforme `homeassistant.const`-Importe geprüft und sichergestellt.
- Fix: Sicherer Release zur Installation der neuesten Version.

## [0.1.6] - 2026-07-14
### Geändert
- Fix: `DEFAULT_API_URL` importiert, damit die fest hinterlegte Kraichtal-API-URL als Fallback funktioniert.
- Fix: Beispiel-URL in `plan.md` auf `https://kraichtal-wetter.de/dashboard/api.php` aktualisiert.
- Fix: `async_forward_entry_setups` statt nicht existierender `async_forward_entry_setup` verwendet.
- Fix: remove deprecated `PRESSURE_HPA` import and use "hPa" units for pressure sensor.

## Unveröffentlicht
- Weitere Stabilitäts- und Fehlertests.
- Optionales `CHANGELOG`-Anpassungsformat.

## [0.1.0] - 2026-07-14
### Geändert
- Minor Release: Feste API-URL in der Integration hinterlegt; Nutzer geben nur noch den `key` ein.
- Beibehaltung der Abwärtskompatibilität für bestehende `api_key`/`apikey`-Einträge.
- Korrekte Anhängung des `key=` Parameters an die API-URL (vermeidet 401 Unauthorized).
- Icon: `logo.png` (128×128) hinzugefügt und in Integration bereitgestellt.
- Dokumentation (`README.md`, `plan.md`) aktualisiert.

