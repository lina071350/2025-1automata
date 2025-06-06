import datetime 
import math

from pyjevsim import BehaviorModel, Infinite
from utils.object_db import ObjectDB

from .stationary_decoy import StationaryDecoy
from .self_propelled_decoy import SelfPropelledDecoy
from ..mobject.stationary_decoy_object import StationaryDecoyObject
from ..mobject.self_propelled_decoy_object import SelfPropelledDecoyObject

# 방어 시스템에서 기만기를 생성/발사하는 객체
class Launcher(BehaviorModel):
    def __init__(self, name, platform):
        BehaviorModel.__init__(self, name)
        
        self.platform = platform
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Launch", 0)

        self.insert_input_port("order")

        self.launch_flag = False

    def ext_trans(self, port, msg):
        if port == "order":
            print(f"{self.get_name()}[order_recv]: {datetime.datetime.now()}")
            self._cur_state = "Launch"

    def output(self, msg):
        if not self.launch_flag:
            se = ObjectDB().get_executor()
            position = self.platform.get_position()

            # 직접 고정식 2개, 자항식 2개 정의
            decoy_list = [
                {"type": "stationary", "lifespan": 30, "elevation": 0, "azimuth": 0, "speed": 0},
                {"type": "stationary", "lifespan": 30, "elevation": 0, "azimuth": 180, "speed": 0},
                {"type": "self_propelled", "lifespan": 20, "speed": 15, "xy_speed": 15, "heading": 90, "elevation": 0, "azimuth": 90},
                {"type": "self_propelled", "lifespan": 20, "speed": 15, "xy_speed": 15, "heading": 270, "elevation": 0, "azimuth": 270},
            ]      

            for idx, decoy in enumerate(decoy_list):
                destroy_t = math.ceil(decoy['lifespan'])

                if decoy["type"] == "stationary":
                    sdo = StationaryDecoyObject(position, decoy)
                    decoy_model = StationaryDecoy(f"[Decoy][{idx}]", sdo)
                elif decoy["type"] == "self_propelled":
                    sdo = SelfPropelledDecoyObject(position, decoy)
                    decoy_model = SelfPropelledDecoy(f"[Decoy][{idx}]", sdo)
                else:
                    continue

                ObjectDB().decoys.append((f"[Decoy][{idx}]", sdo))
                ObjectDB().items.append(sdo)
                se.register_entity(decoy_model, 0, destroy_t)

            self.launch_flag = True

        return None

    def int_trans(self):
        if self._cur_state == "Launch":
            self._cur_state = "Wait"