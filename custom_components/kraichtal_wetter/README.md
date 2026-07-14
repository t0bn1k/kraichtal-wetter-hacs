# Kraichtal Wetter

Kraichtal Wetter verbindet Home Assistant mit der Kraichtal Wetter API und stellt die Daten als Sensoren sowie als `weather`-Entity bereit.

## Installation

1. Kopiere den Ordner `custom_components/kraichtal_wetter` in dein Home Assistant `custom_components`-Verzeichnis.
2. Starte Home Assistant neu.
3. Öffne `Einstellungen → Geräte & Dienste → Integration hinzufügen`.
4. Suche nach `Kraichtal Wetter`.
5. Gib den API-Key ein. Die API-URL ist in der Integration fest hinterlegt.

## Konfiguration

Diese Integration verwendet eine UI-basierte Einrichtung. Optional kannst du die Werte auch in `configuration.yaml` eintragen:

```yaml
kraichtal_wetter:
  key: !secret weather_api_key
  scan_interval: 300
```

In `secrets.yaml`:

```yaml
weather_api_key: DEIN_API_KEY_HIER
```

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

## Hinweis

Die Integration erscheint in Home Assistant als `Kraichtal Wetter`. Alle Entitäten werden unter einem Gerät in der Integrationen-Übersicht gruppiert.
