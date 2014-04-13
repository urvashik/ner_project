from controller import Controller
NER = Controller()
print NER.state.get_corpus()
print NER.state.dictionaries


#for i in range(30): Iterate
for ne_type in NER.get_ne_types() :
    #Find a rule, note the type
    NER.find_rules(ne_type)
    b_rules, f_rules = NER.promote_rules(0.7)
    for rule in b_rules :
        rule.print_rule()

#for ne_type in NER.get_ne_types() :
    #Use rules to find NE
#    NER.find_ne(ne_type)
    #b_rules, f_rules = NER.promote_rules(0.7)

