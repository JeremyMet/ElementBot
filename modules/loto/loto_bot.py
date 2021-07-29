import random ;
from modules.module import module ;
from .loto import loto;
import datetime;
import pickle;
import copy;

class loto_bot(module):

    def __init__(self, keyword = "loto", flask_scoreboard = "./modules/loto/flask_scoreboard.dic", hour=0, minute=0): # <- template ... Here goes your default module name
        super().__init__(keyword) ;
        self.help = "propose (1,2,3,4,5,6)" ; # <- will be printed out by the admin module
        self.whatis = "A loto hello module. "
        self.module_name = "Loto Module"
        self.__version__ = "0.0.1"
        self.loto_inst = loto(hour=hour, minute=minute);
        self.flask_scoreboard = flask_scoreboard;
        self.flask_scoreboard_array = {}
        try:
            with open(flask_scoreboard, "rb") as pickle_file:
                self.flask_scoreboard_array = pickle.load(pickle_file);
        except:
            pass

    @module.module_on_dec
    def process_msg_active(self, cmd, sender=None, room=None):
        raw_cmd = cmd.split(" ");
        ret = "" ;
        if (len(raw_cmd) == 3 and raw_cmd[2] == "dailybet"):
            ret = self.loto_inst.get_dailybet();
        elif (len(raw_cmd) == 3 and raw_cmd[2] == "scoreboard"):
            ret = self.loto_inst.get_scoreboard();
        elif (len(raw_cmd) == 3 and raw_cmd[2] == "draw"):
                ret = self.loto_inst.check_result();
        return ret ;

    @module.module_on_dec
    def process_msg_passive(self, cmd, sender=None, room=None):
        ret = self.loto_inst.bet(sender, cmd);
        return ret;


    @module.module_on_dec
    # @module.clock_dec
    def run_on_clock(self, room=None):
        log = self.loto_inst.get_log();
        last_draw = log["last_draw"];
        now = datetime.datetime.now();
        one_day = datetime.timedelta(days=1);
        # Nous avons changé de jour ...
        delta = now-last_draw;
        if delta.days > 0:
            ret = self.loto_inst.check_result();
            self.loto_inst.save_current_state();
            # Dans le cas où l'on change de mois,
            # (pas très propre de gérer tout ça dans cette fonction mais bon ...)
            if ((now+one_day).month != now.month):
                key = (str(now.month).zfill(2))+(str(now.year).zfill(4));
                winner = sorted(self.loto_inst.scoreboard.items(), key=lambda x: x[1], reverse=True);
                if winner:
                    winner = winner[0][0];
                    ret+="\n\U0001f389 \U0001f389 Le vainqueur du mois est ... {} \U0001f389 \U0001f389 !! Félicitations".format(winner.upper());
                else:
                    ret+="\nPas de vainqueur ce mois-ci !"
                self.flask_scoreboard_array[key] = copy.deepcopy(self.loto_inst.scoreboard);
                with open(self.flask_scoreboard, "wb") as pickle_file:
                    pickle.dump(self.flask_scoreboard_array, pickle_file);
                self.loto_inst.scoreboard = {};
            self.loto_inst.save_current_state();
            return ret;

    def exit(self):
        print("\tSauvegarde en cours ...")
        self.loto_inst.save_current_state();


if __name__ == "__main__":
    pass
