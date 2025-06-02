import platform
from pyjevsim import BehaviorModel, Infinite
import datetime

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

        # 총예산 및 사용량
        self.total_budget = 10.0
        self.used_budget = 0.0

    def ext_trans(self,port, msg):
        if port == "threat_list":
            print(f"{self.get_name()}[threat_list]: {datetime.datetime.now()}")
            self.threat_list = msg.retrieve()[0]
            self._cur_state = "Decision"

    def output(self, msg):
        #target = None
        
        #for t in self.threat_list:
        #    target =  self.platform.co.get_target(self.platform.mo, t)

        target = None
        min_distance = float("inf")
        for t in self.threat_list:
            candidate = self.platform.co.get_target(self.platform.mo, t)
            if candidate and hasattr(candidate, "distance"):
                if candidate.distance < min_distance:
                    target = candidate
                    min_distance = candidate.distance

        # 타겟이 가까우면 기만기 사용
        if target and min_distance < 5:
            remaining = self.total_budget - self.used_budget

            if remaining >= 2.5:
                self.platform.lo.decoy_list.append({"type": "self_propelled", "lifespan": 5})
                self.used_budget += 2.5
                print(f"{self.get_name()}: 자항식 기만기 추가 (누적 비용: {self.used_budget})")
            elif remaining >= 1.0:
                self.platform.lo.decoy_list.append({"type": "stationary", "lifespan": 5})
                self.used_budget += 1.0
                print(f"{self.get_name()}: 고정식 기만기 추가 (누적 비용: {self.used_budget})")
            else:
                print(f"{self.get_name()}: 예산 부족으로 기만기 미사용")
        else:
            print(f"{self.get_name()}: 타겟 없음 또는 거리 멂 (min_distance={min_distance})")
       
        # house keeping
        self.threat_list = []
        self.platform.co.reset_target()
        
        if target:
            message = SysMessage(self.get_name(), "target")
            message.insert(target)
            msg.insert_message(message)
        
        return msg
        
    def int_trans(self):
        if self._cur_state == "Decision":
            self._cur_state = "Wait"