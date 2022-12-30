import pygame, math, numpy, vertexObject, heapq

WHITE = (255, 255, 255)
GREY = (187, 187, 187)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 60

WIDTH, HEIGHT = 1280, 720

class hw1: 

	def draw_line_dashed(self, surface, color, start_pos, end_pos, width = 2, dash_length = 3, exclude_corners = True):

		# convert tuples to numpy arrays
		start_pos = numpy.array(start_pos)
		end_pos   = numpy.array(end_pos)

		# get euclidian distance between start_pos and end_pos
		length = numpy.linalg.norm(end_pos - start_pos)

		# get amount of pieces that line will be split up in (half of it are amount of dashes)
		dash_amount = int(length / dash_length)

		# x-y-value-pairs of where dashes start (and on next, will end)
		dash_knots = numpy.array([numpy.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

		return [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)
				for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]

	# def draw_dashed_line(self, surf, color, start_pos, end_pos, width=2, dash_length=3):
	# 	x1, y1 = start_pos
	# 	x2, y2 = end_pos
	# 	dl = dash_length

	# 	if (x1 == x2):
	# 		ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
	# 		xcoords = [x1] * len(ycoords)
	# 	elif (y1 == y2):
	# 		xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
	# 		ycoords = [y1] * len(xcoords)
	# 	else:
	# 		a = abs(x2 - x1)
	# 		b = abs(y2 - y1)
	# 		c = round(math.sqrt(a**2 + b**2))
	# 		dx = dl * a / c
	# 		dy = dl * b / c

	# 		xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
	# 		ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else dy)]

	# 	next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
	# 	last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
	# 	for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
	# 		start = (round(x1), round(y1))
	# 		end = (round(x2), round(y2))
	# 		pygame.draw.line(surf, color, start, end, width)

	def draw_blocked_box(self,window):
		
		# Take each element in the vertices list
		for i in range (len(vertices_list)):
			# Check if the square is suppose to be blocked
			if (vertices_list[i][2] == 1):
					# calculate the actual grid position and draw the blocked box
					tl_x = (vertices_list[i][0] - 1) * square_size + margin
					tl_y = (vertices_list[i][1] - 1) * square_size + margin
					pygame.draw.rect(window, GREY, pygame.Rect((tl_x + 1), (tl_y + 1), (square_size - 1), (square_size - 1)))	
	
	def draw_positions(self, window):

		# Get the coordinate position
		start_pos_x, start_pos_y = start_pos
		goal_pos_x, goal_pos_y = goal_pos

		# calculate actual grid position for both start and goal
		start_pos_x = (start_pos_x - 1) * square_size + margin
		start_pos_y = (start_pos_y - 1) * square_size + margin

		goal_pos_x = (goal_pos_x - 1) * square_size + margin
		goal_pos_y = (goal_pos_y - 1) * square_size + margin

		# draw the positions on the grid
		pygame.draw.circle(window, GREEN, (start_pos_x, start_pos_y), radius)
		pygame.draw.circle(window, BLUE, (goal_pos_x, goal_pos_y), radius)
        		

	def grid(self, window):
		x, y = margin, margin
		length_row = square_size * columns + margin
		length_column = square_size * rows + margin

		# draw the lines both horizontally and vertically so that it creates the grid
		for i in range (columns + 1):
			pygame.draw.line(window, BLACK, (x,margin), (x, length_column))
			x += square_size
			
		for i in range (rows + 1):
			pygame.draw.line(window, BLACK, (margin,y), (length_row, y))
			y += square_size


	def redraw(self, window):
		window.fill(WHITE)
		self.grid(window)
		counter = 0
		while (counter < (len(path) - 1)):
			first_vertex = path[counter]
			second_vertex = path[counter+1]
			self.draw_line_dashed(window, RED, ((first_vertex[0]-1)*square_size + margin, (first_vertex[1]-1)*square_size + margin), ((second_vertex[0]-1)*square_size + margin, (second_vertex[1]-1)*square_size + margin))
			# self.draw_dashed_line(window, RED, ((first_vertex[0]-1)*square_size + margin, (first_vertex[1]-1)*square_size + margin), ((second_vertex[0]-1)*square_size + margin, (second_vertex[1]-1)*square_size + margin))
			counter = counter + 1
		# self.draw_dashed_line(window, BLUE, (margin, margin), (square_size + margin , square_size + margin))
		self.draw_blocked_box(window)
		self.draw_positions(window)
		pygame.display.update()

	# vertex is an integer tuple, [x, y]
	# return a list of vertices of unblocked neighbors for vertex
	def find_neighbors(self, vertex):
		x , y =  vertex
		max_x = columns + 1
		min_x = 1
		max_y = rows + 1
		min_y = 1

		top_vertex = (x,y-1)
		bottom_vertex = (x,y+1)
		left_vertex = (x-1,y)
		right_vertex = (x+1,y)
		diagonal_tl = (x-1,y-1)
		diagonal_tr = (x+1,y-1)
		diagonal_bl = (x-1,y+1)
		diagonal_br = (x+1,y+1)

		listOfVertices = []

		listOfVertices.append((x-1, y-1))
		listOfVertices.append((x, y-1))
		listOfVertices.append((x+1, y-1))

		listOfVertices.append((x-1, y))
		listOfVertices.append((x+1, y))

		listOfVertices.append((x-1, y+1))
		listOfVertices.append((x, y+1))
		listOfVertices.append((x+1, y+1))

		counter = 0
		while (counter < len(listOfVertices)):
			if (listOfVertices[counter][0] < min_x):
				del listOfVertices[counter]
				counter = counter - 1
			if (listOfVertices[counter][0] > max_x):
				del listOfVertices[counter]
				counter = counter - 1
			if (listOfVertices[counter][1] < min_y):
				del listOfVertices[counter]
				counter = counter - 1
			if (listOfVertices[counter][1] > max_y):
				del listOfVertices[counter]
				counter = counter - 1
			counter = counter + 1
		
		counter = 0
		while (counter < len(listOfVertices)):
			if (listOfVertices[counter] == left_vertex):
				top_square = (x-1, y-1)
				entry_num_top = ((top_square[0]-1) * rows + top_square[1])
				bottom_square = (x-1, y)
				entry_num_bottom = ((bottom_square[0]-1) * rows + bottom_square[1])

				# getting blocked status for top square
				if (entry_num_top > len(vertices_list)) or (entry_num_top < 1):
					top_blocked = 1
				else:
					top_blocked = vertices_list[entry_num_top-1][2]
				
				# getting blocked status for bottom square
				if (entry_num_bottom > len(vertices_list)) or (entry_num_bottom < 1):
					bottom_blocked = 1
				else:
					bottom_blocked = vertices_list[entry_num_bottom-1][2]
				
				if (top_blocked == 1) and (bottom_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == right_vertex):
				top_square = (x, y-1)
				entry_num_top = ((top_square[0]-1) * rows + top_square[1])
				bottom_square = (x, y)
				entry_num_bottom = ((bottom_square[0]-1) * rows + bottom_square[1])

				# getting blocked status for top square
				if (entry_num_top > len(vertices_list)) or (entry_num_top < 1):
					top_blocked = 1
				else:
					top_blocked = vertices_list[entry_num_top-1][2]
				
				# getting blocked status for bottom square
				if (entry_num_bottom > len(vertices_list)) or (entry_num_bottom < 1):
					bottom_blocked = 1
				else:
					bottom_blocked = vertices_list[entry_num_bottom-1][2]
				
				if (top_blocked == 1) and (bottom_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == top_vertex):
				left_square = (x-1, y-1)
				entry_num_left = ((left_square[0]-1) * rows + left_square[1])
				right_square = (x, y-1)
				entry_num_right = ((right_square[0]-1) * rows + right_square[1])

				# getting blocked status for left square
				if (entry_num_left > len(vertices_list)) or (entry_num_left < 1):
					left_blocked = 1
				else:
					left_blocked = vertices_list[entry_num_left-1][2]
				
				# getting blocked status for right square
				if (entry_num_right > len(vertices_list)) or (entry_num_right < 1):
					right_blocked = 1
				else:
					right_blocked = vertices_list[entry_num_right-1][2]
				
				if (left_blocked == 1) and (right_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == bottom_vertex):
				left_square = (x-1, y)
				entry_num_left = ((left_square[0]-1) * rows + left_square[1])
				right_square = (x, y)
				entry_num_right = ((right_square[0]-1) * rows + right_square[1])

				# getting blocked status for left square
				if (entry_num_left > len(vertices_list)) or (entry_num_left < 1):
					left_blocked = 1
				else:
					left_blocked = vertices_list[entry_num_left-1][2]
				
				# getting blocked status for right square
				if (entry_num_right > len(vertices_list)) or (entry_num_right < 1):
					right_blocked = 1
				else:
					right_blocked = vertices_list[entry_num_right-1][2]
				
				if (left_blocked == 1) and (right_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == diagonal_tl):
				diagonal_square = (x-1, y-1)
				entry_num_diagonal = ((diagonal_square[0]-1) * rows + diagonal_square[1])

				# getting blocked status for diagonal square
				if (entry_num_diagonal > len(vertices_list)) or (entry_num_diagonal < 1):
					diagonal_blocked = 1
				else:
					diagonal_blocked = vertices_list[entry_num_diagonal-1][2]
				
				if (diagonal_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == diagonal_tr):
				diagonal_square = (x, y-1)
				entry_num_diagonal = ((diagonal_square[0]-1) * rows + diagonal_square[1])

				# getting blocked status for diagonal square
				if (entry_num_diagonal > len(vertices_list)) or (entry_num_diagonal < 1):
					diagonal_blocked = 1
				else:
					diagonal_blocked = vertices_list[entry_num_diagonal-1][2]
				
				if (diagonal_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == diagonal_bl):
				diagonal_square = (x-1, y)
				entry_num_diagonal = ((diagonal_square[0]-1) * rows + diagonal_square[1])

				# getting blocked status for diagonal square
				if (entry_num_diagonal > len(vertices_list)) or (entry_num_diagonal < 1):
					diagonal_blocked = 1
				else:
					diagonal_blocked = vertices_list[entry_num_diagonal-1][2]
				
				if (diagonal_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			elif (listOfVertices[counter] == diagonal_br):
				diagonal_square = (x, y)
				entry_num_diagonal = ((diagonal_square[0]-1) * rows + diagonal_square[1])

				# getting blocked status for diagonal square
				if (entry_num_diagonal > len(vertices_list)) or (entry_num_diagonal < 1):
					diagonal_blocked = 1
				else:
					diagonal_blocked = vertices_list[entry_num_diagonal-1][2]
				
				if (diagonal_blocked == 1):
					del listOfVertices[counter]
					counter = counter - 1

			counter = counter + 1

		return listOfVertices

	
	def h_of_n(self, vertex1, vertex2):
		diff_x = abs(vertex1[0] - vertex2[0])
		diff_y = abs(vertex1[1] - vertex2[1])
		inside_sqrt = diff_x**2 + diff_y**2
		answer = math.sqrt(inside_sqrt)
		return answer
	
	# def line_Of_Sight(self, s, e):
	# 	x0 = s[0]
	# 	y0 = s[1]
	# 	x1 = e[0]
	# 	y1 = e[1]
	# 	f = 0
	# 	dy = y1 - y0
	# 	dx = x1 - x0

	# 	if dy < 0:
	# 		dy = -1 * dy
	# 		vertex_map[s].curr_vertex = [x0, -1]
		

	# def theta_update_vertex(self, s, e):
	# 	e = vertex_map[e]
	# 	if (line_Of_Sight(s.parent, e.curr_vertex)):
	# 		s_parent_to_e = vertex_map[s.parent].g_value + self.h_of_n(s.parent, e.curr_vertex)
	# 		if (s_parent_to_e < e.g_value):
	# 			e.g_value = s_parent_to_e
	# 			e.parent = s.parent
	# 			if e.curr_vertex in theta_fringe_list:
	# 				e_position = theta_fringe_list.index(e.curr_vertex)
	# 				del theta_fringe[e_position]
	# 				heapq.heapify(theta_fringe)
	# 			f_of_e = self.h_of_n(e.curr_vertex, goal_pos) + s_parent_to_e
	# 			heapq.heappush(theta_fringe, (f_of_e, id(e), e))
	# 	else: 
	# 		s_to_e = s.g_value + self.h_of_n(s.curr_vertex, e.curr_vertex)
	# 		if (e.g_value == -1) or (s_to_e < e.g_value):
	# 			e.g_value = s_to_e
	# 			e.parent = s.curr_vertex
	# 			if e.curr_vertex in a_fringe_list:
	# 				e_position = a_fringe_list.index(e.curr_vertex)
	# 				del a_fringe[e_position]
	# 				heapq.heapify(a_fringe)
					
	# 			f_of_e = self.h_of_n(e.curr_vertex, goal_pos) + s_to_e
	# 			heapq.heappush(a_fringe, (f_of_e, id(e), e))

	# def theta_star(self):
	# 	global theta_fringe
	# 	global theta_fringe_list
	# 	global theta_closed_list
	# 	global theta_neighbor_list

	# 	start_vertex = vertex_map[start_pos]
	# 	start_vertex.g_value = 0.0
	# 	start_vertex.parent = start_pos
		
	# 	theta_fringe = []
	# 	heapq.heappush(theta_fringe, (start_vertex.g_value + self.h_of_n(start_pos, goal_pos), id(start_vertex), start_vertex))

	# 	theta_closed_list = []
	# 	theta_neighbor_list = []

	# 	while (len(theta_fringe) > 0):
	# 		curr_tuple = heapq.heappop(theta_fringe)
	# 		s = curr_tuple[2]
	# 		if (s.curr_vertex == goal_pos):
	# 			return True
	# 		theta_closed_list.append(s.curr_vertex)
	# 		neighbors = self.find_neighbors(s.curr_vertex)
	# 		for e in neighbors:
	# 			if e not in theta_closed_list:
	# 				theta_fringe_list = []
	# 				for i in range(len(theta_fringe)):
	# 					theta_fringe_list.append(theta_fringe[i][2].curr_vertex)

	# 				if e not in theta_fringe_list:
	# 					vertex_map[e].g_value = -1
	# 					vertex_map[e].parent = None
	# 				self.theta_update_vertex(s, e)
	# 	return False

	def a_update_vertex(self, s, e):
		e = vertex_map[e]
		s_to_e = s.g_value + self.h_of_n(s.curr_vertex, e.curr_vertex)
		if (e.g_value == -1) or (s_to_e < e.g_value):
			e.g_value = s_to_e
			e.parent = s.curr_vertex
			if e.curr_vertex in a_fringe_list:
				e_position = a_fringe_list.index(e.curr_vertex)
				del a_fringe[e_position]
				heapq.heapify(a_fringe)
				
			f_of_e = self.h_of_n(e.curr_vertex, goal_pos) + s_to_e
			heapq.heappush(a_fringe, (f_of_e, id(e) ,e))


	def a_star(self):
		global a_fringe
		global a_fringe_list
		global a_closed_list
		global a_neighbor_list

		start_vertex = vertex_map[start_pos]
		start_vertex.g_value = 0.0
		start_vertex.parent = start_pos
		
		a_fringe = []
		heapq.heappush(a_fringe, (start_vertex.g_value + self.h_of_n(start_pos, goal_pos), id(start_vertex), start_vertex))

		a_closed_list = []
		a_neighbor_list = []

		while (len(a_fringe) > 0):
			curr_tuple = heapq.heappop(a_fringe)
			s = curr_tuple[2]
			if (s.curr_vertex == goal_pos):
				return True
			a_closed_list.append(s.curr_vertex)
			neighbors = self.find_neighbors(s.curr_vertex)
			for e in neighbors:
				if e not in a_closed_list:
					a_fringe_list = []
					for i in range(len(a_fringe)):
						a_fringe_list.append(a_fringe[i][2].curr_vertex)

					if e not in a_fringe_list:
						vertex_map[e].g_value = -1
						vertex_map[e].parent = None
					self.a_update_vertex(s, e)
		return False


	def main(self):
		global rows
		global columns
		global start_pos
		global goal_pos
		global radius
		global margin
		global square_size
		global smallest_window 

		global vertices_list
		global path
		global vertex_map
		
		global successful

		# read each line from file and store in a list
		with open("coordinates_1.txt") as textFile:
			lines = [line.strip() for line in textFile]

		# Calculate the position for the start and the goal
		start_pos = lines[0]
		temp_x, temp_y = start_pos.split()
		start_pos = int(temp_x), int(temp_y)
		goal_pos = lines[1]
		temp_x, temp_y = goal_pos.split()
		goal_pos = int(temp_x), int(temp_y)
		
		# Get the number of columns and rows for the grid
		num_coordinates_str = lines[2]
		num_col, num_row = num_coordinates_str.split()
		rows = int(num_row)
		columns = int(num_col)

		square_size = 0
		smallest_window = 0

		# set the radius for the circle and margin of the grid 
		# based on how many rows/columns there is
		biggest_plane = columns
		margin = 50
		if (columns < rows):
			biggest_plane = rows

		if (biggest_plane <= 18):
			radius = 8
		elif(biggest_plane <= 25):
			radius = 6
		elif (biggest_plane <= 50):
			radius = 4
			margin = 25
		elif (biggest_plane <= 75):
			radius = 3
			margin = 10
		else:
			radius = 2
			margin = 10

		# margin = 0
		# calculate the sizes of each square on the grid
		if (WIDTH >= HEIGHT):
			smallest_window = HEIGHT
		else:
			smallest_window = WIDTH

		square_size = (WIDTH - margin - margin) // columns
		if (square_size * rows <= HEIGHT):
			square_size = (WIDTH - margin - margin) // columns

		elif (rows >= columns):

			square_size = (smallest_window - margin - margin) // rows
			
		else:
			square_size = (smallest_window - margin - margin) // columns

		# parse the coordinates for each square and also if its blocked or now
		vertices_list = []
		for i in range(3, len(lines)):
			col_pos, row_pos, blocked = lines[i].split()
			curr_tuple = (int(col_pos), int(row_pos), int(blocked))
			vertices_list.append(curr_tuple)

		# traverse through each vertex and create a vertex object for it
		vertex_map = {}
		for col in range (columns + 1): # 1 - 5
			for row in range (rows + 1): # 1 - 4
				curr_vertex = (col + 1), (row + 1)
				curr_obj = vertexObject.vertexObject(curr_vertex)
				vertex_map[curr_vertex] = curr_obj

		path = []
		successful = self.a_star()
		if (successful):
			finding_path = True
			curr_path = goal_pos
			while (finding_path):
				path.append(curr_path)
				prev_path = curr_path
				curr_path = vertex_map[curr_path].parent
				if (curr_path == prev_path):
					finding_path = False
		else:
			print ("No Path Found")
			return

		pygame.init()
		clock = pygame.time.Clock()
		window = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("Grid")

		run = True
		while run:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
			self.redraw(window)

	def __init__(self) -> None:
		pass


if __name__ == "__main__":
	visualizer = hw1()
	visualizer.main()