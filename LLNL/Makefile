CXX_COMPILER=/usr/tce/packages/gcc/gcc-8.1.0/bin/g++
BOOST_INCLUDE=/usr/tce/packages/boost/boost-1.66.0-mvapich2-2.2-gcc-4.9.3

.PHONY: all random_walk

all: random_walk

random_walk:
	$(CXX_COMPILER) -std=c++17 -O3 -fopenmp -I$(BOOST_INCLUDE) -I include -lboost_random -ltcmalloc_minimal random_walk.cpp -o rw

.PHONY: clean
clean:	
	rm -f rw *.core
