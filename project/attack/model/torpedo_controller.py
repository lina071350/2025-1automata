import platform
from pyjevsim import BehaviorModel, Infinite
import datetime
import math

from pyjevsim.system_message import SysMessage


class TorpedoCommandControl(BehaviorModel):
    def __init__(self, name, platform):
        BehaviorModel.__init__(self, name)

        self.platform = platform

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Decision", 0)

        self.insert_input_port("threat_list")
        self.insert_output_port("target")
        self.threat_list = []

        self.min_distance = float("inf")

    def ext_trans(self, port, msg):
        if port == "threat_list":
            print(f"{self.get_name()}[threat_list]: {datetime.datetime.now()}")
            self.threat_list = msg.retrieve()[0]
            self._cur_state = "Decision"

    def output(self, msg):
        target = None
        target_pos = None

        for t in self.threat_list:
            target = self.platform.co.get_target(self.platform.mo, t)
            torpedo_pos = self.platform.mo.get_position()

            distance = self.distance_to(torpedo_pos, target)

            if distance < self.min_distance:
                self.min_distance = distance
                target_pos = target
                target = t

        if self.min_distance <= 5.0:
            print(f"[{self.get_name()}][SUCCESS] Torpedo reached target")

        # house keeping
        self.threat_list = []
        self.platform.co.reset_target()

        if target:
            message = SysMessage(self.get_name(), "target")
            message.insert(target_pos)
            msg.insert_message(message)

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