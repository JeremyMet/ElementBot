import random;
from .mastermind_unicode import mastermind_unicode


class mastermind(object):

    def __init__(self, combination_length=4, max_tries=6):
        self.combination_length = combination_length;
        self.max_tries = max_tries;
        self.combination = ['r' for _ in range(combination_length)];
        self.str_game_state = "";
        self.current_nb_tries = 0;
        self.rst();


    def rst(self):
        self.str_game_state = "\u2699\uFE0F <b>Mastermind</b> \u2699\uFE0F \n Nombre d'Essais: {} ; \n".format(self.max_tries);
        self.combination = [random.choice(list(mastermind_unicode.emoticon_dico.keys())) for _ in range(self.combination_length)];
        self.current_nb_tries = 0;

    # if NOK, returns an empty array.
    def check_proposition_consistency(self, str_solution):
        array_proposition = [];
        ## Check Solution Consistency
        str_solution = str_solution.replace(" ", "");
        if str_solution[0] == "(" and str_solution[-1] == ")":
            str_solution = str_solution[1:-1] # remove brackets
            array_proposition = str_solution.split(",");
            if len(array_proposition) == self.combination_length:
                for elmt in array_proposition:
                    if not(elmt in mastermind_unicode.emoticon_dico):
                        array_proposition = [] ;
                        break;
            else:
                array_proposition = [] ;
        return array_proposition;

    # Takes as Input "array_proposition"
    def compare_proposition_with_solution(self, array_proposition):
        right_pos = 0;
        right_col = 0;
        combination = self.combination.copy();
        for i in range(self.combination_length):
            if array_proposition[i] == combination[i]:
                right_pos +=1 ;
                combination[i], array_proposition[i] = -1, -1;
        for i in range(self.combination_length):
            if array_proposition[i] != -1:
                if array_proposition[i] in combination:
                    right_col +=1 ;
                    indx = combination.index(array_proposition[i]);
                    combination[indx] = -1;
        return (right_pos, right_col);


    def propose(self, str_proposition):
        ret = "";
        str_proposition = str_proposition.replace(" ", "");
        array_proposition = self.check_proposition_consistency(str_proposition);
        if array_proposition:
            (right_pos, right_col) = self.compare_proposition_with_solution(array_proposition);
            self.str_game_state += str(self.current_nb_tries) +". " + mastermind_unicode.str_to_str(str_proposition) + " \u2192 " +right_pos*'\u2705'+right_col*'\u2611\uFE0F' + (self.combination_length-right_col-right_pos)*'\u274C'+'\n'
            self.current_nb_tries += 1;
            if right_pos == self.combination_length:
                ret = "Bravo \U0001f973 ! Vous avez gagné, il s'agissait effectivement de la combinaison {} !".format(mastermind_unicode.str_to_str(str_proposition));
                self.rst();
            else:
                if self.current_nb_tries == self.max_tries:
                    ret = "Oh non \U0001f625 ! Vous avez manqué de perspicacité ! ... La combinaison recherchée était {}.".format(mastermind_unicode.array_to_str(self.combination));
                    self.rst();
                else:
                    ret = self.str_game_state[:-1];
        return ret;



if __name__ == "__main__":
    mastermind_inst = mastermind();
    mastermind_inst.combination = [0,1,1,2];
    while(True):
        proposition = input();
        cmp = mastermind_inst.propose(proposition);
        print(cmp);
