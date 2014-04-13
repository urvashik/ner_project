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

        self.b_rules = dict()
        self.f_rules = dict()

        #Find inconsistent rules
        self.candidate_rule_b = dict()
        self.candidate_rule_f = dict()

        self.init_dict("PER", "PER.txt")
        self.init_dict("ORG", "ORG.txt")
        self.init_dict("LOC", "LOC.txt")


    def init_dict(self, label, filepath) :
        dictionary = []
        self.ne_types.add(label)
        self.dictionaries[label] = dictionary
        self.b_rules[label] = []
        self.f_rules[label] = []
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

    def log_rules(self, ne_type, b_rules, f_rules) :
        for rule in b_rules :
            prefix = rule.prefix
            if prefix not in self.candidate_rule_b.keys() :
                self.candidate_rule_b[prefix] = (MajorityDict(),rule)
            self.candidate_rule_b[prefix][0].insert(ne_type)

        for rule in f_rules :
            suffix = rule.suffix
            if suffix not in self.candidate_rule_f.keys() :
                self.candidate_rule_f[suffix] = (MajorityDict(),rule)
            self.candidate_rule_f[suffix][0].insert(ne_type)
    
    def promote_rules(self, threshold) :
        def promote(rule_dict, threshold) :
            promote_set = []
            for candidate in rule_dict.keys() :
                rule = rule_dict[candidate][1]
                rule.score = rule_dict[candidate][0].get_majority()
                if rule.score > threshold :
                    promote_set.append(rule)
            return promote_set

        rule_dict = self.candidate_rule_b
        b_rules = promote(rule_dict, threshold)
        for rule in b_rules :
            self.b_rules[rule.label].append(rule)

        rule_dict = self.candidate_rule_f
        f_rules = promote(rule_dict, threshold)
        for rule in f_rules :
            self.f_rules[rule.label].append(rule)


        return b_rules, f_rules

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
                

