import json ;
import threading;

#TODO CLOCK SENSITIVE

class module(object):

    bot_cmd = "tbot" ;
    config = None;

    def login_check_dec(function):
        def wrapper(*args, **kargs):
            if args[2] != module.config["login"]:
                return function(*args, **kargs) ;
            else:
                return None ;
        return wrapper ;



    def lock_dec(function):
        lock = threading.Lock();
        def wrapper(*args, **kargs):
            with lock:
                return function(*args, **kargs) ;
        return wrapper ;


    def clock_dec(function):
        '''
        Deprecated
        :return:
        '''
        def wrapper(*args, **kargs):
            if args[0].clock_sensitive:
                return function(*args, **kargs)
            else:
                return None
        return wrapper ;


    def module_on_dec(function):
        def wrapper(*args, **kargs):
            if args[0].is_module_on:
                return function(*args, **kargs)
            else:
                return None
        return wrapper ;

    def check_command_dec(function):
        '''
        Deprecated
        :return:
        '''
        def wrapper(*args, **kargs):
            s = args[0];
            raw_args = args[1].split() ;
            if len(raw_args) >= 2 and raw_args[0] == module.config["bot_cmd"] and raw_args[1] in s.keywords:
                if len(raw_args) == 3:
                    if raw_args[2] == "uninstall":
                        room = args[3];
                        return s.remove(room) ;
                return function(*args, **kargs) ;
            else:
                return None ;
        return wrapper ;

    def check_command(self, cmd):
        raw_cmd = cmd.split() ;
        return len(raw_cmd) >= 2 and raw_cmd[0] == module.config["bot_cmd"] and raw_cmd[1] in self.keywords ;

    def __init__(self, keyword = None, is_permanent = False):
        self.module_name = "DEFAULT_MODULE_NAME"
        self.room_list = set() ;
        self.timer = 0 ;
        self.clock_sensitive = True ;
        self.is_module_on = True ;
        self.help = "" ;
        self.whatis = "" ;
        self.raw_args = [] ;
        self.is_permanent = is_permanent ;
        if keyword:
            self.keywords = [keyword] ;
        else:
            self.keywords = ["Default_Module_Name"] ;
        self.__version__ = "0.0.1"


    def add_room(self, room):
        self.room_list.add(room.current_alias);

    def remove_room(self, room):
        self.room_list.remove(room.current_alias)

    def get_room_list(self):
        return self.room_list;

    @module_on_dec
    def run(self, cmd, sender = None, room = None):
        pass

    @module_on_dec
    def run_on_clock(self, room=None):
        pass

    def exit(self):
        pass

    def on_start(self):
        return None;

    @module_on_dec
    def clock_update(self):
        self.timer += 1 ;

    def reset_clock(self):
        self.timer = 0 ;

    def set_clock_sensitivity_on(self):
        self.clock_sensitive = True ;

    def set_clock_sensitivity_off(self):
        self.clock_sensitive = False ;

    def is_clock_sensitive(self):
        return self.clock_sensitive;

    def get_timer(self):
        return self.timer ;

    def is_module_activated(self):
        return self.is_module_on ;

    def set_module_on(self):
        self.is_module_on = True ;

    def set_module_off(self):
        self.is_module_on = False ;

    def process_msg_active(instruction, sender, room):
        pass

    def process_msg_passive(self, cmd, sender, room):
        pass

    def run(self, cmd, sender=None, room=None):
        instruction_set = cmd.split("\n") ;
        ret = [] ;
        for instruction in instruction_set:
            raw_args = instruction.split() ;
            tmp = "" ;
            ## Activate Part
            if len(raw_args) == 3 and raw_args[0] == module.config["bot_cmd"] and raw_args[1] in self.keywords and raw_args[2] == "activate":
                if self.is_module_activated():
                    tmp = "Module {} is already activated.".format(self.keywords[0]) ;
                else:
                    self.set_module_on() ;
                    tmp = "Module {} is activated".format(self.keywords[0])
            ## Deactivate Part
            if len(raw_args) == 3 and raw_args[0] == module.config["bot_cmd"] and raw_args[1] in self.keywords and raw_args[2] == "deactivate":
                if not(self.is_module_activated()):
                    tmp = "Module {} is already deactivated.".format(self.keywords[0]) ;
                elif self.is_permanent:
                    tmp =  "Module {} can not be deactivated.".format(self.keywords[0]) ;
                else:
                    self.set_module_off() ;
                    tmp = "Module {} is deactivated.".format(self.keywords[0]) ;
            ## Process Active / Passive
            if tmp == "":
                if len(raw_args) >= 2 and (raw_args[0] == module.config["bot_cmd"]) and (raw_args[1] in self.keywords):
                    if self.is_module_activated():
                        tmp = self.process_msg_active(instruction, sender, room) ;
                else:
                    if self.is_module_activated():
                        if len(raw_args) > 0:
                            tmp = self.process_msg_passive(instruction, sender, room);
            ## End of Processing
            if tmp:
                ret.append(tmp);
                # ret += tmp+'\n' ;
        return ret;

if __name__ == "__main__":
    mod = module() ;
    mod.clock_update() ;
    print(mod.timer)
    mod.clock_sensitive_off() ;
    print(mod.timer)
