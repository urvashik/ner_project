from os import listdir
from rule import Rule
import re
from os.path import isfile, join
from helper import *
class Document :
    def __init__(self, filepath) :
        f = open(filepath, "r")
        self.text = f.read()
        f.close()

    def find_rules(self,gazetteer, label) :
        count = 0
        b_rules, f_rules = [], []
        for ne in gazetteer :
            traverse = 0
            while traverse < len(self.text) :
                index = self.text.find(ne.name, traverse)
                if index < 0 :
                    traverse = len(self.text)
                    break
                traverse = index+ne.len
                if  str.isalnum(self.text[index-1]) or \
                        str.isalnum(self.text[index+ne.len]) :
                            continue
                next_word = get_next_word(self.text, index+ne.len)
                prev_word = get_prev_word(self.text, index)
                if len(prev_word) > 1 :
                    b_rules.append(Rule(label, prev_word, ""))
                if len(next_word) > 1 :
                    f_rules.append(Rule(label, "", next_word))
        return b_rules, f_rules



