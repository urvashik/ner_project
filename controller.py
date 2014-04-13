from state import State

class Controller :
    def __init__(self) :
        self.state = State()

    def get_ne_types(self) :
        return self.state.get_ne_types()

    def find_rules(self, ne_type) :
        dictionary = self.state.dictionaries[ne_type]
        b_rules, f_rules = [], []
        for doc in self.state.corpus :
            b_rules_i, f_rules_i = doc.find_rules(dictionary, ne_type)
            if len(b_rules_i) > 0 :
                b_rules.extend(b_rules_i)
            if len(f_rules_i) > 0 :
                f_rules.extend(f_rules_i)
        self.state.log_rules(ne_type, b_rules, f_rules)
    
    def promote_rules(self, threshold) :
        return self.state.promote_rules(threshold)

    def find_ne(self, ne_type) :
        self.state.match_b_rules(ne_type)
        #self.state.match_f_rules(ne_type)
