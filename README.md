# Kraichtal Wetter

Kraichtal Wetter ist eine Home Assistant Custom Integration, die aktuelle Wetterdaten aus der Kraichtal Wetter API als Sensoren und als `weather`-Entität bereitstellt.

## Installation

### Manuelle Installation

1. Kopiere den Ordner `custom_components/kraichtal_wetter` in dein Home Assistant `custom_components`-Verzeichnis.
2. Starte Home Assistant neu.
3. Öffne `Einstellungen → Geräte & Dienste → Integration hinzufügen`.
4. Suche nach `Kraichtal Wetter`.
5. Folge dem UI-Setup und gib deinen API-Key ein.

### Optional: Konfiguration in YAML

Die Integration ist primär für die UI-Konfiguration ausgelegt. Optional kannst du folgende Einstellungen in `configuration.yaml` hinterlegen:

```yaml
kraichtal_wetter:
  key: !secret weather_api_key
  scan_interval: 300
```

In `secrets.yaml`:

```yaml
weather_api_key: DEIN_API_KEY_HIER
```

## Was bietet Kraichtal Wetter?

- Aktuelle Wetterdaten aus der Kraichtal Wetter API
- Forecast über `weather.kraichtal_wetter_forecast`
- Erweiterte Sensoren aus `station_today`
- Gruppierte Entitäten unter einem Gerät in der Integrationen-Ansicht

## Unterstützte Entitäten

- `weather.kraichtal_wetter_forecast`
- `sensor.kraichtal_wetter_temp`
- `sensor.kraichtal_wetter_feels_like`
- `sensor.kraichtal_wetter_dewpoint`
- `sensor.kraichtal_wetter_humidity`
- `sensor.kraichtal_wetter_pressure`
- `sensor.kraichtal_wetter_wind`
- `sensor.kraichtal_wetter_wind_dir`
- `sensor.kraichtal_wetter_gust_max`
- `sensor.kraichtal_wetter_solar`
- `sensor.kraichtal_wetter_rain`
- `sensor.kraichtal_wetter_tmax_today`
- `sensor.kraichtal_wetter_tmin_today`
- `sensor.kraichtal_wetter_rain_today`
- `sensor.kraichtal_wetter_warnings`
- `sensor.kraichtal_wetter_obs_date`
- `sensor.kraichtal_wetter_obs_time`
- `sensor.kraichtal_wetter_realtime`
- `sensor.kraichtal_wetter_station_today_tmax`
- `sensor.kraichtal_wetter_station_today_tmin`
- `sensor.kraichtal_wetter_station_today_gust`
- `sensor.kraichtal_wetter_station_today_press_max`
- `sensor.kraichtal_wetter_station_today_press_min`

## Lovelace Beispiele

### Übersicht

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.kraichtal_wetter_forecast

  - type: entities
    title: Kraichtal Wetter – Aktuelle Werte
    show_header_toggle: false
    entities:
      - sensor.kraichtal_wetter_temp
      - sensor.kraichtal_wetter_feels_like
      - sensor.kraichtal_wetter_humidity
      - sensor.kraichtal_wetter_pressure
      - sensor.kraichtal_wetter_wind
      - sensor.kraichtal_wetter_rain

  - type: entities
    title: Kraichtal Wetter – Tageswerte
    show_header_toggle: false
    entities:
      - sensor.kraichtal_wetter_tmax_today
      - sensor.kraichtal_wetter_tmin_today
      - sensor.kraichtal_wetter_rain_today
      - sensor.kraichtal_wetter_warnings
      - sensor.kraichtal_wetter_realtime
```
```

### Verlauf

```yaml
type: history-graph
title: Verlauf Temperatur & Luftfeuchte
entities:
  - sensor.kraichtal_wetter_temp
  - sensor.kraichtal_wetter_humidity
hours_to_show: 24
refresh_interval: 300
```

## Hinweise

- Die Integration erscheint in Home Assistant als `Kraichtal Wetter`.
- Nutzer geben nur einen API-Key ein; die API-URL ist fest in der Integration hinterlegt.
- Alle Entitäten werden als Teil desselben Geräts in der Integrationen-Ansicht angezeigt.

## Repository

Dieses Repository enthält die Custom Integration unter `custom_components/kraichtal_wetter` sowie die Dokumentation und das Changelog für die Integration.
