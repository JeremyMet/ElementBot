class module(object):
    def __init__(self):
        self.clock = 0;
    #
    def run_on_clock(self, room=None):
        pass
    #
    def exit(self):
        return None;
    #
    def on_start(self):
        return None;
    #
    def clock_update(self):
        self.clock += 1 ;
    #
    def get_clock(self):
        return self.clock ;
    #
    def process_msg_active(instruction, sender, room):
        pass
    #
    def reset_clock(self):
        self.clock = 0;
