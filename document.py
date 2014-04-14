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

    def find_rules(self,gazetteer) :
        count = 0
        rules = []
        for ne in gazetteer :
            traverse = 0
            while traverse < len(self.text) :
                index = self.text.find(ne, traverse)
                if index < 0 :
                    traverse = len(self.text)
                    break
                traverse = index+len(ne)
                if subword_filter(self.text, index, ne):
                    continue
                next_word = get_next_word(self.text, index+len(ne))
                prev_word = get_prev_word(self.text, index)
                if len(prev_word) > 1 :
                    rules.append((prev_word, ""))
                if len(next_word) > 1 :
                    rules.append(("", next_word))
        return rules



