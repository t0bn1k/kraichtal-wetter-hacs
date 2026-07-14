# Kraichtal Wetter API

Diese Custom Integration verbindet Home Assistant mit der Kraichtal Wetter API. Sie liefert aktuelle Wetterdaten, Forecasts und stellt die Werte als Sensoren und `weather`-Entity bereit.

## Installation

1. Kopiere den Ordner `custom_components/kraichtal_wetter_api` in dein Home Assistant `custom_components`-Verzeichnis.
2. Starte Home Assistant neu.
3. Öffne `Einstellungen → Geräte & Dienste → Integration hinzufügen`.
4. Suche nach `Kraichtal Wetter API`.
5. Gib die `API-URL` ein und optional den `API-Key`.

## Konfiguration

```yaml
kraichtal_wetter_api:
  api_url: !secret weather_api_url
  key: !secret weather_api_key
  scan_interval: 300
```

### Secrets

```yaml
weather_api_key: DEIN_API_KEY_HIER
weather_api_url: https://api.example.com/weather
```

## Unterstützte Entitäten

- `weather.kraichtal_wetter_forecast`
- `sensor.kraichtal_wetter_temp`
- `sensor.kraichtal_wetter_feels_like`
- `sensor.kraichtal_wetter_humidity`
- `sensor.kraichtal_wetter_pressure`
- `sensor.kraichtal_wetter_wind`
- `sensor.kraichtal_wetter_gust_max`
- `sensor.kraichtal_wetter_rain`
- `sensor.kraichtal_wetter_solar`

## Lovelace-Beispiele

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.kraichtal_wetter_forecast

  - type: entities
    title: Kraichtal Wetter
    entities:
      - sensor.kraichtal_wetter_temp
      - sensor.kraichtal_wetter_humidity
      - sensor.kraichtal_wetter_pressure
      - sensor.kraichtal_wetter_wind
      - sensor.kraichtal_wetter_rain

  - type: history-graph
    title: Temperatur & Luftfeuchte
    entities:
      - sensor.kraichtal_wetter_temp
      - sensor.kraichtal_wetter_humidity
    hours_to_show: 24
    refresh_interval: 300
```

## HACS Veröffentlichung

Dieses Repository ist als HACS Custom Repository aufgebaut. Die Integration muss im Root-Verzeichnis einen Ordner `custom_components/kraichtal_wetter_api` enthalten.

- `manifest.json` muss `config_flow` oder `integration_type` definieren.
- Das Repository braucht eine `README.md` und eine `LICENSE`.
- Verwende Tags für Releases, z. B. `v0.0.1`.
