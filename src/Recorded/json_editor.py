import json
import glob
files_path = glob.glob("*.json")
for f_name in files_path:
	with open(f_name,'r') as f:
		data = json.load(f)
		for i in data["shapes"]:
			if i["label"] == 'peanut':
				i["label"] = 'Peanut'
			elif i["label"] == 'walnut':
				i["label"] = 'Walnut'
			elif i["label"] == 'hazelnut':
				i["label"] = 'Haselnut'
	with open(f_name, 'w') as f:
	    json.dump(data, f, indent=2)
