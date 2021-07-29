import random ;
from modules.module import module ;

class greeting(module):

    greeting_array = ["salut", "coucou", "hello", "hola", "demat", "pouet", "pwet"] ;
    tbot_array = ["tbot", "tersabot", "tersa_bot", "bot"] ;
    tbot_random_sentences = \
    ["Non non non et non ! La Shinra produit de l'énergie PROPRE !", \
     "Bientôt des vaccins d'Umbrella !!", \
     "Un jour, j'ai reçu une flèche dans le genou ... !" \
     ]

    def __init__(self, keyword = "greeting"): # <- template ... Here goes your default module name
        super().__init__(keyword) ;
        self.help = "Say \"hello tbot\"." ; # <- will be printed out by the admin module
        self.whatis = "A simple hello module. "
        self.__version__ = "0.0.1"

    @module.module_on_dec
    def run(self, cmd, sender=None, room = None):
        cmd = cmd.lower() ;
        cmd_array = cmd.split(" ")
        if len(cmd_array) == 2:
            if cmd_array[0] in greeting.greeting_array and cmd_array[1] in greeting.tbot_array:
                return random.choice(greeting.greeting_array).capitalize()+" "+sender.capitalize()+" \o/" ;

    @module.module_on_dec
    # @module.clock_dec
    def run_on_clock(self):
        if self.get_timer() > 36000:
            self.reset_clock() ;
            return random.choice(greeting.tbot_random_sentences) ;
        else:
            return None ;




if __name__ == "__main__":

    greet = greeting() ;
    print(greet.run("salut tbot", "Tersaken")) ;
