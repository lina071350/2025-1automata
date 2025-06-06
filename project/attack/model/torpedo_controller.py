import math
import datetime
from pyjevsim import BehaviorModel, Infinite
from pyjevsim.system_message import SysMessage
from utils.object_db import ObjectDB


class TorpedoCommandControl(BehaviorModel):
    def __init__(self, name, platform):
        BehaviorModel.__init__(self, name)

        self.platform = platform
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Decision", 0)

        self.insert_input_port("threat_list")
        self.insert_output_port("target")
        self.insert_output_port("mission_complete")

        self.threat_list = []
        self.mission_completed = False

    def ext_trans(self, port, msg):
        if port == "threat_list":
            print(f"{self.get_name()}[threat_list]: {datetime.datetime.now()}")
            self.threat_list = msg.retrieve()[0]
            self._cur_state = "Decision"

    def output(self, msg):
        if self.mission_completed:
            return msg

        closest_target = None
        min_distance = float("inf")

        for t in self.threat_list:
            target = self.platform.co.get_target(self.platform.mo, t)

            torpedo_pos = self.platform.mo.get_position()
            distance = self.distance_to(torpedo_pos, target)
            print(f"{self.get_name()} Distance to target: {distance:.2f}")

            if distance < min_distance:
                min_distance = distance
                closest_target = target

            if distance <= 3.0:
                print(f"[{self.get_name()}] Target position reached.")
                self.mission_completed = True

                # 미션 완료 메시지 전송
                success = SysMessage(self.get_name(), "mission_complete")
                success.insert("SUCCESS")
                msg.insert_message(success)

                # ObjectDB에서 torpedo 제거
                if self.platform.mo in ObjectDB().items:
                    ObjectDB().items.remove(self.platform.mo)

                break

        self.threat_list = []
        self.platform.co.reset_target()

        if closest_target and not self.mission_completed:
            follow = SysMessage(self.get_name(), "target")
            follow.insert(closest_target)
            msg.insert_message(follow)

        return msg

    def int_trans(self):
        if self._cur_state == "Decision":
            self._cur_state = "Wait"

    def distance_to(self, pos1, pos2):
        return math.sqrt(
            (pos1[0] - pos2[0]) ** 2
            + (pos1[1] - pos2[1]) ** 2
            + (pos1[2] - pos2[2]) ** 2
        )