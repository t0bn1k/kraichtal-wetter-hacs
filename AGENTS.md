# Kraichtal Wetter — HACS Custom Component

## Repo-Übersicht

Home-Assistant-Custom-Integration für die Kraichtal-Wetter-API. Kein Build-System, keine Tests, keine Linter.

## Domain & Manifest

- Domain: `kraichtal_wetter` · HA-Minimum: `2026.3` · `iot_class: cloud_polling`
- Plattformen: `sensor`, `weather`
- Keine externen Abhängigkeiten (`requirements: []`)

## Wichtige Konventionen

- **API-Key-Feldname**: `key` (nicht `api_key`). Rückwärtskompatibel: `__init__.py:23-25` akzeptiert auch `api_key` / `apikey` aus alten Installationen.
- **API-URL** ist in `const.py:9` hardcodiert — Nutzer geben nur den Key an.
- **Sensoren** nutzen Dot-Notation in `sensor.py` um verschachtelte API-Felder aufzulösen (z.B. `station_today.tmax` → `data["current"]["station_today"]["tmax"]`).
- **Forecast-Datum** wird aus `meta.generated` + Tages-Index berechnet (API liefert kein `date` pro Tag). `weather.py:82-122`.
- **Forecast-Caching**: `async_forecast_daily()` cached bis `async_update()` invalidiert.
- **ICON_MAP** in `weather.py` übersetzt API-Icon-Namen in HA-Wetterbedingungen.
- **Beim ersten Refresh** wird `ConfigEntryNotReady` geworfen → HA wiederholt automatisch.
- **Default `scan_interval`**: 300 s (konfigurierbar via Options-Flow)
- **Reauth-Flow** vorhanden (API-Key via UI aktualisierbar).
- **hass.data**: `hass.data[DOMAIN][entry.entry_id]` speichert `{"coordinator", "client", "entry"}`.
- **UI-Sprache**: Deutsch (`strings.json`, Sensor-Namen)

## CI / Release

Einzige Pipeline: `.github/workflows/release.yml` — Tag `v*.*.*` erzeugt GitHub Release mit automatisch extrahiertem Changelog-Eintrag.

## Verzeichnisstruktur

```
custom_components/kraichtal_wetter/
├── __init__.py          # async_setup_entry, Coordinator-Init
├── config_flow.py       # Config-Flow, Reauth, Options
├── const.py             # DOMAIN, Konstanten
├── coordinator.py       # KraichtalWetterClient (HTTP)
├── sensor.py            # 22 Sensoren
├── weather.py           # WeatherEntity + Forecast
├── strings.json         # Deutsche UI-Texte
└── brand/               # 8 Brand-Bilder (icon/logo + @2x + dark_*), lokale Auslieferung seit HA 2026.3
hacs.json                # HACS-Metadaten
lovelace/                # Beispiel-Dashboards
scripts/generate_logo.py # Entwickler-Werkzeug
```

## Stil (im Code)

- `from __future__ import annotations`
- `voluptuous` + `cv` für Schemata
- `urllib.parse` für URL-Bau (kein String-Concatenation)
- `CoordinatorEntity` + `SensorEntityDescription`-Pattern
