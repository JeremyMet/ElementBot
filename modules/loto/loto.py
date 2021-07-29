import json;
import random;
import datetime;
from collections import namedtuple;
import os.path
import pickle

Draw_Time = namedtuple("Draw_Time", "hour minute");

class loto(object):

    pt_table = {} ;
    pt_table[0] = 0 ;
    pt_table[1] = 1 ;
    pt_table[2] = 5 ;
    pt_table[3] = 75 ;
    pt_table[4] = 3400 ;
    pt_table[5] = 800000 ;
    pt_table[6] = 10000000 ;

    def __init__(self, hour=0, minute=0, scoreboard_file="./modules/loto/scoreboard_file.dic", \
    dailybet_file="./modules/loto/dailybet_file.dic", log_file = "./modules/loto/log.dic", nb_numbers=49, combination_length=6):
        self.scoreboard_file = scoreboard_file;
        self.dailybet_file = dailybet_file;
        self.log_file = log_file;
        self.nb_numbers = nb_numbers;
        self.combination_length = combination_length;
        self.scoreboard = {} ;
        self.dailybet = {} ;
        # On initialise au jour précédent ; typiquement si on lance le script le 1er juin et que l'on souhaite un tirage à 22h
        # on initialise "le tirage précédent" (fictif, il n'a pas eu lieu) le 31 mai à 22h ; le module loto_bot.py (le "wrapper de cette classe")
        # vérifie toutes les secondes s'il y a eu 24h écoulés entre la date datetime.now() et la date du tirage précédent. Ainsi, même si l'on lance le script
        # à 21h45 un premier juin, en utilisant le tirage "fictif" (celui de 31 mai à 22h), nous aurons bien à tirage à 22h, le 1er juin.
        self.draw_time = Draw_Time(hour, minute);
        if os.path.isfile(self.log_file):
            with open(self.log_file, "rb") as pickle_file:
                self.log = pickle.load(pickle_file);
        else:
            tmp_datetime = datetime.datetime.now();
            self.log = {} ;
            self.log["last_draw"] = datetime.datetime(year=tmp_datetime.year, month = tmp_datetime.month, \
            day = tmp_datetime.day, hour = self.draw_time.hour, minute = self.draw_time.minute)-datetime.timedelta(days=1) ;
        self.load_previous_state();
        random.seed(datetime.datetime.now()); # Seed initialisation


    def set_scoreboard_file(self, scoreboard_file):
        self.scoreboard_file = scoreboard_file;

    def set_log_file(self, log_file):
        self.log_file = log_file;

    def set_dailybet_file(self, dailybet_file):
        self.dailybet_file = dailybet_file;

#    def set_draw_time(self, hour, minute):
#        self.draw_time = Draw_Time(hour, minute);


    def get_draw_time(self):
        return self.draw_time;

    def get_log(self):
        return self.log;

    def load_previous_state(self):
        if os.path.isfile(self.scoreboard_file):
            with open(self.scoreboard_file, "rb") as pickle_file:
                self.scoreboard = pickle.load(pickle_file);
        if os.path.isfile(self.dailybet_file):
            with open(self.dailybet_file, "rb") as pickle_file:
                self.dailybet = pickle.load(pickle_file);
        if os.path.isfile(self.log_file):
            with open(self.log_file, "rb") as pickle_file:
                self.log = pickle.load(pickle_file);

    def save_current_state(self):
            with open(self.scoreboard_file, "wb") as pickle_file:
                pickle.dump(self.scoreboard, pickle_file);
            with open(self.dailybet_file, "wb") as pickle_file:
                pickle.dump(self.dailybet, pickle_file);
            with open(self.log_file, "wb") as pickle_file:
                pickle.dump(self.log, pickle_file);


    def draw(self):
        self.current_result = set();
        while(len(self.current_result) < self.combination_length):
            rd = random.randint(1, self.nb_numbers);
            self.current_result.add(rd);
        tmp_datetime = datetime.datetime.now();
        self.log["last_draw"] = datetime.datetime(year=tmp_datetime.year, month = tmp_datetime.month, day = tmp_datetime.day, hour = self.draw_time.hour, minute = self.draw_time.minute) ;
        #self.current_result = {1,2,3,8,33,2}; # todo remove!

    def check_result(self):
        self.draw(); # tirage
        ret = "\U0001F3B2 Le tirage du {} est {}. \nBravo à".format(datetime.datetime.today().strftime('%d-%m-%Y'), self.current_result);
        is_there_a_winner = False;
        for key, value in self.dailybet.items():
            tmp_nb_pt = len(self.current_result & value);
            nb_pt = loto.pt_table[tmp_nb_pt];
            if nb_pt > 0:
                is_there_a_winner = True;
                ret += "\n\t- {} avec {} point(s) ({} nombre(s) correct(s))".format(key.capitalize(), nb_pt, tmp_nb_pt)
            if key in self.scoreboard.keys(): # on ajoute quand même les participants avec zero point.
                self.scoreboard[key] += nb_pt;
            else:
                self.scoreboard[key] = nb_pt;
        self.dailybet = {} ; # réinitialisation des paris ;)
        if is_there_a_winner:
            return ret;
        else:
            return "\U0001F3B2 Pas de vainqueurs aujourd'hui ({}) !\nLe tirage était le suivant : {}.".format(datetime.datetime.today().strftime('%d-%m-%Y'), self.current_result);

    def bet(self, sender, proposition):
        # check if proposition is well-formed
        proposition = proposition.replace(" ", "");
        if (proposition[0] != "(" or proposition[-1] != ")"):
            return "";
        proposition = proposition[1:-1];
        proposition_array = proposition.split(",");
        for i in proposition_array:
            if not(i.isnumeric()):
                return "" # On ne traite pas ce cas
        if (len(proposition_array) != self.combination_length):
            return "\U0001F3B2 La combinaison doit être de longueur {}.".format(self.combination_length);
        proposition_array = [(int(i) if (int(i) <= self.nb_numbers) else 0) for i in proposition_array];
        if (0 in proposition_array):
            return "\U0001F3B2 Les valeurs doivent être comprises entre 1 et {}.".format(self.nb_numbers);
        proposition_set = set(proposition_array);
        if (len(proposition_set) != self.combination_length):
            return "\U0001F3B2 Les propositions ne doivent pas contenir deux fois le même nombre."
        # proposition is well-formed,
        self.dailybet[sender] = proposition_set;
        return "\U0001F3B2 La proposition {} de {} a bien été prise en compte.".format(self.dailybet[sender], sender.capitalize());

    def get_dailybet(self):
        ret = "\U0001F3B2 Joueurs Participants - Grille";
        for key, value in self.dailybet.items():
            ret = "{}\n\t- {}: {} ".format(ret, key.capitalize(), value);
        return ret;

#todo mettre dans l'ordre croissant
    def get_scoreboard(self):
        medals_array = ["\U0001F947", "\U0001f948", "\U0001f949"] ;
        ret = "\U0001F3B2 Tableau des Scores :";
        cpt = 0 ;
        for key_value in sorted(self.scoreboard.items(), key=lambda x: x[1], reverse=True):
            ret = "{}\n\t- {}: {}".format(ret, key_value[0].capitalize(), key_value[1]);
            if cpt < 3:
                ret+= (" ({})".format(medals_array[cpt]));
            cpt+=1;
        return ret;
