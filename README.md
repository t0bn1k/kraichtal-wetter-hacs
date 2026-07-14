# kraichtal-wetter-hacs

## Ziel

Dieses Repository soll eine HACS-fähige Home Assistant Custom Integration für eine Wetterstation-JSON-API enthalten. Die Integration liest die Daten einer nahegelegenen Wetterstation aus, stellt sie als Sensoren und `weather`-Entität bereit und ermöglicht eine einfache Visualisierung auf einem Lovelace-Dashboard.

## Warum Home Assistant + HACS?

- **Home Assistant**: zentrale Plattform für Sensoren, Automationen und Dashboards.
- **HACS**: ermöglicht einfache Installation und Updates von Custom Integrations.
- **Custom Integration**: besser als direkte `rest`-Sensoren bei komplexen APIs, Forecast-Prognosen und UI-Setup.

## Struktur der Integration

Das finale Repository sollte folgenden Aufbau haben:

- `custom_components/kraichtal_wetter_api/manifest.json`
- `custom_components/kraichtal_wetter_api/__init__.py`
- `custom_components/kraichtal_wetter_api/coordinator.py`
- `custom_components/kraichtal_wetter_api/sensor.py`
- `custom_components/kraichtal_wetter_api/weather.py`
- `custom_components/kraichtal_wetter_api/const.py`
- `custom_components/kraichtal_wetter_api/strings.json` (optional für Übersetzungen)
- `custom_components/kraichtal_wetter_api/README.md`

## 1. API-Daten importieren

1. Prüfe die JSON-Antwort der Wetterstation-API.
2. Identifiziere zentrale Felder wie Temperatur, Luftfeuchte, Luftdruck, Wind, Regen und Forecast.
3. Erstelle in der Integration ein `DataUpdateCoordinator`, das regelmäßig die REST-API abfragt.

Empfehlung:

- `scan_interval`: standardmäßig 300 Sekunden (5 Minuten)
- `timeout`: 10 Sekunden
- Fehlerbehandlung: bei 401/403 `AuthenticationFailed`, bei Zeitüberschreitung `UpdateFailed`

## 2. Custom Integration in Home Assistant

### Manifest

`manifest.json` sollte mindestens enthalten:

```json
{
  "domain": "wetterstation_api",
  "name": "Wetterstation API",
  "version": "0.0.1",
  "documentation": "https://github.com/<dein-user>/kraichtal-wetter-hacs",
  "requirements": [],
  "dependencies": [],
  "codeowners": ["@dein-github-user"],
  "config_flow": true,
  "iot_class": "local_polling"
}
```

### Konfiguration

Konfiguration per `configuration.yaml` oder später per UI-Flow:

```yaml
kraichtal_wetter_api:
  api_url: !secret weather_api_url
  api_key: !secret weather_api_key
  scan_interval: 300
```

### Secrets

`secrets.yaml`:

```yaml
weather_api_key: DEIN_API_KEY_HIER
weather_api_url: https://api.example.com/weather
```

## 3. Sensoren und Weather-Plattform

- `sensor.py`: erzeugt feste Sensor-Entitäten wie `sensor.kraichtal_wetter_temp`, `sensor.kraichtal_wetter_humidity`, `sensor.kraichtal_wetter_pressure`.
- `weather.py`: definiert eine `weather.kraichtal_wetter_forecast`-Entität mit aktuellem Zustand und Vorhersage.

Wichtige Sensoren:

- Temperatur
- Luftfeuchtigkeit
- Luftdruck
- Windgeschwindigkeit / Windrichtung
- Regenmenge
- UV-Index (falls verfügbar)

## 4. Dashboard-Visualisierung

### Empfohlene Lovelace-Karten

1. `Entities`-Card für wichtige aktuelle Werte
2. `Weather Forecast`-Card für `weather.wetterstation_forecast`
3. `History Graph` oder `Sensor`-Graph für Temperaturverlauf
4. `Gauge`-Card für Luftfeuchte oder Luftdruck

Beispiel-Lovelace:

```yaml
type: vertical-stack
cards:
  - type: weather-forecast
    entity: weather.kraichtal_wetter_forecast

  - type: entities
    title: Kraichtal Wetter
    entities:
      - sensor.station_temperature
      - sensor.station_humidity
      - sensor.station_pressure
      - sensor.station_wind_speed
      - sensor.station_rain

  - type: history-graph
    entities:
      - sensor.station_temperature
      - sensor.station_humidity
    title: Temperatur & Luftfeuchte
    hours_to_show: 24
    refresh_interval: 300
```

### Dashboard-Tipps

- Zeige die wichtigsten Werte oben an, damit sie sofort sichtbar sind.
- Kombiniere `weather`-Card mit zugehörigen Sensoren für Details.
- Verwende `conditional`-Cards, um nur bei Regen oder Sturm zusätzliche Informationen anzuzeigen.
- Nutze `layout-card` oder `grid`-Card für ein modernes, kompaktes Layout.

## 5. Alternative: native REST-Integration

Wenn du keine Custom Integration bauen möchtest, kannst du die API auch mit `rest`-Sensoren integrieren:

```yaml
sensor:
  - platform: rest
    name: Wetterstation Raw
    resource: !secret weather_api_url
    headers:
      Authorization: "Bearer !secret weather_api_key"
    value_template: "{{ value_json.current.temp }}"
    json_attributes:
      - current
      - days
      - hours
      - today
      - alerts
      - rain
    scan_interval: 300
    verify_ssl: true
```

Diese Variante ist sinnvoll für einen schnellen Proof-of-Concept, aber weniger flexibel als eine Custom Integration.

## 6. HACS-Veröffentlichung

Damit das Repo in HACS funktioniert, muss es eine Custom Integration enthalten und folgende Kriterien erfüllen:

- `custom_components/wetterstation_api` im Repo-Root
- `manifest.json` mit `config_flow` oder `integration_type`
- aussagekräftige `README.md`
- Lizenzdatei (`LICENSE`) und ggf. `CHANGELOG.md`

### Schritte

1. Repo initialisieren:

```bash
git init
git checkout -b main
```

2. Dateien hinzufügen und committen:

```bash
git add .
git commit -m "Initial HACS-ready integration"
```

3. Repository bei GitHub veröffentlichen und ggf. als HACS custom repository registrieren.

4. Release-Tag setzen:

```bash
git tag -a v0.0.1 -m "Initial release"
git push --tags
```

## 7. Praktische Tipps

- Implementiere `config_flow`, damit Nutzer die Integration im Home Assistant UI einrichten können.
- Arbeite mit `DataUpdateCoordinator`, um Abfragen zu bündeln und Fehler sauber zu behandeln.
- Füge `availability`-Logik hinzu: `unavailable`, wenn die API nicht erreichbar ist.
- Teste mit verschiedenen API-Antworten: volle Daten, unvollständige Daten, Fehler.
- Dokumentiere Feld-Belegungen und unterstützte Einheiten in `README.md`.

## Release-Strategie

Siehe `RELEASE_STRATEGY.md` für den empfohlenen Prozess zu Git-Tags, HACS-Releases und Versionsnummerierung.

## Verweis auf den Plan

Die `plan.md` wurde aus dem Repository entfernt, damit das Repo sauber für Tests und HACS-Veröffentlichung bleibt. Falls du sie benötigst, liegt sie nun auf dem Desktop als `plan.md`.
