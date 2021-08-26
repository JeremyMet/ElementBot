import datetime;

class module(object):
    def __init__(self):
        self.clock = datetime.datetime.now();
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
    def get_clock(self):
        now = datetime.datetime.now();
        delta = (now-self.clock).seconds;
        return delta ;
    #
    def process_msg_active(instruction, sender, room):
        pass
    #
    def reset_clock(self):
        self.clock = datetime.datetime.now();
