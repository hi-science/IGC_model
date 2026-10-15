# Weiterentwickeln, versionieren, Ergebnisse liefern

Vorschlag von HiScience (IGC.NRW), Stand 2026-10-15. Gilt für alle Module dieses Repos. Ziel:
Jede Zahl in der IGC.NRW-App lässt sich auf einen Code-Stand, einen Datenstand und eine
Beschreibung zurückführen, und RUB kann ohne HiScience weiterentwickeln und neue Ergebnisse
liefern.

## 1. Begriffe

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Release** | ein geprüfter Code-Stand eines Moduls, als Git-Tag (§3) | dieses Repo |
| **Datenstand** | versionierte Eingaben, z. B. `co2-point-sources/v0.1.0-2026-05-12` | Sciebo `04_processed_data/<partner>/<tool>/<version>/` |
| **Set** | ein Datenstand plus Parameter (Szenario, Solver-Optionen), mit eigener ID | Runner-Config |
| **Ergebnis-Paket** | Paketversion × Set: Inputs, Outputs **und Doku des Release** | Sciebo `06_outputs/<partner>/results/<modell>/<version>/<set>/` |

Die **Paketversion** vergibt, wer veröffentlicht. Beim CO₂-Netzwerk heißt sie bei HiScience
`tools-N`; HiScience erhöht sie mit jedem übernommenen Release, Tag bzw. Commit stehen im
Paket (`_manifest.json`, Lauf-Parameter `rub_commit`). Ein Paket wird nie überschrieben:
neuer Code ergibt eine neue Paketversion, neue Eingaben oder Parameter ein neues Set.

## 2. Arbeiten mit Git

- `main` ist immer lauffähig und geprüft. Gearbeitet wird in kurzlebigen Branches
  (`feature/<thema>`, `fix/<thema>`), zusammengeführt per Pull Request mit Review durch eine
  zweite Person. Langlebige persönliche Branches (heute `roman`) bitte nach `main` überführen;
  die Module liegen nebeneinander, ein gemeinsamer `main` vermeidet doppelte Pflege.
- Ein Commit ist eine logische Änderung. Betreff kurz und im Imperativ, im Text das Warum.
  Ändert ein Commit Ergebnisse, steht das im Betreff oder in der ersten Zeile des Textes.
- **Keine Daten und Ergebnisse in Git:** `Results/`, `*.nc`, `*.pkl`, große Eingaben stehen in
  `.gitignore`. Eingaben kommen aus versionierten Datenpaketen; der Ordner kommt aus der
  Umgebung (z. B. `CO2_NETWORK_DATA_ROOT`), nicht fest aus dem Code.
- Abhängigkeiten mit Versionen festhalten (`environment.yml` oder `requirements.txt`, besser
  eine Lock-Datei). Solver und Version gehören in die Ergebnisse.
- Fehlt noch: `LICENSE` (Voraussetzung für Weitergabe und Übernahme in die App) und
  `CITATION.cff` (zitierfähige Versionen).

## 3. Versionen und Releases

Versionen nach [Semantic Versioning](https://semver.org/lang/de/), je Modul als annotierter
Tag auf `main` mit diesem Präfix:

| Verzeichnis | Tag | erster Tag |
|---|---|---|
| `co2_network_module` | `co2-network-vX.Y.Z` | `co2-network-v1.0.0` |
| `network_module` | `network-vX.Y.Z` | `network-v1.0.0` |
| `econ_module` (Trading) | `econ-vX.Y.Z` | `econ-v1.0.0` |
| `plant_design_module` | `plant-design-vX.Y.Z` | `plant-design-v1.0.0` |

```bash
git tag -a co2-network-v1.0.0 -m "CO₂-Netzwerk 1.0.0"
git push origin co2-network-v1.0.0      # nur diesen Tag, nicht alle lokalen
```

| Teil | Wann erhöhen |
|---|---|
| MAJOR | Eingabe- oder Ausgabeformat ändert sich inkompatibel (Spalten, Einheiten, Dateien) |
| MINOR | neue Funktion oder methodische Änderung, Formate bleiben kompatibel |
| PATCH | Fehlerkorrektur |

Jede neue Version, auch ein PATCH, ergibt in der App neue Ergebnis-Pakete; nichts wird
automatisch übernommen. Ändert ein Release Ergebnisse, sagt das eine Überschrift im
`CHANGELOG.md` (z. B. `### Behoben – ändert Ergebnisse`). Ein Release besteht aus: Tag,
Abschnitt im `CHANGELOG.md` des Moduls und aktualisierter `docs/MODEL.md`.

Veröffentlicht werden nur getaggte Stände. **Übergang:** Bis zum ersten Tag rechnet und
veröffentlicht HiScience mit Commit-Ständen (heute `c0a36e1`); der Commit steht im Paket.

## 4. Doku pflegen

Die Doku gehört zum Code und wird im selben Pull Request geändert („docs as code“). Je Modul:

| Datei | Inhalt |
|---|---|
| `<verzeichnis>/docs/MODEL.md` | Modellbeschreibung: Zweck, Methode (Gleichungen in LaTeX, `$…$`/`$$…$$`), Eingaben mit Quelle und Einheit, Ausgaben mit Spalten und Einheit, Parameter, Annahmen und Grenzen. Kopf mit `title`, `updated`, `upstream` (Repo und Tag) |
| `<verzeichnis>/CHANGELOG.md` | Änderungen je Version nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), oben `## [Unreleased]` |

