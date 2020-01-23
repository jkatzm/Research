#include <algorithm>
#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "omp.h"

#include <boost/algorithm/string.hpp>
#include <boost/random.hpp>
#include <boost/random/random_device.hpp>
#include <boost/random/discrete_distribution.hpp>

//////////////////////////////////////////////////////////////////////////////
// struct: out_edge
//////////////////////////////////////////////////////////////////////////////

struct out_edge {
    out_edge(uint64_t node_id, uint64_t timestamp) : n(node_id), t(timestamp) {} // constructor
    
    out_edge(const out_edge& old_obj) : n(old_obj.n), t(old_obj.t) {} // copy constructor
    
    out_edge& operator=(out_edge&&) { // move assignment
        return *this;
    }
    
    bool operator< (const out_edge& other) const {
        return (t < other.t);
    }
    
    const uint64_t n;
    const uint64_t t;
}; // out_edge

//////////////////////////////////////////////////////////////////////////////
// struct: graph
//////////////////////////////////////////////////////////////////////////////

struct graph {
    // ASSUMPTION: the nodes should be labeled 0 to |V|-1
    // ASSUMPTION: no self-loops
    graph(std::string file, std::string data_format) {
        if (data_format == "nnt") {
            std::ifstream ifs;

            ifs.open(file, std::ifstream::in);
            
            uint64_t i, j, t;
            while (ifs >> i >> j >> t) {
            	assert(i != j);
                out_edges[i].emplace_back(out_edge(j, t));
                out_edges[j];
            }
            
            ifs.close();
            
            for (auto& it : out_edges) {
                std::sort(it.second.begin(), it.second.end());
            }
        }

        else if (data_format == "nn") {
            std::ifstream ifs;

            ifs.open(file, std::ifstream::in);
			
			uint64_t i, j;            
            while (ifs >> i >> j) {
            	assert(i != j);
                out_edges[i].emplace_back(out_edge(j, -1));
                out_edges[j];
            }
            
            ifs.close();
        }

        else {
            throw "illegal data format";
        }
    }
    
    size_t num_nodes() const {
        return out_edges.size();
    }

    size_t num_neighbors(uint64_t n) const {
    	return out_edges.at(n).size();
    }
    
    bool node_exists(uint64_t n) const {
        return out_edges.find(n) != out_edges.end();
    }
    
    const std::vector<out_edge>& get_out_edges(uint64_t n) const {
        return out_edges.at(n);
    }

    void print_neighbors(uint64_t n) const {
        std::cout << n << std::endl;
        for (const auto& it : get_out_edges(n)) {
            std::cout << "--> " << it.n << " (t=" << it.t << ")" << std::endl;
        }
    }
    
private:
    std::unordered_map<uint64_t, std::vector<out_edge>> out_edges;
}; // graph

//////////////////////////////////////////////////////////////////////////////
// helper functions
//////////////////////////////////////////////////////////////////////////////

template <typename RandomNumberEngine>
int randint(uint64_t upper_bound, RandomNumberEngine& rnd_eng) {
    // returns a random integer in the range [0, upper_bound)
    std::uniform_int_distribution<uint64_t> dist(0, upper_bound-1);
    return dist(rnd_eng);
}

template <typename RandomNumberEngine>
const out_edge& get_random_item(const std::vector<out_edge>& vec, RandomNumberEngine& rnd_eng) {
    // returns an item from a random index of a vector
    return vec.at(randint(vec.size(), rnd_eng));
}

//////////////////////////////////////////////////////////////////////////////
// class: random_walk
//////////////////////////////////////////////////////////////////////////////

class random_walk {
	const std::string walk_type; // either "PageRank" or "Temporal" or "CloseTriangles"
	const uint64_t n_walkers;

    const size_t n_threads;
    std::vector<boost::random::mt19937_64> rnd_eng_per_thread;
    std::vector<std::vector<uint64_t>> walker_history_per_thread;
    std::vector<int> timestamps_per_thread;
    
public:
    random_walk( std::string _walk_type, uint64_t _n_walkers, uint64_t _n_threads ) :
    	n_threads(_n_threads),
        n_walkers(_n_walkers),
        walk_type(_walk_type), 
        rnd_eng_per_thread(0),
        walker_history_per_thread(0),
        timestamps_per_thread(0) {

        for (size_t tc = 0; tc < n_threads; tc++) {
            boost::random::random_device rnd_dev;
            rnd_eng_per_thread.push_back(boost::random::mt19937_64(rnd_dev));
            walker_history_per_thread.push_back(std::vector<uint64_t>(0));
            timestamps_per_thread.push_back(-1);
        }

        std::cout << std::endl << "Initialized random walker." << std::endl << std::endl;
	} // random_walk

