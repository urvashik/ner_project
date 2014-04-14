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
    
        #From all iteration
        self.ne = dict()
        #From last iteration
        self.ne_recent = dict()

        self.rules = dict()
        self.rules_recent = dict()

        #Find inconsistent rules
        self.candidate_rules = dict()
        self.candidate_ne = dict()

        self.init_dict("PER", "PER.txt")
        self.init_dict("ORG", "ORG.txt")
        self.init_dict("LOC", "LOC.txt")

    def get_type_and_score(self,rule) :
        if rule not in self.rules :
            return ("None", -1)
        maj_map = self.rules[rule]
        return (maj_map.get_type(), maj_map.get_majority())

    def init_dict(self, label, filepath) :
        f = open(filepath, "r")
        for line in f :
            name = line.strip()
            self.ne[name] = MajorityDict()
            # Put some large weight for the label since it's seed
            self.ne[name].insert(label, 99)
            self.ne_recent[name] = self.ne[name]

    def add_corpus(self, filepath) :
        onlyfiles = [ f for f in listdir(filepath) if isfile(join(filepath,f)) ]
        for f in onlyfiles :
            self.corpus.append(Document(filepath+"/"+f))

    def get_corpus(self) :
        return self.corpus

    def get_ne_types(self) :
        return list(self.ne_types)

    def log_rules(self, ne, rules) :
        ne_type = self.ne_recent[ne].get_type()
        ne_score = self.ne_recent[ne].get_majority()
        #print "ne type:"+ne_type + "score"+str(ne_score)
        for rule in rules :
            if rule not in self.candidate_rules.keys() :
                self.candidate_rules[rule] = MajorityDict()
            self.candidate_rules[rule].insert(ne_type)

    def promote_rules(self, threshold, max_to_promote) :
        def promote(rule_list) :
            self.rules_recent=dict()
            for rule in rule_list :
                if rule in self.rules : 
                    #Old rule don't help us find new NE. 
                    #However, we still update score based on new observation.
                    self.rules[rule].merge(self.candidate_rules[rule])
                else :
                    self.rules_recent[rule] = self.candidate_rules[rule]
                    self.rules[rule] = self.candidate_rules[rule]
            return rule_list

        rule_dict = self.candidate_rules
        rules = sort_by_score(rule_dict)
        rules = [r for r in rules if rule_dict[r].get_majority() > threshold]
        ret = promote(rules[:max_to_promote])
        self.candidate_rules = dict()
        return ret

    def promote_ne(self, threshold, max_to_promote) :
        def promote(ne_list) :
            self.ne_recent=dict()
            for name in ne_list :
                if name in self.ne :
                    self.ne[name].merge(self.candidate_ne[name])
                else :
                    self.ne_recent[name] = self.candidate_ne[name]
                    self.ne[name] = self.candidate_ne[name]
            return ne_list
        ne_dict = self.candidate_ne
        ne_list = sort_by_score(ne_dict)
        #for ne in ne_list :
        #    print "ne:"+ne+" score:"+str(ne_dict[ne].get_majority())
        ne_list = [ne for ne in ne_list if ne_dict[ne].get_majority() > threshold]
        ret = promote(ne_list[:max_to_promote])
        self.candidate_ne = dict()
        return ret


    def find_ne(self) :
        def insert_candidate_ne(ne, rule_type, rule_score) :
            if len(ne) == 0 :
                return
            if ne not in self.candidate_ne.keys() :
                self.candidate_ne[ne] = MajorityDict()
            self.candidate_ne[ne].insert(rule_type, rule_score)

        def distance_close(text, l_bound, r_bound) :
            if -1 == text[l_bound:r_bound].find('.') :
                return True
            return False
        def search_substring(text, query, traverse) :
            if query == "" :
                #Empty rule
                return traverse, traverse
            while traverse < len(text) :
                candidate_index = text.find(query, traverse)
                '''New traverse pointer should not point to same index
                as query to prevent infinite loop'''
                traverse = candidate_index+len(query)
                if candidate_index == -1 :
                    return -1, len(text)
                if subword_filter(text, candidate_index, query) : 
                    return candidate_index, traverse
            return -1, len(text)
        self.candidate_ne = dict()
        #You only find new NE from newly promoted rules
        rule_list = self.rules_recent
        for rule in rule_list :
            info = self.get_type_and_score(rule)
            rule_score, rule_type = info[1], info[0]
            for doc in self.corpus : 
                text = doc.text
                traverse = 0
                while traverse < len(text) :
                    l_bound, traverse= search_substring(text,rule[0],traverse)
                    if l_bound == -1 :
                        break
                    r_bound, traverse = search_substring(text,rule[1],traverse)
                    if r_bound == -1 :
                        traverse = len(text)
                        break
                    ''' If rule parts are too distance or different sentences, do
                    not count '''
                    if not distance_close(text, l_bound, r_bound) :
                        break
                    ''' If the rule only specifies previous token, seek forward
                    word. Otherwise, you find the wrong NE'''
                    if len(rule[1]) == 0:
                        ne = get_next_word(text, r_bound)
                    else :
                        ne = get_prev_word(text, r_bound)
                    insert_candidate_ne(ne, rule_type, rule_score)

