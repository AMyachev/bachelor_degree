#pragma once
#include "basis.h"
#include <ctime>

using std::vector;
using std::string;
using std::cout;
using std::pair;
using std::endl;

typedef pair<const permutation&, const permutation&> pair_parents;
typedef pair<const permutation*, const permutation*> pair_descendants;

enum Escip { random_control = 1};
enum Essp { panmixia = 1 };
enum Escd { crossover_OX = 1, crossover_CX };
enum Etm { point_mutation = 1, saltation };
enum Essng { B_tournament = 1, roulette };

const int share_mutation = 5;                                       // 0.05
const int size_tournament = 4;

class Singleton {
private:
	Escip strategy_creating_initial_population;
	Essp strategy_selection_parents;
	Escd strategy_creating_descendants;
	Etm type_mutation;
	Essng strategy_selection_next_generation;
public:
	Singleton(Escip scip, Essp ssp, Escd scd, Etm tm, Essng ssng);
	const Escip& get_strategy_creating_initial_population() const;
	const Escd& get_strategy_creating_descendants() const;
	const Essp& get_strategy_selection_parents() const;
	const Etm& get_type_mutation() const;
	const Essng& get_strategy_selection_next_generation() const;

};

class Population : public vector<permutation*> {
	vector<float>* adaptability_permutations;
public:
	const vector<float>& get_adapt() const;
	void set_adapt(vector<float>* adapt_indiv);
	vector<float>* calculate_adaptability(input_data& param);
	int find_best_permutation();
	float calculate_average_fitness();
	int count_individ(const permutation & individ);
	void print_population();
	~Population();
};

class genetic_algorithm {
	input_data& param;
	Singleton prima;
	int size_population;
	int count_generations;
	int find(const permutation& whr, int element);
	int find_begin_cycle(const permutation& whr);
	pair_parents* choose_parents(const Population & population);
	permutation* create_child_for_crossover_OX(const permutation& first_parent, const permutation& second_parent,
		int first_point_section, int second_point_section);
	permutation* create_child_for_crossover_CX(const permutation& first_parent, const permutation& second_parent);
	pair_descendants * create_descendants(const pair_parents & parents);
	Population* create_initial_population(permutation* perm);
	Population * reproduction(const Population & population);
	Population * create_mutants(const Population & descendants);
	permutation* mutation(const permutation& descendant);
public:
	int choose_size_population();
	int choose_size_population_childs();
	void set_Singleton(Singleton _prima);
	bool find(const Population & population, const vector<pair<int, float>>& indiv, int index);
	Population * next_generation(Population * descendants, Population * mutants);
	bool continue_evolve(float best_criterion);

	genetic_algorithm(input_data& _param, Singleton _prima);
	permutation start(permutation* perm = nullptr);
	int get_count_generations() const;
	friend bool friend_gen_alg_test();
};


bool test_population();