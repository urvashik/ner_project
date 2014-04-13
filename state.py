from document import Document
from helper import *
from os import listdir
import re
from os.path import isfile, join

class State :
    def __init__(self) :
        self.ne_types = set()
        self.corpus = []
        self.add_corpus("Raw")
        self.dictionaries = dict()

        self.rules = dict()

        #Find inconsistent rules
        self.candidate_rules = dict()

        self.init_dict("PER", "PER.txt")
        self.init_dict("ORG", "ORG.txt")
        self.init_dict("LOC", "LOC.txt")

    def get_type_and_score(self,rule) :
        if rule not in self.rules :
            return ("None", -1)
        maj_map = self.rules[rule]
        return (maj_map.get_type(), maj_map.get_majority())


    def init_dict(self, label, filepath) :
        dictionary = []
        self.ne_types.add(label)
        self.dictionaries[label] = dictionary

        f = open(filepath, "r")
        for line in f :
            ne = NamedEntity(line.strip(), 1.0)
            dictionary.append(ne)

    def add_corpus(self, filepath) :
        onlyfiles = [ f for f in listdir(filepath) if isfile(join(filepath,f)) ]
        for f in onlyfiles :
            self.corpus.append(Document(filepath+"/"+f))

    def get_corpus(self) :
        return self.corpus

    def get_ne_types(self) :
        return list(self.ne_types)

    def log_rules(self, ne_type, rules) :
        for rule in rules :
            if rule not in self.candidate_rules.keys() :
                self.candidate_rules[rule] = MajorityDict()
            self.candidate_rules[rule].insert(ne_type)

    def promote_rules(self, threshold, max_to_promote) :
        def sort_by_score(rules, score_dict) :
            return sorted(rules, \
                    key=lambda x:score_dict[x].get_majority(), reverse=True)

        def get_score(rule, score_dict) :
            return score_dict[rule].get_majority()

        def promote(rule_list) :
            for rule in rule_list :
                if rule in self.rules : 
                    self.rules[rule].merge(self.candidate_rules[rule])
                else :
                    self.rules[rule] = self.candidate_rules[rule]
            return rule_list

        rule_dict = self.candidate_rules
        rules = sort_by_score(rule_dict.keys(), rule_dict)
        rules = [r for r in rules if get_score(r, rule_dict) > threshold]
        return promote(rules[:max_to_promote])

    def match_b_rules(self, ne_type) :
        rule_list = self.b_rules[ne_type]
        for rule in rule_list :
            prefix = rule.prefix
            for doc in self.corpus :
                indicies = [m.start()+len(prefix) for m in re.finditer(prefix, doc.text)]
                indicies = [index for index in indicies \
                        if subword_filter(doc.text, index,prefix)]
                #print list(set([get_prev_word(doc.text, index) for index in indicies]))
                if len(indicies) > 0 :
                    print indicies
                

