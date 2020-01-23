"""
This file contains mostly set-theoretic operations on set of points in the plane/

Notation:
v and w are points in the plane. both are of the form (x_coord, y_coord)
X is our set of points
S is an arbitrary set
""" 

from numpy import sqrt

def is_empty(S):
	# returns True iff S is the empty set
	return len(S) == 0

def Intersection(X, Y):
	return X.intersection(Y)

def euc(v, w):
	# returns the Euclidean distance between points v and w
	return sqrt( (v[0]-w[0])**2 + (v[1]-w[1])**2 )

def gthan(v, w):
	# returns True iff v is 'greater than' w, as defined by the poset
	return euc(v, w) > 1 and v[0] > w[0]

def U(x, X):
	# defined in the paper
	return set(v for v in X if gthan(v, x))

def lthan(v, w):
	# returns True iff v is 'less than' w, as defined by the poset
	return euc(v, w) > 1 and v[0] < w[0]

def D(x, X):
	# defined in the paper
	return set(v for v in X if lthan(v, x))

def incomparable(v, w):
	# returns True iff v and w are 'incomparable', as defined by the poset
	return euc(v, w) <= 1 and v != w

def I(x, X):
	# defined in the paper
	return set(v for v in X if incomparable(v, x))

def comparable(v, w):
	return not incomparable(v, w)

def C(x, X):
	# defined in the paper
	return set(v for v in X if comparable(v, x))

# Wikipedia:
# A maximal (minimal) element of a subset S of some poset is an
# element of S that is not smaller (greater) than any other element in S.

def Max(S): # the set of maximal elements of S
	return set(v for v in S if is_empty(U(v, S)))

def Min(S): # the set of minimal elements of S 
	return set(v for v in S if is_empty(D(v, S)))

