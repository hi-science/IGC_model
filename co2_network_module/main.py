import os
import pypsa
import numpy as np

import data
#import network
#from network import nrw
import constraints as nrw_constr

# HiScience overlay: switched solver from Gurobi (commercial) to HiGHS
# (open-source). PyPSA supports HiGHS natively via `highspy`.
# Solver options come from the app config (JSON in CO2_NETWORK_SOLVER_OPTIONS).
import json as _json
_SOLVER_NAME = os.environ.get("CO2_NETWORK_SOLVER", "highs")
_SOLVER_OPTS = (
    _json.loads(os.environ["CO2_NETWORK_SOLVER_OPTIONS"])
    if os.environ.get("CO2_NETWORK_SOLVER_OPTIONS")
    else {"mip_rel_gap": 0.005, "presolve": "on"}
    if _SOLVER_NAME == "highs"
    else {'MIPGap': 0.005, 'MIPFocus': 3, 'Heuristics': 0.2, 'Cuts': 2,
          'Presolve': 2, 'ImproveStartTime': 600, }
)

# HiScience overlay: same switch as network.py (upstream: network.py True,
# main.py False -> main.py would load a network without the demand sinks).
demand = os.environ.get('CO2_NETWORK_DEMAND', '1') == '1'
scenario = data.scenario_name

if demand:
    nrw = pypsa.Network(f"Results/nrw_raw_{scenario}_d.nc")
else:
    nrw = pypsa.Network(f"Results/nrw_raw_{scenario}_nd.nc")
    
def main():
    
            
    nrw.optimize(
    solver_name=_SOLVER_NAME,
    multi_investment_periods=True,
    solver_options=_SOLVER_OPTS,
    extra_functionality=nrw_constr.constraints)
    #solver_options={'MIPGap': 0.01,},
    #extra_functionality=nrw_constr.constraints)       

    path = 'Results/nrw_optimized_'
    path += scenario
    if demand:
        path += '_d'
    else:
         path += '_nd'
    path += '.nc'
    nrw.export_to_netcdf(path)


if __name__ == '__main__':
    main()