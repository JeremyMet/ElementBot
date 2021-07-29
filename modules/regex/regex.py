from modules.module import module ;
import re ;

class regex(module):

    def __init__(self, keyword = "regex", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.help = "Useless module" ; # <- will be printed out by the admin module
        self.whatis = "A Simple regex module."
        self.__version__ = "0.0.1"
        self.regex_dic = {}


    @module.login_check_dec # ignore when messages come from the bot itself.
                            # it can be useful to listen to what the bot says in some cases
    def process_msg_active(self, cmd, sender, room):
        # <-- Your code goes here.
        raw_args = cmd.split() ;
        extract_strings = re.findall('"(.*?)"', cmd) ;
        if len(extract_strings) == 2:
            try:
                p = re.compile(extract_strings[0]) ;
            except:
                return "Not a valid regex."
            else:
                self.regex_dic[p] = extract_strings[1] ;
                return "Regex has been recorded."
        return None ;

    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        ret = "" ;
        for p, val in self.regex_dic.items():
            if p.match(cmd):
                ret += val+'\n' ;
        return ret[:-1] ;

    @module.module_on_dec
    def run_on_clock(self):
        # <- Your code goes here.
        pass

    def exit(self):
        # <- Your code goes here.
        # This function is called when the bot is shut down,
        # this can for instance be used to save temporary variables into files.
        pass