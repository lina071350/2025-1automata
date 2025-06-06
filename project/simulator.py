import project_config
import sys

from pyjevsim import SysExecutor, ExecutionType, Infinite
from utils.scenario_manager import ScenarioManager
from utils.pos_plotter import PositionPlotter
from utils.object_db import ObjectDB

import os
abs_path = os.path.dirname(os.path.abspath(__file__))

attack = ""
defense = ""

if len(sys.argv) == 3:
	if sys.argv[1]:
		attack = sys.argv[1]
	if sys.argv[2]:
		defense = sys.argv[2]

pos_plot = PositionPlotter()
sm = ScenarioManager(abs_path, "stationary_decoy.yaml", attack, defense)
se = SysExecutor(1, ex_mode=ExecutionType.R_TIME)
ObjectDB().set_executor(se)

se.insert_input_port("start")

for ship in sm.get_surface_ships():
	se.register_entity(ship)
	se.coupling_relation(se, "start", ship, "start")

for torpedo in sm.get_torpedoes():
	se.register_entity(torpedo)
	se.coupling_relation(se, "start", torpedo, "start")
	pass

se.insert_external_event("start", None)

for _ in range(30):
	se.simulate(1)
	for ship in sm.get_surface_ships():
		x, y, z = ship.get_position()
		pos_plot.update_position('ship', x, y, z)

	for torpedo in sm.get_torpedoes():
		x, y, z = torpedo.get_position()
		pos_plot.update_position('torpedo', x, y, z, 'black', 'orange')

	for name, decoy in ObjectDB().decoys:
		x, y, z = decoy.get_position()
		pos_plot.update_position(name, x, y, z, 'black', 'green')

#print(se.model_map)
se.terminate_simulation()

