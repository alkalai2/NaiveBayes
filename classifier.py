from sys import argv
import math
script, training_file, test_file = argv

def build_classifier(training_file):
  with open (training_file) as tfile:
		rows = [r.split(' ') for r in tfile.readlines()]
		summary = {1:[], -1:[]}
		
		# form formatted summary by class
		for n in range(len(rows)):
			r = rows[n]
			formatted = [(int(r[i].split(':')[0]), int(r[i].split(':')[1])) for i in range(1, len(r))]
			summary[int(r[0])].append(formatted)
		
		# {1 : { 7: [occurences, total value] .. }, -1: {} }
		totals = get_totals(summary)

		# {1 : { 5: <std> ..} ,  -1: {..} }
		stds = get_stds(summary, totals)

				



# get P(x = v|Y) -> x = attr_num, v = attr_val, Y = class_num 
def single_attr_prob(class_num, attr_num, attr_val, totals, stds):
	my_std = stds[class_num][attr_num]
	my_mean = totals[class_num][attr_num][1]/totals[class_num][attr_num][0]
	
	return (1/((2*math.pi*(my_std**2))**(0.5))) * math.exp(-1*((attr_value - my_mean)**2)/(2*(my_std**2)))

def get_totals(summary):
	totals = {1:{}, -1:{}}
	for class_num in (1, -1):
		for row in summary[class_num]:
			for s in row:
				attr_num = s[0]
				attr_value = s[1]
				if(attr_num in totals[class_num].keys()):
					totals[class_num][attr_num] = [totals[class_num][attr_num][0] + 1,  totals[class_num][attr_num][1] + attr_value]
				else:
					totals[class_num][attr_num] = [1, attr_value]
	
	return totals	
def get_stds(summary, totals):
	stds = {1: {}, -1:{}}
	for class_num in (1, -1):
		for row in summary[class_num]:
			for s in row:
				attr_num = s[0]
				attr_value = s[1]
				mean = totals[class_num][attr_num][1] / totals[class_num][attr_num][0]
				diff = (attr_value - mean)**2
				if(attr_num in stds[class_num].keys()):
					stds[class_num][attr_num] = stds[class_num][attr_num] + diff
				else:
					stds[class_num][attr_num] = diff
	for class_num in (1, -1):
		for k in stds[class_num].keys():
			print(k, ", " ,stds[class_num][k], " ", totals[class_num][k])
			stds[class_num][k] = (float(stds[class_num][k])/totals[class_num][k][0])**(.5)	

	return stds

build_classifier(training_file)
