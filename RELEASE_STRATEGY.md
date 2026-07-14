# Release-Strategie für Kraichtal Wetter API

## Ziel

Diese Release-Strategie stellt sicher, dass die Integration sauber über HACS verteilt werden kann und dass Versionsnummern, Tags und Releases nachvollziehbar bleiben.

## Versionsschema

Verwende semantisches Versionieren (SemVer):

- `vMAJOR.MINOR.PATCH`
- `MAJOR` bei inkompatiblen Änderungen
- `MINOR` bei neuen, abwärtskompatiblen Features
- `PATCH` bei Fehlerbehebungen und kleinen Verbesserungen

Beispiel:

- `v0.0.1` — initialer Entwicklungsstart
- `v0.1.0` — neue Feature-Integration oder zusätzliche Entity
- `v0.1.1` — Fehlerbehebung oder kleinere Verbesserung

## HACS-spezifische Anforderungen

- HACS ermittelt die Version über Git-Tags.
- Ohne Tag kann HACS Commit-Hashes wie `a98917c` nicht als stabile Version verwenden.
- Erstelle für jeden Release einen Tag und pushe ihn zum Remote-Repo.

## Release-Prozess

1. Sicherstellen, dass der Code getestet und gerätebereit ist.
2. `manifest.json` prüfen und ggf. die `version` aktualisieren.
3. Lokale Git-Änderungen committen.
4. Release-Tag erstellen:

```bash
git tag -a v0.0.1 -m "Kraichtal Wetter API v0.0.1"
git push origin v0.0.1
```

5. Optional: GitHub Release mit Beschreibung anlegen.
6. In HACS die Release-Liste aktualisieren und die neue Version installieren.

## Release-Checkliste

- [ ] `custom_components/kraichtal_wetter_api` im Repo-Root
- [ ] `manifest.json` korrekt und `config_flow: true`
- [ ] `README.md` auf aktuelles Release ausgerichtet
- [ ] `LICENSE` vorhanden
- [ ] Git-Tag erstellt und gepusht
- [ ] Tests erfolgreich ausgeführt
- [ ] HACS-Installation geprüft

## Branch-Strategie

Für dieses einzelne Integration-Repo reicht eine einfache Struktur:

- `main` für den stabilen Produktionscode
- optional `develop` für laufende Entwicklung

Wenn nur ein Branch genutzt wird, solltest du vor jedem Release einen sauberen Commit auf `main` haben.

## Hinweise zur `manifest.json`

Die `version` in `manifest.json` sollte mit dem Release-Tag übereinstimmen, damit die Integration intern konsistent bleibt:

```json
{
  "domain": "kraichtal_wetter_api",
  "name": "Kraichtal Wetter API",
  "version": "0.0.1",
  "config_flow": true,
  "iot_class": "local_polling"
}
```

## Wartung nach dem Release

- Dokumentiere sichtbare Änderungen in einem `CHANGELOG.md` oder in GitHub Release Notes.
- Erstelle nach jedem Bugfix oder Feature-Update einen neuen Patch- oder Minor-Tag.
- Teste vor dem Tagging die `config_flow` und die wichtigsten Sensor-/Weather-Entitäten.
