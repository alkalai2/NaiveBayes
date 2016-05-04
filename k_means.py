import math

def run_kmeans():
	data = [(1.0, 1.0), (1.5,2.0), (2.5,5.5), (6.0,5.0), (4.0,5.0), (4.5,5.0), (3.5,5.0), (5.0,1.0), (6.0,1.0)]
	labels = ["none"]*10

	seed_red 	= (4.0,5.0)
	seed_green 	= (3.5,4.5)
	seed_blue 	= (6.0, 5.0)

	for r in range(1,10):
		print("\n iteration %d" % r)
		print("seeds: " + str((seed_red, seed_green, seed_blue)))
		for i, d in enumerate(data):
			x = d[0]
			y = d[1]

			dist_red = ((d[0] - seed_red[0]) ** 2 + (d[1] - seed_red[1]) ** 2)**(0.5)
			dist_green = ((d[0] - seed_green[0]) ** 2 + (d[1] - seed_green[1]) ** 2)**(0.5)
			dist_blue = ((d[0] - seed_blue[0]) ** 2 + (d[1] - seed_blue[1]) ** 2)**(0.5)

			if(min([dist_red, dist_green, dist_blue]) == dist_red):
				labels[i] = "red"
			if(min([dist_red, dist_green, dist_blue]) == dist_green):
				labels[i] = "green"
			if(min([dist_red, dist_green, dist_blue]) == dist_blue):
				labels[i] = "blue"

			print("{0}: \t {1}").format(d, labels[i])
			
			# set new centers of clusters
		(seed_red, seed_green, seed_blue) = get_centers(data, labels)

def get_centers(data, labels):
	red_x = 0.0
	red_y = 0.0

	green_x = 0.0
	green_y = 0.0

	blue_x = 0.0
	blue_y = 0.0

	for i, d in enumerate(data):
		if(labels[i] == 'red'):
			red_x = red_x + d[0]
			red_y = red_y + d[1]
		if(labels[i] == 'green'):
			green_x = green_x + d[0]
			green_y = green_y + d[1]
		if(labels[i] == 'blue'):
			blue_x = blue_x + d[0]
			blue_y = blue_y + d[1]

	center_red = (red_x/labels.count('red'), red_y/labels.count('red'))
	center_green = (green_x/labels.count('green'), green_y/labels.count('green'))
	center_blue = (blue_x/labels.count('blue'), blue_y/labels.count('blue'))	
	
	return (center_red, center_green, center_blue)


# run script
run_kmeans()