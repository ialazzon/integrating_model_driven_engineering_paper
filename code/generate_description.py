from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EClass
import sys
import json
from num2words import num2words


rset = ResourceSet()
resource = rset.get_resource(URI('sclang.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('project_proposal_review.sclang'))
model_root = resource.contents[0]

the_contract = model_root.scontract[0]
elements = the_contract.element


def pluralize_noun(n, s):
    if n == 1:
        return f"{s}"
    else:
        return f"{s}s"

description = ""

participants = []
part_names = []
for e in elements:
    if e.__class__.__name__== 'Participant':
        participants.append(e)
        part_names.append(e.name)

description += f"There are {num2words(len(participants))} {pluralize_noun(len(participants), 'participant')}: "
description += f", ".join(part_names)
description += "\n"

transactions = []
tran_names = []
for e in elements:
    if e.__class__.__name__== 'Transaction':
        transactions.append(e)
        tran_names.append(e.name)
        
description += f"There are {num2words(len(transactions))} {pluralize_noun(len(transactions), 'transaction')}: "
description += f", ".join(tran_names)
description += "\n"


roles = []
role_names = []
for e in elements:
    if e.__class__.__name__== 'Role':
        roles.append(e)
        role_names.append(e.name)
        
description += f"There are {num2words(len(roles))} {pluralize_noun(len(roles), 'role')}: "
description += f", ".join(role_names)
description += "\n"

for r in roles:
    description += f"Members in role {r.name} are: "
    parts = r.participant
    parts_names = []
    for p in parts:
        parts_names.append(p.name)
    description += f", ".join(parts_names)
    description += "\n"
    
ors =[]
for e in elements:
    if e.__class__.__name__== 'OR':
        ors.append(e)
        
def describe_an_or(an_or, t):
    parts = an_or.dis_element
    dis = []
    for p in parts:
        dis.append(p.name)
    for r in roles:
         rels = r.relationship
         for rel in rels:
              if rel.__class__.__name__== 'RoleRel' and rel.to == an_or:
                   dis.append(f"{num2words(rel.min_num_members)} {pluralize_noun(rel.min_num_members, 'member')} in role {r.name}")   
    return f" or ".join(dis)
	

        
description += "\nThe following are the transactions' authorization requirements:\n"
for t in transactions:
    description += f"For {t.name}, the following are the authorization requirements:\n"
    counter = 1
    # TranRel from participants to transactions
    for p in participants:
        rels = p.relationship
        for rel in rels:
            if rel.__class__.__name__== 'TranRel' and rel.to == t:
                description += f"{counter}- It must be authorized by {p.name}.\n"
                counter +=1
                
	# RoleRel from roles to transactions
    for r in roles:
         rels = r.relationship
         for rel in rels:
            if rel.__class__.__name__== 'RoleRel' and rel.to == t:
                description += f"{counter}- It must be authorized by {num2words(rel.min_num_members)} {pluralize_noun(rel.min_num_members, 'member')} in role {r.name}.\n"
                counter +=1
                
	# OR
    for an_or in ors:
        if an_or.transaction == t:
            description +=  f"{counter}- It must be authorized by " + describe_an_or(an_or, t) + "\n"
            
    description += "\nAll requirements must be met.\n\n"

print(description)


