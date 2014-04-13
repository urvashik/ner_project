from state import State

class Controller :
    def __init__(self) :
        self.state = State()

    def get_ne_types(self) :
        return self.state.get_ne_types()

    def find_rules(self, ne_type) :
        dictionary = self.state.dictionaries[ne_type]
        rules = []
        for doc in self.state.corpus :
            rules_i = doc.find_rules(dictionary)
            if len(rules_i) > 0 :
                rules.extend(rules_i)
        self.state.log_rules(ne_type, rules)
    
    def promote_rules(self, threshold, max) :
        return self.state.promote_rules(threshold, max)

    def find_ne(self, ne_type) :
        self.state.match_b_rules(ne_type)
        #self.state.match_f_rules(ne_type)
