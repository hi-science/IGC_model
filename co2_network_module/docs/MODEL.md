---
title: "CO₂-Netzwerk (PyPSA-MILP)"
updated: 2026-10-15
upstream: "https://github.com/OliverLinsel/IGC_model · Branch roman · Basis c0a36e1 + HiScience-Vorschlag"
---

# CO₂-Netzwerk (PyPSA-MILP)

> **Entwurf von HiScience**, aus dem Code abgeleitet (Stand `c0a36e1` mit den Commits dieses
> Vorschlags). Bitte von RUB prüfen, ergänzen und ab dann mit jedem Release pflegen
> (`CONTRIBUTING.md` §4). Stellen mit „(prüfen)“ sind aus dem Code gelesen, nicht bestätigt.

## Zweck

Kostenoptimaler Ausbau eines multimodalen CO₂-Transportnetzes (Pipeline, LKW, Binnenschiff)
von Industriequellen zu den Nordsee-Speichern (Aurora) und zu CO₂-Senken der
Ethylen-Produktion, Stützjahre 2030–2050. Je Quelle und Jahr entscheidet das Modell, ob CO₂
entweicht oder abgeschieden und über welchen Verkehrsträger es transportiert wird.

## Methode

Gemischt-ganzzahliges lineares Programm (MILP) in PyPSA mit eigenen Nebenbedingungen
(`constraints.py`), Multi-Period-Investment mit einem Snapshot je Periode
$y \in \{2030, 2034, 2038, 2042, 2046, 2050\}$, diskontiert mit
$\delta_y = (1+r)^{-(y-2030)}$, $r = 0{,}05$.

**Netzaufbau** (`data.py`, `network.py`): Anlagen gleicher NACE-Klasse im Umkreis von 5 km
werden gebündelt; Binnenhäfen werden ausgedünnt (≥ 50 km Abstand). Quellen, Terminals, Häfen
und Senken werden an den nächsten Knoten des vereinfachten Straßen- bzw. Wasserstraßengraphen
gehängt. Je Standort gibt es eine Ebene je Verkehrsträger (`_P`, `_T`, `_W`), verbunden über
Umschlag-Links.

**Zielfunktion:**

$$
\min \sum_{\ell} c^{\mathrm{cap}}_{\ell}\,\bar p_{\ell}
+ \sum_{s} \delta_{y(s)} \Big( \sum_{\ell} c^{\mathrm{marg}}_{\ell,s}\, p_{\ell,s}
+ \sum_{q} c^{\mathrm{CO_2}}_{s}\, g_{q,s} \Big)
+ \sum_{y} \delta_y \sum_{\ell \in L_P} c^{\mathrm{fix}}_\ell\, d_\ell\, (y_{\ell,y} - y_{\ell,y-1})
$$

mit Transportkosten je km und Verkehrsträger, anlagenspezifischen Abscheidekosten
(`CCS Cost`), Injektionskosten, dem CO₂-Preis $c^{\mathrm{CO_2}}_s$ auf das Aufkommen der
Quellen (`co2_price`, 100 000 … 200 000 je kt von 2030 bis 2050) und Bau-Fixkosten je
Pipeline-km (onshore 100 000, offshore 171 000), die im Baujahr anfallen. Einheiten (prüfen).

**Nebenbedingungen:** Knotenbilanz (PyPSA), Kapazitätskopplung $0 \le p_{\ell,s} \le \bar p_\ell$,
CO₂-Bedarf der Senken $D_{k,y}$ (Schalter `demand`), Obergrenze für entweichendes CO₂ mit
$\phi_y = \max(0, \min(0{,}9, (2050-y)/20))$, Pipeline-Bau binär mit Big-M
(einmal gebaut bleibt gebaut), kein Zwischenspeichern an Quellen, festes Aufkommen je Quelle
(`p_min_pu = 1`), außer Stahl (NACE 24.1): 10–100 % (`p_min_pu = 0,1`), gesteuert über den
CO₂-Preis.

## Eingaben

Alle Dateien liegen in `CO2_NETWORK_DATA_ROOT` (Ordner). `CO2_NETWORK_GRID_STREET`/`_WATER`
nennen die Dateinamen der Graphen in diesem Ordner (Pickle oder GeoParquet).

| Eingabe | Inhalt | Versioniertes Datenpaket (Sciebo) |
|---|---|---|
| `emissions.xlsx` | Anlagen mit `tco2_2023`, NACE, `Scenario`, `CCS Cost`, Koordinaten | `co2-point-sources` + `co2-source-classes` (mit Umwandlung) |
| `NUTS_RG_01M_2024_3035.gpkg`, `NUTS3_NRW_2024_4326.gpkg` | Gebiete | `nuts-regions` |
| `simple_grid_Street.pkl`, `simple_grid_Water.pkl` | vereinfachte Graphen | `transport-network` (`road_simplified.parquet`, `waterway_simplified.parquet`) |
| `binnenschiff_haefen.gpkg` | Binnenhäfen | `transport-network` (`nodes.parquet`) |
| `CO2_demand.xlsx` | Senken (Blatt `Ethylen`), kt/a je Stützjahr | – (Herkunft offen) |

## Ausgaben

`Results/nrw_optimized_<set>_<d|nd>.nc`: gelöstes PyPSA-Netz (Links mit `p_nom_opt`, Flüsse,
Kosten). Mengen in kt CO₂/a, Kosten je kt (prüfen).

## Parameter und Szenarien

| Parameter | Wert | Hinweis |
|---|---|---|
| `CO2_NETWORK_SCENARIO_SET` | `Base only`, `Base and S1`, … | filtert Quellen nach Spalte `Scenario` |
| `CO2_NETWORK_DEMAND` | `1`/`0` | Senken einbeziehen |
| `CO2_NETWORK_SOLVER`, `_OPTIONS` | Default HiGHS | Gurobi wie bisher möglich |
| Diskontsatz | 0,05 | `data.py` |
| Injektionskosten | 15 000 je kt | = 15 €/t (prüfen) |
| CO₂-Preis `co2_price` | 100 000 (2030) … 200 000 (2050) je kt | in 20 000er Schritten je Stützjahr (prüfen: €/kt) |

## Annahmen und Grenzen

- Aufkommen je Quelle fest (Basisjahr 2023), über alle Stützjahre gleich; nur Stahl kann
  zwischen 10 und 100 % liegen.
- Ein Zeitschnitt je Stützjahr, keine unterjährige Dynamik.
- Kosteneinheiten sind im Code nicht dokumentiert (prüfen).
- Mit HiGHS wird die Toleranz von 0,5 % in vertretbarer Zeit nicht erreicht; Ergebnisse mit
  Zeitlimit sind zulässig, aber nicht nachweislich nahe-optimal (Gap angeben).

## Änderungen

Siehe `CHANGELOG.md`.
