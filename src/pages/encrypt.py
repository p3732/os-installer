import os
import subprocess


class Encrypt:
    def __init__(self, builder, global_state):
        self.global_state = global_state

        self.pin_box = builder.get_object("encrypt_pin_box")
        self.pin_field = builder.get_object("encrypt_pin_field")

        # switch signals
        switch = builder.get_object("encrypt_switch")
        switch.connect("state-set", self.on_switch_flipped)

    def load(self, config):
        return

    def on_switch_flipped(self, switch, state):
        self.global_state.encrypt = state
