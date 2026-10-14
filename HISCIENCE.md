# Vorschlag von HiScience (IGC.NRW) für `roman` (CO₂-Netzwerk)

Stand 2026-10-14 · Ticket SR-539 (HiScience) · Ansprechpartner: HiScience, info@hiscience.de

HiScience rechnet das CO₂-Netzwerk in der IGC.NRW-App mit diesem Code (Pin `c0a36e1`). Die
ersten Commits sind genau das, was HiScience heute als Patch anwendet, plus ein
GeoParquet-Leser. Die Commits zu `move_source` und zur Stahl-Flexibilität korrigieren Fehler
und können Ergebnisse ändern; sie sind einzeln zu prüfen.

## Commits

| Commit | Inhalt | Ändert Ergebnisse? |
|---|---|---|
| Pfade, Szenario-Set, `demand`, Solver per Umgebung | `CO2_NETWORK_DATA_ROOT`, `CO2_NETWORK_SCENARIO_SET`, `CO2_NETWORK_DEMAND` (gleich in `network.py` und `main.py`), `CO2_NETWORK_SOLVER(_OPTIONS)`, Default HiGHS | nein |
| GeoParquet lesen | `utils.load_geodataframe` erkennt `.parquet`; `utils.load_grid` liest den Graphen als Pickle oder GeoParquet (`CO2_NETWORK_GRID_STREET`/`_WATER`) | nein |
| `Results/` nicht versionieren | eingecheckte `.nc` konnten alte Stände maskieren; der Ordner bleibt über `.gitkeep` (die Skripte legen ihn nicht an); einmalig `git rm -r --cached 'co2_network_module/Results/*.nc' 'co2_network_module/Results/Old_nc'` | nein |
| `move_source` | Endpunkt ist `coords[-1]`, war `coords[0]` | möglich (Quellen und Senken auf einem Kantenende: ≤ 25 m außerhalb, ≤ 5 m innerhalb NRW); im Test ohne Wirkung |
| Stahl-Flexibilität | `'24.1' in name_i` war nie wahr (Namen nach Bündelung `Source-<i>`); jetzt über die NACE | ja, in Szenarien mit Stahl (S1) |

**Testläufe (HiGHS, Zeitlimit 600 s, 14.10.2026):** „Base only“ ergibt exakt die Kennzahlen
von `c0a36e1` mit den Overlay-Patches (46,33 Mt, 4.197 km, 69 Quellen, Gap 17,7 %). „Base and
S1“ ändert sich durch die Stahl-Flexibilität: 78,61 Mt und 120 Quellen wie bisher, Netz
6.642 statt 6.123 km, Kapazitätskosten 44,0 statt 78,0 M€/a, Gap 14,6 statt 12,95 %. Wegen
des Zeitlimits (und eines parallel laufenden Rechners) sind die genauen Werte unsicher; ein
Lauf mit Gurobi und engem Gap wäre die bessere Referenz.

Ausführen wie bisher, z. B.:

```bash
export CO2_NETWORK_DATA_ROOT=/pfad/zu/04_processed_data/CO2_Network
export CO2_NETWORK_SCENARIO_SET="Base only" CO2_NETWORK_DEMAND=1
cd co2_network_module && python network.py && python main.py
```

## Datenpakete statt Einzeldateien

Die IGC.NRW-Datenpipelines veröffentlichen versionierte Pakete unter
`04_processed_data/hiscience/<tool>/<version>/` bzw. `03_intermediate/hiscience/…`
(`transport-network`). Direkt lesbar ist bisher nur `transport-network`
(`road_simplified.parquet`, `waterway_simplified.parquet` statt `simple_grid_*.pkl` über
`CO2_NETWORK_GRID_STREET`/`_WATER`; Wasser identisch, Straße siehe unten). Die übrigen Pakete
können Einzeldateien ersetzen, brauchen aber eine Umwandlung bzw. Spaltenzuordnung
(`load_geodataframe` liest dafür bereits `.parquet`): `co2-point-sources` +
`co2-source-classes` statt `emissions.xlsx` (Abgleich: 1.677 von 1.694 Zeilen identisch),
`nuts-regions` statt der NUTS-gpkg. HiScience macht diese Zuordnung in der App mit einem
Adapter; ob sie in den RUB-Code soll, ist abzustimmen.

## Offene Fragen an RUB

- **Radien des vereinfachten Graphen:** Der Code hat 10/20 km (Straße) und 15/15 km (Wasser),
  die Pickles entstanden mit 5/10 km und mit niederländischen Autobahnen
  (`streets_nrw_gdf.pkl`, Quelle `Wegvakken.gpkg`). Welche Werte gelten? Herkunft und Lizenz
  von `Wegvakken.gpkg`?
- **Gebiet der Quellen:** `emissions.xlsx` enthält alle 1.694 ETS-Anlagen Deutschlands; „Base
  only“ hat 101 Anlagen (31,9 Mt) außerhalb NRW. Gewollt?
- **Einheit der CCS-Kosten:** `emissions.xlsx` 30–145 (EUR/t?), `sources_module.py` dieselben
  Werte × 1.000 (EUR/kt?).
- **NACE 17.11** hat kein Szenario und fällt immer heraus. Gewollt?
- Herkunft von `CO2_demand.xlsx` und `nace_definitions.xlsx` (fehlt auf Sciebo).
- Lizenz des Repos.
