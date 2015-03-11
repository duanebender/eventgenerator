import json
from pprint import pprint
from attribute import Attribute

# This class provides the utility to load behaviour pattern definitions 
# from json file "patterns.json".
#

class Pattern():
	patterns = {}
	dict_attr = {}
	
	def __init__(self, dict):
		self.dict_attr = dict
		
	def load(self):
		# load pattern definition file
		json_data=open('input/patterns.json')
		data = json.load(json_data)
		#pprint(data)
		json_data.close()
		
		for entity in data:
			itemset = []
			sequence = []
			time = {}
			if "actor" in entity:
				for key, value in entity["actor"].iteritems():
					itemset.append(self.dict_attr[value])
					
			if "context" in entity:
				for key, value in entity["context"].iteritems():
					itemset.append(self.dict_attr[value])
					
			if "sequence" in entity:
				for item in entity["sequence"]:
					oneset = []
					for key, value in item.iteritems():
						oneset.append(self.dict_attr[value])
					sequence.append(oneset)
					
			if "time" in entity:
				time = entity["time"]
					
			self.patterns[entity["id"]] = {}
			self.patterns[entity["id"]]["itemset"] = itemset
			self.patterns[entity["id"]]["sequence"] = sequence
			self.patterns[entity["id"]]["time"] = time
		
if __name__ == '__main__':
	attribute = Attribute()
	attribute.load_dist_json()
	attribute.load_attr_cvs()
	
	pattern = Pattern(attribute.sem_to_rep)
	pattern.load()
	print pattern.patterns