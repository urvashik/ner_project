class Rule :
    def __init__(self, label, prefix, suffix) :
        self.label = label
        self.prefix = prefix if prefix != None else ""
        self.suffix = suffix if suffix != None else ""
        self.application = 0
        self.correct = 0
        self.wrong = 0

    def is_wrong(self) :
        self.wrong += 1
        self.application += 1

    def is_correct(self) :
        self.correct += 1
        self.application += 1

    def print_rule(self) :
        print self.prefix + "<"+self.label+">" + self.suffix

