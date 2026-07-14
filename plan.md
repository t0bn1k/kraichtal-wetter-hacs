# Exported Plan: Home Assistant Integration — Wetterstation API

Datum: 2026-07-14

Kurzbeschreibung
- Ziel: JSON-API einer Wetterstation als HACS-fähige Home Assistant Custom Integration bereitstellen, dokumentieren und in ein neues Repository verschieben.
- Ergebnis: Integrationscode (Coordinator, Sensor-, Weather-Plattform), YAML-Beispiele, Lovelace-Beispiele, Installations- und Release-Hinweise.

Erstellte Dateien (im aktuellen Repo)
- [custom_components/kraichtal_wetter_api/__init__.py](custom_components/kraichtal_wetter_api/__init__.py) — Setup, Coordinator-Initialisierung
- [custom_components/kraichtal_wetter_api/coordinator.py](custom_components/kraichtal_wetter_api/coordinator.py) — DataUpdateCoordinator für REST-Aufrufe
- [custom_components/kraichtal_wetter_api/sensor.py](custom_components/kraichtal_wetter_api/sensor.py) — Mapping der API-Felder auf `sensor.`-Entities
- [custom_components/kraichtal_wetter_api/weather.py](custom_components/kraichtal_wetter_api/weather.py) — `weather`-Entity + Forecast
- [custom_components/kraichtal_wetter_api/const.py](custom_components/kraichtal_wetter_api/const.py) — Konstanten
- [custom_components/kraichtal_wetter_api/manifest.json](custom_components/kraichtal_wetter_api/manifest.json) — Integration-Metadaten
- [custom_components/kraichtal_wetter_api/README.md](custom_components/kraichtal_wetter_api/README.md) — Install-Anleitung

Konfiguration (Beispiele)

1) `secrets.yaml`

```yaml
weather_api_key: DEIN_API_KEY_HIER
weather_api_url: https://kraichtal-wetter.de/dashboard/api.php
```

2) `configuration.yaml` (Integration)

```yaml
wetterstation_api:
  key: !secret weather_api_key
  scan_interval: 300
```

3) Alternative: direkte `rest`-Sensor-Beispiel (falls nicht die Custom Integration verwendet wird)

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

Lovelace Minimalbeispiele
- Entities-Card mit wichtigen Sensoren
- History-Graph für `sensor.station_temperature`
- Weather-Forecast-Card für `weather.wetterstation_forecast`

Testing / Verifikation
- Nach Installation: `Developer Tools → States` prüfen (Sensoren & Weather-Entity vorhanden)
- Logs prüfen bei Fehlern (Timeout, 401)
- Testfälle: falscher API-Key → Sensor `unavailable`; API offline → Coordinator-Fehler im Log

Schritt-für-Schritt zum Verschieben in ein neues Repository

1. Neues Repo initialisieren (lokal)

```bash
cd /path/to/your/projects
git init wetterstation_api
cd wetterstation_api
```

2. Kopiere die Integration-Dateien

```bash
cp -R /path/to/churchtools-suite/custom_components/wetterstation_api ./
```

3. Füge Standarddateien hinzu (README, LICENSE, .gitignore)

```bash
echo "# Wetterstation API" > README.md
echo "MIT" > LICENSE
cat > .gitignore <<'GIT'
__pycache__/
.DS_Store
GIT
```

4. Commit und Push

```bash
git add .
git commit -m "Initial HACS-ready integration"
git branch -M main
git remote add origin git@github.com:youruser/wetterstation_api.git
git push -u origin main
```

HACS-Veröffentlichung (Kurzinfo)
- Für HACS: Repository muss `custom_components/wetterstation_api` im Repo-Root enthalten oder als custom repository registriert werden.
- README sollte Install-Anleitung, Versionshinweise, CHANGELOG und Lizenz enthalten.
- Tag-Release anlegen (`git tag -a v0.0.1 -m "v0.0.1"` → `git push --tags`).

Empfohlene nächste Schritte (Priorität)
1. `config_flow` implementieren (UI-basiertes Setup) — erhöht Benutzerfreundlichkeit in HACS.
2. Unit-Tests + GitHub Actions (Lint, Tests) — Qualitätssicherung.
3. Erweiterte Fehlerbehandlung (Rate-Limit, Backoff) und Retries im Coordinator.
4. Optional: MQTT-Bridge / Node-RED-Flow als Alternative für Resilienz.

Kontakt & Hinweise
- Integration wurde generisch entwickelt; passe `api_url` und Feld-Mappings an, falls die API leicht anders strukturiert ist.
- Lizenzempfehlung: MIT oder Apache-2.0 für einfache Open-Source-Nutzung.
