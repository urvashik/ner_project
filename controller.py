from state import State

class Controller :
    def __init__(self) :
        self.state = State()

    #Can define halting condition based on extraction count
    def get_ne_types(self) :
        return self.state.get_ne_types()

    def find_rules(self) :
        for ne in self.state.ne_recent.keys() :
            rules = []
            for doc in self.state.corpus :
                rules_i = doc.find_rules([ne])
                if len(rules_i) > 0 :
                    rules.extend(rules_i)
            self.state.log_rules(ne, rules)
    
    def promote_rules(self, threshold, max) :
        return self.state.promote_rules(threshold, max)

    def promote_ne(self, threshold, max) :
        return self.state.promote_ne(threshold, max)

    def find_ne(self):
        #print self.state.rules_recent
        self.state.find_ne()
    
    #Reset candidates for next iteration.
    def end_iteration(self) :
        self.state.candidate_rules = dict()
        self.state.candidate_ne = dict()
