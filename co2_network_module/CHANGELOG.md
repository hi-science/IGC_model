# Changelog – CO₂-Netzwerk (`co2_network_module`)

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/) als Tag `co2-network-vX.Y.Z`
(`CONTRIBUTING.md` §3).

## [Unreleased]

Vorschlag von HiScience (Branch `hiscience/io-vorschlag-roman`, siehe `HISCIENCE.md`).

### Geändert
- Pfade, Szenario-Set, `demand`-Schalter und Solver per Umgebung statt fest im Code
  (`CO2_NETWORK_DATA_ROOT`, `CO2_NETWORK_SCENARIO_SET`, `CO2_NETWORK_DEMAND`,
  `CO2_NETWORK_SOLVER(_OPTIONS)`); Default-Solver HiGHS.
- Eingaben auch als GeoParquet aus versionierten Datenpaketen (`CO2_NETWORK_GRID_STREET`/`_WATER`).
- Ergebnisse in `Results/` werden nicht mehr versioniert.

### Behoben – ändert Ergebnisse
- Stahl-Flexibilität (NACE 24.1) wird jetzt angewendet (war wirkungslos).
- `move_source`: Endpunkt einer Kante ist `coords[-1]`.

### Hinzugefügt
- `CONTRIBUTING.md`, `docs/MODEL.md` (Entwurf), dieses Changelog.

## Vor dem Changelog

Stand `c0a36e1` (19.08.2026): Ethylen-Senken (`CO2_demand.xlsx`) aufgenommen.
