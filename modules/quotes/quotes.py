from modules.module import module ;
import datetime ;
import json ;
import random ;
from collections import namedtuple;
import pickle;
import os ;

Draw_Time = namedtuple("Draw_Time", "hour minute");

class quotes(module):

    def __init__(self, keyword = "quotes", hour = 0, minute = 0, log_path = "./modules/quotes/log.dic", is_permanent = False):
        super().__init__(keyword, is_permanent) ;
        self.keywords = ["quotes"] ; # <- Name of your module
        self.help = "A quote module" ; # <- will be printed out by the admin module
        self.module_name = "Quote Module"
        self.whatis = "A simple quote module !"
        self.__version__ = "0.0.2";
        self.draw_time = Draw_Time(hour, minute);
        # Check previous (...)
        self.log_path = log_path ;
        if os.path.isfile(self.log_path):
            with open(self.log_path, "rb") as pickle_file:
                self.log = pickle.load(pickle_file);
        else:
            self.log = {};
            tmp_datetime = datetime.datetime.now();
            self.log["last_draw"] = datetime.datetime(year=tmp_datetime.year, month = tmp_datetime.month, \
            day = tmp_datetime.day, hour = self.draw_time.hour, minute = self.draw_time.minute)-datetime.timedelta(days=1) ;
        # Load the quotes file
        try:
            with open("modules/quotes/stupidstuff_clean.json", "r") as f:
                self.quotes = json.loads(f.read()) ;
        except IOError:
            raise("Could not load the quotes file \"quote.json\"") ;
        # Refresh the ret string
        self.refresh();


    def refresh(self):
        current_time = datetime.datetime.now();
        current_time_str = datetime.date(current_time.year, current_time.month, current_time.day).isoformat() ;
        # current_quote_index = (current_time.day+current_time.month*30+current_time.year*365)%len(self.quotes) ;
        current_quote_index_tmp = datetime.datetime.now()-datetime.datetime(1961, 2,1);        
        current_quote_index = (current_quote_index_tmp.days)%len(self.quotes);
        self.current_quote = self.quotes[current_quote_index] ;
        self.ret = "<b>~~~ \U0001f921 Today's Joke (" +  current_time_str +") ~~~</b>\n" \
               +self.current_quote["body"] +'\n'+'\t'*10+ "Category: <i>"+self.current_quote["category"]+"</i>" ;

    @module.module_on_dec
    @module.login_check_dec
    def process_msg_active(self, cmd, sender=None, room=None):
        return self.ret;

    @module.module_on_dec
    def run_on_clock(self, room=None):
        current_time = datetime.datetime.now() ;
        delta = current_time-self.log["last_draw"];
        if (delta.days > 0):
            self.log["last_draw"] = datetime.datetime(year=current_time.year, month = current_time.month, \
            day = current_time.day, hour = self.draw_time.hour, minute = self.draw_time.minute) ;
            try:
                with open(self.log_path, "wb") as pickle_file:
                    pickle.dump(self.log, pickle_file);
            except IOError:
                print("Can not write in {}.".format(self.log_path));
            self.refresh();
            return self.ret ;
