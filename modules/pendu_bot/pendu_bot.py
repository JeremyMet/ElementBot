import json
import random
import re
import unidecode
#
from .pendu import pendu
from modules.module import module ;

class pendu_bot(module):


    def __init__(self, keyword = "pendu"): # <- template ... Here goes your default module name
        super().__init__();
        self.module_name = "pendu_bot"
        self.help = "type tbot pendu help for further details.";
        self.whatis = "Un simple jeu du pendu."
        self.__version__ = "0.0.1"
        self.pendu = pendu() ;
        self.keyword = keyword;
    #
    def on_start(self):
        ret = "<b>\uD83E\uDDE0 ~~~ Jeu du Pendu ~~~ \uD83E\uDDE0</b> \n"+str(self.pendu);
        return ret;
    #
    def process_msg_active(self, cmd, sender = None, room = None):
        #
        match = re.fullmatch('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
        if match:
            # self.reset_clock();
            current_prop = match[0];
            tmp_str = self.pendu.propose(current_prop[1:]);
            return tmp_str;
        #
        args = cmd.split(" ") ;
        if (args[0] != self.keyword):
            return None;
        #
        if (len(args) == 2):
            if args[1] == "show":
                return str(self.pendu) ;
            elif args[1] == "score":
                return self.pendu.show_score() ;
            elif args[1] == "letters":
                return self.pendu.show_lt() ;
            elif args[1] == "debug":
                return "debug \n" ;
            elif args[1] == "words":
                return self.pendu.get_word_list();
            elif args[1] == "help":
                return "tbot pendu propose A pour proposer la lettre A, \n \
    tbot pendu show montre l'état actuel du mot, \n \
    tbot pendu event montre l'event en cours (s'il y en a)";
            elif args[1] == "event":
                return self.pendu.show_event() ;
        else:
            return None ;
    #
    def run_on_clock(self, room=None):
        if self.get_clock() > 28800: # 8 hours.
            self.pendu.save_score() ;
            self.reset_clock() ;
            return "\U0001f4be <b>Sauvegarde du Score</b> \U0001f4be\n\u26A0\uFE0F Rappel ! \n"+str(self.pendu) ;
    #
    def exit(self):
        self.pendu.save_score() ;
        if self.pendu.lt:
            return "\u26A0\uFE0F Oooh Non ! Vous avez été trop lents \U0001F606 ! Le mot cherché était \"<b>{}</b>\".".format(self.pendu.current_word);
        else:
            return None;

if __name__ == "__main__":
    pb = pendu_bot() ;
