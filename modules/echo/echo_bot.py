from modules.module import module ;
from datetime import datetime;
import re
from collections import namedtuple;

class echo_bot(module):

    msgtype = namedtuple("msgtype", ["timestamp", "msg_array"]);
    allmsgtype = namedtuple("allmsgtype", ["roomset", "msg_array"]);


#    accentedChar = "àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ";
    filter_regex = re.compile("\(@filter:#[0-9aA-zZ\-]+:[0-9aA-zZ\-]+.[0-9aA-zZ]{1,5}\)");
    message_regex = re.compile("\[.+\]");

    @classmethod
    def get_filters(cls, msg):
        ret_filter_list = [];
        mt_iter = re.finditer(cls.filter_regex, msg);
        for mt in mt_iter:
            current_filter = mt.group(0);
            msg = msg.replace(current_filter, "");
            ret_filter_list.append(current_filter[9:-1]);
        return ret_filter_list, msg;

    @classmethod
    def get_message(cls, msg):
        extracted_msg = max(re.findall(cls.message_regex, msg), key=len);
        extracted_msg = extracted_msg[1:-1] ; # remove brackets
        return extracted_msg;

    def __init__(self, keyword = "echo"): # <- template ... Here goes your default module name
        super().__init__(keyword) ;
        self.help = "WIP" ; # <- will be printed out by the admin module
        self.whatis = "An Echo module. "
        self.module_name = "Echo Module"
        self.__version__ = "0.0.1"
        self.last_draw = datetime(year=1961, month=2, day=1);
        self.msg_dic = {}; # Used to store messages when filters are set.

    @module.module_on_dec
    @module.login_check_dec
    def process_msg_active(self, cmd, sender=None, room=None):
        message = echo_bot.get_message(cmd);
        if message: # if not empty
            filters, clear_msg = echo_bot.get_filters(message);
            if not(filters):
                filters = self.room_list;
            for filter in filters:
                if filter in self.msg_dic:
                    self.msg_dic[filter].msg_array.append(clear_msg);
                else:
                    now = datetime.now();
                    self.msg_dic[filter] = echo_bot.msgtype(timestamp=now, msg_array=[clear_msg]);
        return None;

    # @module.login_check_dec
    # TODO pour éviter de reboucler plusieurs fois sur la liste des événements (self.ret_array), éventuellement faire un dictionnaire qui stocke par "salon" le message de retour ?
    # Cons : ajout d'un dictionnaire, n'a un réel intérêt que pour les grosses structures.
    @module.module_on_dec
    @module.clock_dec
    @module.lock_dec
    def run_on_clock(self, room):
        ret = "";
        now = datetime.now();
        current_alias = room.current_alias;
        # For messages with filters
        if current_alias in self.msg_dic:
            for msg in self.msg_dic[current_alias].msg_array:
                ret+= (msg+"\n");
            del self.msg_dic[current_alias]
        # Garbage Collector;
        to_be_del = [];
        for key, value in self.msg_dic.items():
            if (now-value.timestamp).seconds > 300: # if no request from a room has been observed for 300 seconds, then remove the room from echo_bot dictionnary.
                to_be_del.append(key);
        for croom in to_be_del:
            del self.msg_dic[croom];
        return ret;

    def exit(self):
        pass
