from sys import argv
import math
script, training_file, test_file = argv

def run_classifier(training_file, test_file):
  with open (training_file) as tfile:
  		total_yes = 0
  		total_no = 0


  		######### BUILD CLASSIFIER ##########

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


		############ TEST CLASSIFIER ############

		## Evaluate Classifier with Training Data File ##

		tr_true_pos = 0
		tr_false_neg = 0
		tr_false_pos = 0
		tr_true_neg = 0
		tr_hit_rate = 0.0

		for n in range(len(rows)):
			r = rows[n]
			formatted = [(int(r[i].split(':')[0]), int(r[i].split(':')[1])) for i in range(1, len(r))]
			expected = int(r[0])
			result = get_complete_decision(total_yes, total_no, formatted, totals, stds)
			if(result == expected):
				tr_hit_rate = tr_hit_rate + 1
				if(expected == 1):
					tr_true_pos = tr_true_pos + 1
				else:
					tr_true_neg = tr_true_neg + 1
			else:
				if(expected == 1):
					tr_false_neg = tr_false_neg + 1
				else:
					tr_false_pos = tr_false_pos + 1


		tr_hit_rate = tr_hit_rate/len(rows)
		print("Training Success Rate : {0}%").format(int(100*tr_hit_rate), "%")
		print("{0} {1} {2} {3}").format(tr_true_pos, tr_false_neg, tr_false_pos, tr_true_neg)


		
		## Evaluate Classifier with Test Data File ##

		test_true_pos = 0
		test_false_neg = 0
		test_false_pos = 0
		test_true_neg = 0
		test_hit_rate = 0.0
		with open (test_file) as testfile:

			test_rows = [r.split(' ') for r in testfile.readlines()]
			test_hit_rate = 0.0

			for n in range(len(test_rows)):
				r = test_rows[n]
				formatted = [(int(r[i].split(':')[0]), int(r[i].split(':')[1])) for i in range(1, len(r))]
				expected = int(r[0])
				result = get_complete_decision(total_yes, total_no, formatted, totals, stds)
				if(result == expected):
					test_hit_rate = test_hit_rate + 1
					if(expected == 1):
						test_true_pos = test_true_pos + 1
					else:
						test_true_neg = test_true_neg + 1
				else:
					if(expected == 1):
						test_false_neg = test_false_neg + 1
					else:
						test_false_pos = test_false_pos + 1


			test_hit_rate = test_hit_rate/len(test_rows)
			print("Test Success Rate : {0}%").format(int(100*test_hit_rate), "%")
			print("{0} {1} {2} {3}").format(test_true_pos, test_false_neg, test_false_pos, test_true_neg)


# get complete decision
# data = [(attr_num, attr_val)...]
def get_complete_decision(total_yes, total_no, data, totals, stds):


	p_yes = float(total_yes)/(total_yes + total_no)
	p_no = float(total_no)/(total_yes + total_no)

	p_xs_given_yes = 1.0
	p_xs_given_no = 1.0

	p_yes_xs = 1.0
	p_no_xs = 1.0

	s_yes = 0
	s_no = 0

	for d in data:
		p_xi_yes = single_attr_prob(1, d[0], d[1], totals, total_yes, total_no, stds)
		p_xi_no = single_attr_prob(-1, d[0], d[1], totals, total_yes, total_no, stds)
		
		s_yes = s_yes + p_xi_yes
		s_no = s_no + p_xi_no

		p_xs_given_yes = p_xs_given_yes * p_xi_yes
		p_xs_given_no = p_xs_given_no * p_xi_no

		p_yes_xi = 1.0
		if(d[0] in totals[1].keys()):
			p_yes_xi = float(totals[1][d[0]][0])/(total_yes)
		p_yes_xs = p_yes_xs * p_yes_xi


		p_no_xi = 1.0
		if(d[0] in totals[-1].keys()):
			p_no_xi = float(totals[-1][d[0]][0])/(total_no)
		p_no_xs = p_no_xs * p_no_xi

	s_yes = s_yes/len(data)
	s_no = s_no/len(data)

	prob_yes = (p_yes * p_xs_given_yes/p_yes_xs)
	prob_no = (p_no * p_xs_given_no/p_no_xs)
	
	if(prob_yes > prob_no):
		return 1
	else:
		return -1

# get P(x = v|Y) -> x = attr_num, v = attr_val, Y = class_num 
def single_attr_prob(class_num, attr_num, attr_val, totals, total_yes, total_no, stds):
	if(stds[1][1] != 0.0):
		my_std = float(stds[class_num][attr_num])
		my_mean = float(totals[class_num][attr_num][1])/totals[class_num][attr_num][0]
	
		return (1/((2*math.pi*(my_std**2))**(0.5))) * math.exp(-1*((attr_val - my_mean)**2)/(2*(my_std**2)))

	my_occurance = 0
	if(attr_num in totals[class_num].keys()):
		my_occurance = totals[class_num][attr_num][1]
	if(class_num == 1):
		return my_occurance/(float(total_yes))
	if(class_num == -1):
		return my_occurance/(float(total_no))
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
			stds[class_num][k] = (float(stds[class_num][k])/totals[class_num][k][0])**(.5)	
	return stds

run_classifier(training_file, test_file)
