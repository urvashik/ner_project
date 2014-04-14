from controller import Controller
NER = Controller()

#for i in range(30): Iterate
for ne_type in NER.get_ne_types() :
    NER.find_rules(ne_type)
promote_set = NER.promote_rules(0.7, 99)

for ne_type in NER.get_ne_types() :
    NER.find_ne()
#for key in NER.state.candidate_ne.keys():
#    print NER.state.candidate_ne[key].get_majority()
promote_set = NER.promote_ne(0.7,99)
#print promote_set
#for key in promote_set :
#    print NER.state.ne[key].get_majority()
