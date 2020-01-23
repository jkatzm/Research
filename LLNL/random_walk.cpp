#include "random_walk.hpp"

//////////////////////////////////////////////////////////////////////////////
// helper functions
//////////////////////////////////////////////////////////////////////////////

double get_mean(const std::vector<double>& vec) {
	return std::accumulate(vec.begin(), vec.end(), 0.0) / vec.size();
}

double get_variance(const std::vector<double>& vec) {
	double mean = get_mean(vec);

	double accum = 0.0;
	
	for (double d : vec) {
		accum += (d - mean) * (d - mean);
	}

	return accum / (vec.size() - 1);
}

void reset_scores(std::vector<double>& scores) {
	#pragma omp parallel for
	for (size_t i = 0; i < scores.size(); i++) {
		scores[i] = 0.0;
	}
}

void print_top_k(const std::vector<double>& scores, uint64_t k, bool just_nodes) {
	
	std::vector<uint64_t> indices(scores.size());
	std::iota(indices.begin(), indices.end(), 0);

	auto comp = [&scores](uint64_t left, uint64_t right)
	{
		return scores[left] > scores[right];
	};

	std::partial_sort(indices.begin(), indices.begin() + k, indices.end(), comp);

	for (uint64_t i = 0; i < k; ++i) {
		// std::cout << i << " : ";
		std::cout << indices[i];

		if (just_nodes == false) {
			std::cout << " (" << scores[indices[i]] << ")";
		}

		std::cout << std::endl;
	}

    std::cout << std::endl;
}




//////////////////////////////////////////////////////////////////////////////
// main function
//////////////////////////////////////////////////////////////////////////////

int main(int argc, char** argv) {

    auto walk_start_time = std::chrono::high_resolution_clock::now();
    size_t n_threads = 0;
    
    {
    #pragma omp parallel
        {
            n_threads = omp_get_num_threads();
        }
    }
	// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	/////////////////////////
    // parameters 
    const std::string filename = "graphs/temporal_hack.txt";
    const graph G(filename, "nnt");
	const uint64_t seed = 0; // 200223, 301065
	const uint64_t top_k = G.num_nodes();
	const uint64_t target = 0; // TODO
	/////////////////////////


	std::cout << "# num nodes = " << G.num_nodes() << std::endl;
	std::cout << "# seed node = " << seed << std::endl;


	random_walk rw1("PageRank", 1000000, n_threads);
	std::vector<double> scores1(G.num_nodes(), 0.0);
	rw1.do_walk(G, scores1, "cp", seed, true);
	print_top_k(scores1, top_k, false);


	random_walk rw2("Temporal", 1000000, n_threads);
	std::vector<double> scores2(G.num_nodes(), 0.0);
	rw2.do_walk(G, scores2, "cp", seed, true);
	print_top_k(scores2, top_k, false);


	// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    auto walk_end_time = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(walk_end_time - walk_start_time);
    std::cout << std::endl << "# " << elapsed.count() << " seconds elapsed" << std::endl;
    return 0;

} // main


