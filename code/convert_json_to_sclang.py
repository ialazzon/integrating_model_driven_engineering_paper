from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EClass
import sys
import json 

msg_counter = 0.0

rset = ResourceSet()
resource = rset.get_resource(URI('sclang.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('project_proposal_review.sclang'))
model_root = resource.contents[0]

the_contract = model_root.scontract[0]
elements = the_contract.element
# test_cases = the_contract.testcase

with open('claude.json', 'r') as file:
    json_test_cases= json.load(file)


participants = []
transactions = []
for e in elements:
	if e.__class__.__name__== 'Participant':
		participants.append(e)
	if e.__class__.__name__== 'Transaction':
		transactions.append(e)		

map_part = {}
map_transaction ={}
for p in participants:
	map_part[p.name] = p
for t in transactions:
	map_transaction[t.name] = t

TestCase = mm_root.getEClassifier('TestCase')
Authorization =mm_root.getEClassifier('Authorization')


for tc in json_test_cases:
	new_test_case = TestCase()
	new_test_case.name = tc["name"]
	new_test_case.accept = tc["accept"]
	new_test_case.transaction = map_transaction[tc["transaction"]]
	new_test_case.authorization.append(Authorization())
	for at in tc["authorizers"]:
		new_test_case.authorization[0].participant.append(map_part[at])
	the_contract.testcase.append(new_test_case)

resource.save()

