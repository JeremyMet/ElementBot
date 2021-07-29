

class pendu_modifier(object):


    def __init__(self, event_path):
        with open(event_path, 'r') as f:
            self.events = json.load(f) ;
        old_weight = 0 ;
        new_weight = 0 ;
        for key in self.events.keys():
            old_weight = new_weight ;
            new_weight = old_weight+self.events[key]["weight"] ;
            self.events[key]["proba_range"] = (old_weight, new_weight) ;
        self.events_total_weight = new_weight ;


    def modifier(self, pendu_inst, prob_event=50):
        # prob_event in percentage.
        dice_event_trigger = random.randint(1,100) ;
        if dice_event_trigger < prob_event:
            return None ;
        dice_event_choice = random.randint(0, self.events_total_weight-1) ;
        for event in self.events.values():
            range = event["proba_range"] ;
            if range[0] <= dice_event_choice < range[1]:
                self.str_event = "\u26A0\uFE0F EVENT : "+str(event["message"])+"\n \n" ;
                self.life_max = constant_life_max+event["bonus_life"] ;
                self.life = constant_life_max+event["bonus_life"] ;
                self.mirror = True if event["mirror"] == "yes" else False ;
                self.min_lg = event["min_lg"] ;
                self.max_lg = event["max_lg"] ;
                break ;
