def print_log(promote_set,dic) :
    for item in promote_set :
        print str(item) +" purity:" + str(dic[item].get_majority())+ " type :" + \
                str(dic[item].get_type())

from controller import Controller
NER = Controller()

#Specify number of iterations
for i in range(10): 
    print "-------------------Iteration:"+str(i)+"-------------------"

    NER.find_rules()
    promote_set = NER.promote_rules(0.6, 9) #Args : threshold [0,1], max promotions
    print_log(promote_set, NER.state.rules)

    NER.find_ne()
    promote_set = NER.promote_ne(0.6, 9)
    print_log(promote_set, NER.state.ne)

    NER.end_iteration()