Vorlage für eine neue `MODEL.md`: `docs/MODEL-vorlage.md`.

Die IGC.NRW-App zeigt zu jedem Ergebnis-Set die Modellbeschreibung der Version, mit der es
gerechnet wurde; wählt man ein anderes Set, wechseln Beschreibung, Übersicht und Analysen
mit. Beim CO₂-Netzwerk ist das die `co2_network_module/docs/MODEL.md` des übernommenen
Stands: Sie kommt beim Rechnen als `docs/model.md` ins Paket.

## 5. Neue Ergebnisse in die App bringen

**Vorher lokal prüfen:** Mit dem App-Repo lässt sich ein eigener Stand des CO₂-Netzwerks lokal
rechnen (README des App-Repos, „Als Partner lokal rechnen“): im Submodul den Branch oder Tag
auschecken (`git -C models/rub_co2_network/upstream checkout co2-network-v1.0.0`), eine Kopie
der Config mit **neuer Set-ID** anlegen und `make run-co2 CONFIG=<kopie>` rechnen. Ein neuer
Stand braucht eine neue Set-ID, weil die lokale Paketversion `tools-N` gleich bleibt;
`FORCE=1` braucht es nur, um einen schon gerechneten Stand nachzurechnen. Die Pakete bleiben
lokal unter `data/06_outputs/` (Übersicht: `make results-list`, Kennzahlen in
`outputs/kpis.parquet`).

**Weg A – HiScience übernimmt ein Release (CO₂-Netzwerk):**

1. Release taggen (§3) und HiScience Tag und gewünschte Sets nennen.
2. HiScience hebt den Submodul-Stand in der App per Merge Request (mit Review) und erhöht die
   Paketversion, rechnet und legt die Pakete unter
   `06_outputs/hiscience/results/rub-co2-network/tools-N/<set>/` ab, mit der `MODEL.md` des
   Tags im Paket.
3. Nach Abstimmung gibt HiScience die Sets im Register frei (`_register.json`).

Transport-Routing und Trading rechnet die App heute mit HiScience-Nachbauten
(Transport: eigene Implementierung des Algorithmus, Trading: `igc-model`). Änderungen an
`network_module` bzw. `econ_module` übernimmt HiScience dort nach Absprache; ein Tag allein
ändert diese Ergebnisse nicht.

**Weg B – RUB veröffentlicht selbst (für eigene, neue Modelle mit eigener Modell-ID):**

1. Pakete mit der eigenen Rechenkette erzeugen und unter
   **`06_outputs/rub/results/<modell>/<version>/<set>/`** ablegen, nie unter `hiscience/`.
   Format: `docs/results-package-format.md` im App-Repo (`datapackage.json`, `outputs/`,
   `docs/model.md` = `MODEL.md` des Tags, optional `docs/analysis.md` mit der Einordnung des
   Sets und `docs/view.yaml` für Übersicht und Analysen). Hier ist die Paketversion der Tag.
2. Erst als `<set>.partial` hochladen, dann umbenennen. Prüfen mit `igc-tools results check`.
3. Freigeben im eigenen Register `06_outputs/rub/results/<modell>/_register.json`
   (`"visible": true`); die erste Lieferung und die Darstellung mit HiScience abstimmen.

Eine Modell-ID gehört genau einem Partner. Soll RUB auch die integrierten Modelle selbst
veröffentlichen, stimmen wir den Wechsel ab (die bisherigen Pakete bleiben unter `hiscience/`).

Auf Sciebo gilt: Jede Institution schreibt nur in ihren eigenen Ordner (`rub/`) und liest die
Daten der anderen direkt aus deren Ordner. Spiegeln oder Kopieren fremder Ordner ist nicht
nötig, die Runner lesen eine Kopie nicht.

## 6. Cloud-Läufe

Rechnet jemand in der App mit eigener Eingabe („Eigene Eingabe“), läuft immer die Version, die
mit der App ausgerollt ist (Submodul-Stand bzw. Versionskonstante der App), mit den neuesten
veröffentlichten Datenständen. Unveröffentlichte Branches laufen nie in der Cloud. Ein neues
Release kommt nur über Weg A (Merge Request, Review, Deploy der App) in die Cloud; die Freigabe
von Sets im Register hat darauf keinen Einfluss.

## 7. Checkliste für einen Pull Request

- [ ] `docs/MODEL.md` passt zum Code, `CHANGELOG.md` unter `[Unreleased]` ergänzt
- [ ] Ändert Ergebnisse? Im PR genannt, mit Kennzahlen vorher/nachher aus einem Testlauf
- [ ] Keine Daten oder Ergebnisse eingecheckt, keine festen Pfade
- [ ] Eingaben aus versionierten Datenpaketen (Version im PR genannt)
- [ ] Review durch eine zweite Person
