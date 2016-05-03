from sys import argv
import math
script, training_file, test_file = argv

def run_classifier(training_file, test_file):
  with open (training_file) as tfile:
  		total_yes = 0
  		total_no = 0
  		## BUILD CLASSIFIER ##

		rows = [r.split(' ') for r in tfile.readlines()]
		summary = {1:[], -1:[]}
		
		# form formatted summary by class
		for n in range(len(rows)):
			r = rows[n]
			formatted = [(int(r[i].split(':')[0]), int(r[i].split(':')[1])) for i in range(1, len(r))]
			summary[int(r[0])].append(formatted)
			if(int(r[0]) == 1):
				total_yes = total_yes + 1
			else:
				total_no = total_no + 1
		
		# {1 : { 7: [occurences, total value] .. }, -1: {} }
		totals = get_totals(summary)

		# {1 : { 5: <std> ..} ,  -1: {..} }
		stds = get_stds(summary, totals)


		## TEST CLASSIFIER ##
		print(totals[1][1])
		print(totals[-1][1])
		print(" row : ", summary[1][1])
		
		yes_hitrate = 0.0
		no_hitrate= 0.0
		for i in range(10):
			if(1 == get_complete_decision(total_yes, total_no, summary[1][i], totals, stds )):
				print("True")
				yes_hitrate = yes_hitrate + 1
			else:
				print("False")

		for j in range(10):
			if(-1 == get_complete_decision(total_yes, total_no, summary[-1][j], totals, stds )):
				print("True")
				no_hitrate = no_hitrate + 1
			else:
				print("False")
		yes_hitrate = yes_hitrate/10
		no_hitrate = no_hitrate/10

		print(yes_hitrate)
		print(no_hitrate)

# get complete decision
# data = [(attr_num, attr_val)...]
def get_complete_decision(total_yes, total_no, data, totals, stds):


	p_yes = float(total_yes)/(total_yes + total_no)
	p_no = float(total_no)/(total_yes + total_no)

	p_xs_given_yes = 1.0
	p_xs_given_no = 1.0

	p_yes_xs = 1.0
	p_no_xs = 1.0

	min_yes = 100000
	min_no = 100000
	for d in data:
		p_xi_yes = single_attr_prob(1, d[0], d[1], totals, stds)
		p_xi_no = single_attr_prob(-1, d[0], d[1], totals, stds)

		p_xs_given_yes = p_xs_given_yes * p_xi_yes
		p_xs_given_no = p_xs_given_no * p_xi_no

		p_yes_xi = float(totals[1][d[0]][0])/(total_yes)
		p_yes_xs = p_yes_xs * p_yes_xi


		p_no_xi = float(totals[-1][d[0]][0])/(total_no)
		p_no_xs = p_no_xs * p_no_xi

	# 	if(totals[1][d[0]][0] < min_yes):
	# 		min_yes = totals[1][d[0]][0]

	# 	if(totals[-1][d[0]][0] < min_no):
	# 		min_no = totals[-11][d[0]][0]	

	# p_yes_xs = min_yes/(total_yes)
	# p_no_xs = min_no/(total_no)

	# print("prob yes  : {0}, {1}, {2}").format(p_yes, p_xs_given_yes, p_yes_xs)
	# print("prob no  : {0}, {1}, {2}").format(p_no, p_xs_given_no, p_no_xs)
	prob_yes = (p_yes * p_xs_given_yes)
	prob_no = (p_no * p_xs_given_no)

	print("prob_yes", prob_yes )
	print("prob_no", prob_no )
	
	if(prob_yes > prob_no):
		return 1
	else:
		return -1

# get P(x = v|Y) -> x = attr_num, v = attr_val, Y = class_num 
def single_attr_prob(class_num, attr_num, attr_val, totals, stds):
	my_std = float(stds[class_num][attr_num])
	my_mean = float(totals[class_num][attr_num][1])/totals[class_num][attr_num][0]
	
	return (1/((2*math.pi*(my_std**2))**(0.5))) * math.exp(-1*((attr_val - my_mean)**2)/(2*(my_std**2)))

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
			print(k, ": " ,stds[class_num][k], " ", totals[class_num][k])
			stds[class_num][k] = (float(stds[class_num][k])/totals[class_num][k][0])**(.5)	

	return stds

run_classifier(training_file, test_file)
