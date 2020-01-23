
# The file follows the algorithm in the poset paper

from poset_helper import *

def poset_algorithm(X):
	# input: a list of points 'X'
	# output: a 2- or 3- clique coloring, 'COLOR_DICT'

	COLOR_DICT = {x : "" for x in X}

	X = set(X)

	###################
	##### PICK x1 #####
	################### 

	potential_x1 = set( x for x in X if not is_empty(Intersection(I(x, X), Max(X))) )
	potential_x1 = Min(potential_x1)

	if len(Max(X)) <= 1:
		# print("Max(X) has only one element.")
		return False

	x1 = list(potential_x1)[0]
	# print("x1:", x1, '\n')
	
	if x1 in Max(X):
		# print("x1 is in Max(X).")
		return False

	M0 = Intersection(Max(X), I(x1, X))
	M1 = Min(I(x1, X))

	if not is_empty(Intersection(M1, Min(X))):
		for x in C(x1, X):
			COLOR_DICT[x] = 'r'

		for x in I(x1, X):
			COLOR_DICT[x] = 'b'

		return COLOR_DICT
	
	###################
	##### PICK x2 #####
	###################

	potential_x2 = set( x for x in D(x1, X) if not is_empty(Intersection(I(x, X), M1)))
	potential_x2 = Min(potential_x2)

	if len(potential_x2) == 0:
		# print("some sort of error here")
		return False

	x2 = list(potential_x2)[0]
	# print("x2:", x2, '\n')

	M2 = Min(I(x2, X))

	if not is_empty(Intersection(M2, Min(X))):
		for x in X:
			if comparable(x, x1) and comparable(x, x2):
				COLOR_DICT[x] = 'r'
			else:
				if incomparable(x, x1):
					COLOR_DICT[x] = 'b'
				else:
					COLOR_DICT[x] = 'y'

		return COLOR_DICT

	###################
	##### PICK xk #####
	###################

	print("to continue......")
	return False
