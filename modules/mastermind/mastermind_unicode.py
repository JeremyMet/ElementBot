class mastermind_unicode():

    emoticon_dico = {}
    emoticon_dico["r"] = "\U0001f534" ; # rouge,
    emoticon_dico["b"] = "\U0001f535" ; # bleu,
    emoticon_dico["j"] = "\U0001f7e1" ; # jaune,
    emoticon_dico["v"] = "\U0001f7e2" ; # vert,
    emoticon_dico["m"] = "\U0001f7e4" ; # marron,
    emoticon_dico["n"] = "\u26AB" ; # noir

    @classmethod
    def str_to_str(cls, str_proposition):
        ret = "";
        for elt in str_proposition:
            if elt in cls.emoticon_dico:
                ret+= cls.emoticon_dico[elt];
            else:
                ret+= elt;
        return ret;

    @classmethod
    def array_to_str(cls, array_proposition):
        ret = "("
        for elt in array_proposition:
            ret+= cls.emoticon_dico[elt];
            ret+=","
        ret=ret[:-1]+")"
        return ret;
