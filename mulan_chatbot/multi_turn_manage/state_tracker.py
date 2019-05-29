# -*- coding: utf-8 -*-


# this model is from my another repository travel_consult_chatbot (https://github.com/ricosr/travel_consult_chatbot)

class State:
    def __init__(self, slot_state):
        self.last_slot_state = slot_state
        self.state_dict = {}

    def update_last_slot_state(self, slot_state):
        self.last_slot_state = slot_state

    def get_last_slot_state(self):
        return self.last_slot_state

    def add_one_state(self, slot_state, slot_value, confidence):
        self.state_dict[slot_state] = {"slot_value": slot_value, "confidence": confidence}

    def update_slot_value(self, slot_state, slot_value):
        self.state_dict[slot_state]["slot_value"] = slot_value

    # def update_confidence(self, slot_state, confidence):
    #     self.state_dict[slot_state]["confidence"] = confidence

    def get_state(self):
        return self.state_dict

    def get_slot_value(self, slot_state):
        return self.state_dict[slot_state]["slot_value"]

    # def get_confidence(self, slot_state):
    #     return self.state_dict[slot_state]["confidence"]

    # def update_all_state(self, ie_values_dict):
    #     if ie_values_dict:
    #         for k, v in ie_values_dict.items():
    #             if v and v != 0:
    #                 if k in self.get_state():
    #                     if self.get_slot_value(k) == v:
    #                         self.update_confidence(k, 1)
    #                     else:
    #                         self.update_slot_value(k, v)
    #                         self.update_confidence(k, 0.5)
    #                 else:
    #                     self.add_one_state(k, v, 0.5)

    # def get_current_slot(self, current_slot):
    #     if self.get_state():
    #         for slot_key, value_dict in self.get_state().items():
    #             if self.get_confidence(slot_key) == 1:
    #                 current_slot[slot_key] = value_dict["slot_value"]
    #             if self.get_confidence(slot_key) == 0:
    #                 current_slot[slot_key] = "no"

    # def get_need_to_confirm(self):
    #     confirm_key_ls = []
    #     for slot_state, value_dict in self.get_state().items():
    #         if self.get_confidence(slot_state) < 1:
    #             confirm_key_ls.append(slot_state)
    #     return confirm_key_ls

    # def judge_dialogue_state(self):
    #     if self.state_dict:
    #         for slot_state, value_dict in self.state_dict.items():
    #             if value_dict["slot_value"] is not None and value_dict["slot_value"] != 0 and value_dict["confidence"] == 1:
    #                 continue
    #             else:
    #                 return False
    #         return True   # all slots are OK
    #     else:
    #         return False