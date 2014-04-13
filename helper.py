def get_next_word(text, index) :
    buf = []
    #Stop if no following word
    if index+1 >= len(text) or text[index+1] == '.' :
        return ""
    index += 1
    while index < len(text) and str.isalnum(text[index]) :
        buf.append(str(text[index]))
        index += 1
    return "".join(buf)

def get_prev_word(text, index) :
    buf = []
    #Stop if no previous words
    if text[index-1] == '.' :
        return ""
    index -= 2
    while index > 0 and str.isalnum(text[index]) :
        buf.insert(0, str(text[index]))
        index -= 1
    return "".join(buf)


class NamedEntity :
    def __init__(self, name, score) :
        self.name = str(name)
        self.score = float(score)
        self.len = len(self.name)

class MajorityDict :
    def __init__(self) :
        self.dictionary = dict()
        self.max = (-1, None)
        self.total = 0.0

    def insert(self, key, value=1) :
        if key not in self.dictionary.keys() :
            self.dictionary[key] = value
            val = 1
        else :
            self.dictionary[key] += value
            val = self.dictionary[key]
        if val > self.max[0] :
            self.max = (val, key)
        self.total += 1.0

    def merge(self, other) :
        for key in other.dictionary.keys() :
            self.insert(key, other[key])

    def get_majority(self) :
        return self.max[0]/self.total
    def get_type(self) :
        return self.max[1]

def subword_filter(text, index, word) :
    print word
    print text[index-1 : index+len(word)+2]
    if  str.isalnum(text[index-1]) or str.isalnum(text[index+len(word)]) :
        return False
    return True

