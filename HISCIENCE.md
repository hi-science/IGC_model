# Vorschlag von HiScience (IGC.NRW) für `main`

Stand 2026-10-14 · Ticket SR-539 (HiScience) · Ansprechpartner: HiScience, info@hiscience.de

HiScience betreibt die IGC.NRW-App und rechnet dort Varianten der RUB-Modelle. Dieser Branch
schlägt kleine Änderungen auf der Eingabe-/Ausgabe-Seite vor, damit RUB und HiScience
dieselben, versionierten Datenstände nutzen können. Jeder Commit ist einzeln übernehmbar.

## Commits

| Commit | Inhalt | Ändert Ergebnisse? |
|---|---|---|
| `.gitignore` in `plant_design_module/input` | Tippfehler `xlslx`: `technology_input.xlsx` wurde nie versioniert | nein (Datei bitte einchecken) |

## Trading

HiScience rechnet Trading mit einer modularen Neu-Implementierung (`igc-model`, Golden-Parität
zu `main@a33bb5c`). Eingaben sind die drei Excel-Dateien aus `econ_module/data/h2bb` und
`relationship_module/data/h2bb`, umgewandelt in sieben Parquet-Tabellen (`igc-model convert`).
Der Übergabe-Vorschlag dazu liegt bei HiScience vor und wird gesondert abgestimmt (offen:
Lizenz des Repos).

## Gemeinsame Datenpakete

Die IGC.NRW-Datenpipelines veröffentlichen versionierte GeoParquet-Pakete auf Sciebo unter
`04_processed_data/hiscience/<tool>/<version>/` bzw. `03_intermediate/hiscience/…`, je mit
`datapackage.json` und SHA-256:

| Paket | Inhalt | Ersetzt in RUB-Code |
|---|---|---|
| `co2-point-sources` | CO₂-Punktquellen DE 2021–2024 (IED und EU-ETS getrennt, nie addieren) | `emissions/*.gpkg`/`*.xlsx` (network_module), `emissions.xlsx` (CO₂-Netz, zusammen mit `co2-source-classes`) |
| `co2-source-classes` | NACE → Szenarioklasse und CCS-Kosten | Spalten `Scenario`, `CCS Cost` |
| `nuts-regions` | NUTS 0–3 für DE, NL, BE (GISCO-Spalten) | NUTS-gpkg-Dateien |
| `transport-network` | Straßen-/Wasserstraßengraph, auch vereinfacht wie `simplify_infrastructure.py` | `simple_grid_*.pkl` |
| `gas-grid-lkd`, `h2-backbone` | Gasnetz LKD-EU, EHB-Karte | `routing_template/*.gpkg` |

## Offene Fragen an RUB

- Lizenz des Repos (Voraussetzung für Übernahme und Weitergabe).
- `technology_input.xlsx` einchecken; Status der Validierung der Anlagenauslegung.
- `network_module`: Fallstudie wird doppelt zugewiesen (`igc_nrw` → `h2bb`), gewollt?
