from modules.module import module ;
from .mastermind import mastermind
import re
import unidecode
from .mastermind_unicode import mastermind_unicode;


class mastermind_bot(module):

    def __init__(self, keyword = "mastermind", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.module_name = "mastermind"
        self.whatis = "A simple Mastermind Game."
        self.__version__ = "0.0.1"
        self.mastermind_inst = mastermind()
        self.help = "" ;
        for key, value in mastermind_unicode.emoticon_dico.items():
            self.help += (key+"=="+value+", ");
        self.help = self.help[:-2]; #remove comma
        self.help += "\n"


    @module.login_check_dec # ignore when messages come from the bot itself.
                            # it can be useful to listen to what the bot says in some cases
    def process_msg_active(self, cmd, sender, room):
        raw_cmd = cmd.split(" ");
        if len(raw_cmd) == 3 and raw_cmd[2] == "help":
            return self.help;
        if len(raw_cmd) == 3 and raw_cmd[2] == "state":
            return self.mastermind_inst.str_game_state;

    #@module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        #match = re.findall('\§([a-zA-Z]+)', (unidecode.unidecode(cmd)))
        if self.mastermind_inst.check_proposition_consistency(cmd):
            self.reset_clock();
            return self.mastermind_inst.propose(cmd) ;


    @module.module_on_dec
    def run_on_clock(self, room=None):
        # <- Your code goes here.
        pass

    def exit(self):
        # <- Your code goes here.
        # This function is called when the bot is shut down,
        # this can for instance be used to save temporary variables into files.
        pass
