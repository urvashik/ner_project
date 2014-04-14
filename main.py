from controller import Controller
NER = Controller()

for i in range(2): 
    print "-------------------Iteration:"+str(i)+"-------------------"
    NER.find_rules()
    promote_set = NER.promote_rules(0.7, 990)
    for rule in promote_set :
        print str(rule) +" " + str(NER.state.rules[rule].get_majority()) + " " + \
                str(NER.state.rules[rule].get_type())

    NER.find_ne()
    promote_set = NER.promote_ne(0.7, 999)
    for key in promote_set :
        m = NER.state.ne[key]
        print str(key) + "  " + str(m.get_type())+ " " + str(m.get_majority())
    NER.end_iteration()
