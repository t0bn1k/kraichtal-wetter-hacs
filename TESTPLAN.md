# Testplan für Kraichtal Wetter API

## Ziel

Der Testplan stellt sicher, dass die Custom Integration `kraichtal_wetter_api` in Home Assistant funktioniert, über HACS installiert werden kann und die erwarteten Sensor- und Weather-Entitäten liefert.

## 1. Vorbereitung

1. Prüfe die Repository-Struktur:
   - `custom_components/kraichtal_wetter_api/manifest.json`
   - `custom_components/kraichtal_wetter_api/__init__.py`
   - `custom_components/kraichtal_wetter_api/config_flow.py`
   - `custom_components/kraichtal_wetter_api/coordinator.py`
   - `custom_components/kraichtal_wetter_api/sensor.py`
   - `custom_components/kraichtal_wetter_api/weather.py`
   - `custom_components/kraichtal_wetter_api/const.py`
   - `custom_components/kraichtal_wetter_api/strings.json`
   - `custom_components/kraichtal_wetter_api/README.md`
2. Stelle sicher, dass `README.md` und `LICENSE` vorhanden sind.
3. Bereite eine lokale Home Assistant Entwicklungsumgebung vor (z. B. Home Assistant Container oder Core).
4. Lege eine Test-URL fest, die die API-Daten liefert. Falls kein echtes Backend verfügbar ist, nutze einen Mock-Server oder eine lokale JSON-Datei.

## 2. Installationsprüfung

### 2.1 Manuelle Installation in Home Assistant

1. Kopiere `custom_components/kraichtal_wetter_api` in das Home Assistant `custom_components`-Verzeichnis.
2. Starte Home Assistant neu.
3. Öffne `Einstellungen → Geräte & Dienste → Integration hinzufügen`.
4. Suche nach `Kraichtal Wetter API`.
5. Führe den UI-Setup-Flow aus und gib die Test-URL sowie optional den API-Key ein.
6. Prüfe, ob die Integration erfolgreich eingerichtet wird.

### 2.2 HACS-Installation (optional)

1. Erstelle eine temporäre HACS-Installation und registriere das lokale Repo als Custom Repository, falls möglich.
2. Installiere die Integration über HACS.
3. Starte Home Assistant neu.
4. Prüfe erneut die Einrichtung und Funktionalität.

## 3. Funktionale Tests

### 3.1 API-Abruf und Coordinator

1. Kontrolliere, dass beim Setup ein `DataUpdateCoordinator` eingerichtet wird.
2. Prüfe die ersten API-Abfrageergebnisse:
   - `ok`-Feld in der API-Antwort
   - `current`-Daten vorhanden
   - `days`-Forecast vorhanden
3. Teste fehlerhafte Antworten:
   - ungültige URL / 404
   - HTTP 401/403
   - ungültiges JSON
   - `ok: false`
4. Verifiziere, dass die Integration bei fehlgeschlagenem Update nicht abstürzt und dass die Entitäten auf `unavailable` gehen.

### 3.2 Sensor-Entitäten

Prüfe die folgenden Entitäten in `Developer Tools → States`:

- `sensor.kraichtal_wetter_temp`
- `sensor.kraichtal_wetter_feels_like`
- `sensor.kraichtal_wetter_humidity`
- `sensor.kraichtal_wetter_pressure`
- `sensor.kraichtal_wetter_wind`
- `sensor.kraichtal_wetter_gust_max`
- `sensor.kraichtal_wetter_rain`
- `sensor.kraichtal_wetter_solar`

Für jede Entität:
- Wert ist nicht `unknown` oder `unavailable`
- Einheit passt zur Entität
- Name und einzigartige ID sind korrekt

### 3.3 Weather-Entität

Prüfe:

- `weather.kraichtal_wetter_forecast` existiert
- aktueller Zustand ist plausibel (z. B. `partlycloudy`, `sunny`)
- Forecast-Daten erscheinen in der Entität

## 4. UI-Dashboard-Tests

### 4.1 Lovelace-Validierung

1. Erstelle eine Lovelace-Seite mit folgenden Karten:
   - `weather-forecast` für `weather.kraichtal_wetter_forecast`
   - `entities`-Card mit den wichtigsten Sensoren
   - `history-graph` für Temperatur und Feuchte
2. Prüfe, dass die Karten ohne Fehler geladen werden.
3. Verifiziere, dass die Werte korrekt dargestellt werden.

### 4.2 Bedienbarkeit

- Stelle sicher, dass die Integration im UI als `Kraichtal Wetter API` erscheint.
- Prüfe, ob das Setup klar beschriftet und verständlich ist.

## 5. Grenzfälle und Fehlerfälle

1. API-Key fehlt, aber die URL enthält einen Key.
2. API-Key ist im Config Flow angegeben, aber die URL enthält keinen Key.
3. `scan_interval` ist sehr niedrig (z. B. 30 s) und sehr hoch (z. B. 3600 s).
4. API-Antwort ohne Forecastdaten (`days` leer) – Integration darf nicht abstürzen.
5. Teilweise fehlende Felder in `current`.

## 6. Release- und HACS-Checkliste

1. `manifest.json` gültig und vollständig.
2. `CODEOWNERS` und `license` vorhanden.
3. `custom_components/kraichtal_wetter_api` im Repo-Root.
4. `README.md` enthält Installationsanweisungen und HACS-Hinweise.
5. Repository funktioniert mit HACS als Custom Repository.

## 7. Optional: Automatisierte Tests

1. Schreibe Unit-Tests für den Coordinator und die `async_get_data`-Logik.
2. Simuliere API-Antworten mit `aiohttp`-Mocks.
3. Füge bei Bedarf GitHub Actions hinzu für:
   - Linting
   - Python-Tests
   - Formatierung

## Ergebnis

Nach Abschluss dieses Testplans solltest du sicher sein, dass die Integration:

- in einer Home Assistant-Umgebung funktioniert,
- über den UI-Flow eingerichtet werden kann,
- sinnvolle Sensoren und Forecast-Daten liefert,
- für HACS sauber strukturiert ist.
