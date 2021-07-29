from modules.module import module ;
from bs4 import BeautifulSoup  ;
import urllib ;
import re ;


class wiktionary(module):

    def __init__(self, keyword = "wiktionary", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.help = "Modele to query wiktionary" ; # <- will be printed out by the admin module
        self.whatis = "A simple template !"
        self.__version__ = "0.0.1"


    # @module.login_check_dec # ignore when messages come from the bot itself.
                            # it can be useful to listen to what the bot says in some cases
    def process_msg_active(self, cmd, sender, room):
        # <-- Your code goes here.
        raw_args = cmd.split() ;
        if len(raw_args) == 3:
            word = raw_args[2] ;
            page = urllib.request.urlopen("https://fr.wiktionary.org/wiki/"+word).read() ;
            soup = BeautifulSoup(page, 'html.parser')
            tmp_list = soup.find_all("span", id = "Verbe")[0] ;
            ret = ""
            read = tmp_list.find_next("dl") ;
            while read:
                definition = re.findall("<i>.*</i>", str(read))[0] ;
                definition = definition.replace("<i>", "")
                definition = definition.replace("</i>", "")
                if definition and definition[-1] != ".":
                    definition += "." ;
                if definition :
                    ret+= "- "+definition+"\n" ;
                read = read.find_next("dl");
            return ret[:-1] ;
        return None ;

    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        pass

    @module.module_on_dec
    def run_on_clock(self):
        # <- Your code goes here.
        pass

    def exit(self):
        # <- Your code goes here.
        # This function is called when the bot is shut down,
        # this can for instance be used to save temporary variables into files.
        pass