	void do_walk(const graph& G, std::vector<double>& scores, const std::string score_type, const uint64_t seed, bool verbose) {
		assert(walk_type == "PageRank" || walk_type == "Temporal" || walk_type == "CloseTriangles");
		assert(score_type == "ep" || score_type == "cp");

		if (verbose) {
			std::cout << "Simulating " << walk_type << " walk..." << std::endl << std::endl;
		}

		boost::random::bernoulli_distribution<> continue_walking(0.85);

		#pragma omp parallel for schedule(static, 1)
		for (uint64_t walker_ID = 0; walker_ID < n_walkers; walker_ID++) {
			
			// initialization
            size_t thread_ID = omp_get_thread_num();
            auto& rnd_eng = rnd_eng_per_thread[thread_ID];
            walker_history_per_thread[thread_ID].clear();
            timestamps_per_thread[thread_ID] = -1;

            // start the walk at the seed
            uint64_t current_vertex = seed;
            walker_history_per_thread[thread_ID].push_back(seed);

            // #pragma omp critical(cout)
            // std::cout << thread_ID << ":" << walker_history_per_thread[thread_ID].back() << " "; // TODO: erase

            if (score_type == "cp") {
	            {
	            #pragma omp atomic update
	                scores[current_vertex] += (1 - 0.85) / n_walkers;
	            }
	        }

            // while the walk doesn't terminate
            while (continue_walking(rnd_eng)) {
            	uint64_t next_vertex;

                const std::vector<out_edge>& neighbors = G.get_out_edges(current_vertex);

                ////////////////////////////////////////
				// PageRank
				////////////////////////////////////////
                if (walk_type == "PageRank") {
                    // if dangling, jump back to the seed
                    if (neighbors.empty()) {
                        next_vertex = seed;
                    }

                    // otherwise, jump to random neighbor
                    else {
                        next_vertex = get_random_item(neighbors, rnd_eng).n;
                    }
                }

                ////////////////////////////////////////
				// Temporal
				////////////////////////////////////////
                else if (walk_type == "Temporal") {
                    int x = timestamps_per_thread[thread_ID];
                    auto comp = [x](const out_edge& e) {return (int64_t)e.t > x;};
                    auto first_causal = std::find_if(neighbors.begin(), neighbors.end(), comp);
                    size_t distance = std::distance(first_causal, neighbors.end());
                    
                    // if dangling, jump back to the seed
                    if (distance == 0) { // dangling
                        next_vertex = seed;
                        timestamps_per_thread[thread_ID] = -1;
                    }

                    // otherwise, pick randomly from the set of legal neighbors
                    else {
                        auto next = first_causal + randint(distance, rnd_eng);
                        next_vertex = next->n;
                        timestamps_per_thread[thread_ID] = next->t;
                    }
                }

                ////////////////////////////////////////
				// CloseTriangles
				////////////////////////////////////////
				else if (walk_type == "CloseTriangles") {
					// if dangling, jump back to the seed
					if (neighbors.empty()) {
                        next_vertex = seed;
                        walker_history_per_thread[thread_ID].clear();
                        // std::cout << " x "; // TODO: erase
                    }

                    else {
                    	// if we can close a triangle, do it
						if (walker_history_per_thread[thread_ID].size() > 2) {
							auto it = walker_history_per_thread[thread_ID].end() - 3;
							uint64_t possible_triangle = *it;
							auto comp = [possible_triangle](const out_edge& e) {return e.n == possible_triangle;};

							if (std::any_of(neighbors.begin(), neighbors.end(), comp)) {
								next_vertex = possible_triangle;
							}

							else {
								next_vertex = get_random_item(neighbors, rnd_eng).n;
							}
						}

						// otherwise, jump to random neighbor
	                    else {
	                        next_vertex = get_random_item(neighbors, rnd_eng).n;
	                    }    
                    }

                    walker_history_per_thread[thread_ID].push_back(next_vertex);
                    // #pragma omp critical(cout)
                    // std::cout << thread_ID << ":" << walker_history_per_thread[thread_ID].back() << " "; // TODO: erase
				}


                current_vertex = next_vertex;

                

	            if (score_type == "cp") {
	            	{
	                #pragma omp atomic update
	                    scores[current_vertex] += (1 - 0.85) / n_walkers;
	                }
	            }
            } // while

			// #pragma omp critical(cout)
            // std::cout << thread_ID << ":__"; // TODO: erase

            if (score_type == "ep") {
            	{
	            #pragma omp atomic update
	                scores[current_vertex] += 1.0 / n_walkers;
	            }
            }
		} // for

        if (verbose) {
        	std::cout << "Simulation complete." << std::endl << std::endl;
        }

	} // do_walk

}; // random_walk

