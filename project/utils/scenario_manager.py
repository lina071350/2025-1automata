import yaml
import importlib

class ScenarioManager:
    def __init__(self, abs_path, sce_name="", apath="", dpath=""):
        attack_path = f"attack{apath}.model.torpedo"
        apkg = importlib.import_module(attack_path)

        defense_path = f"defense{dpath}.model.surfaceship"
        dpkg = importlib.import_module(defense_path)
        
        ship_cls = getattr(dpkg, 'SurfaceShip')
        torpedo_cls = getattr(apkg, 'Torpedo')

        # Read YAML file
        with open(f"{abs_path}\\attack{apath}\\scenario\\{sce_name}", 'r') as f:
            yaml_data = yaml.safe_load(f)
            self.torpedoes = [torpedo_cls(f"red_torpedo_{idx}", d) for idx, d in enumerate(yaml_data['Torpedo'])]
        
        with open(f"{abs_path}\\defense{dpath}\\scenario\\{sce_name}", 'r') as f:
            yaml_data = yaml.safe_load(f)
            self.surface_ships = [ship_cls(f"blue_ship_{idx}", d) for idx, d in enumerate(yaml_data['SurfaceShip'])]

    def get_surface_ships(self):
        return self.surface_ships

    def get_torpedoes(self):
        return self.torpedoes