#include "genetic_algorithm.h"

/* Implementation class Singleton */
Singleton::Singleton(Escip scip, Essp ssp, Escd scd, Etm tm, Essng ssng)
	: strategy_creating_initial_population(scip)
	, strategy_selection_parents(ssp)
	, strategy_creating_descendants(scd)
	, type_mutation(tm)
	, strategy_selection_next_generation(ssng)
{};

const Escip& Singleton::get_strategy_creating_initial_population() const
{
	return strategy_creating_initial_population;
}

const Escd & Singleton::get_strategy_creating_descendants() const
{
	return strategy_creating_descendants;
}

const Essp & Singleton::get_strategy_selection_parents() const
{
	return strategy_selection_parents;
}

const Etm & Singleton::get_type_mutation() const
{
	return type_mutation;
}

const Essng & Singleton::get_strategy_selection_next_generation() const
{
	return strategy_selection_next_generation;
}
/////////////////////////////////////////////////////////////////

/* Implementation class Population*/
const vector<float>& Population::get_adapt() const
{
	return *adaptability_permutations;
}

vector<float>* Population::calculate_adaptability(input_data& param)
{
	vector<float>* vect = new vector<float>;
	vect->reserve(size());
	for (unsigned int i = 0; i < size(); ++i)
		vect->push_back((*this)[i]->criterion(param));
	return vect;
}

void Population::set_adapt(vector<float>* adapt_indiv)
{
	adaptability_permutations = adapt_indiv;
}

int Population::find_best_permutation()
{
	/* working for not empty population*/

	float min_adaptability = get_adapt()[0];
	int index = 0;
	for (unsigned int i = 1; i < size(); ++i)
		if (get_adapt()[i] < min_adaptability) {
			min_adaptability = get_adapt()[i];
			index = i;
		}
	return index;
}

float Population::calculate_average_fitness()
{
	float sum = 0;
	const vector<float>& adapt = get_adapt();
	for (unsigned int i = 0; i < size(); ++i)
		sum += adapt[i];
	return sum / size();
}

int Population::count_individ(const permutation & individ)
{
	int count = 0;
	for (unsigned int i = 0; i < size(); ++i)
		if (individ == *(*this)[i]) ++count;
	return count;
}

void Population::print_population()
{
	const vector<float>& adaptability_permutations = get_adapt();
	for (unsigned int i = 0; i < size(); ++i) {
		(*this)[i]->print_way();
		cout << "   " << adaptability_permutations[i];
		cout << std::endl;
	}
}

Population::~Population() {
	for (unsigned int i = 0; i < this->size(); ++i)
		delete (*this)[i];
	delete adaptability_permutations;
}
//////////////////////////////////////////////////////////////////

/* Implementation class genetic_algorithm*/
int genetic_algorithm::find(const permutation& whr, int element)
{
	for (unsigned int i = 0; i < whr.size(); ++i)
		if (whr[i] == element) return i;
	return -1;
}

int genetic_algorithm::find_begin_cycle(const permutation& whr)
{
	int size = whr.size();
	int ind_begin = rand() % size;
	if (whr[ind_begin] != 0) {
		for (int i = ind_begin; i >= 0; --i)
			if (whr[i] == 0)	return i;
		for (int i = ind_begin; i < size; ++i)
			if (whr[i] == 0) return i;
		return -1;
	}
	return ind_begin;
}

pair_parents* genetic_algorithm::choose_parents(const Population & population)
{
	int first = 0;
	int second = 0;

	pair_parents* pair = nullptr;

	switch (prima.get_strategy_selection_parents()) {
	case panmixia:
		first = rand() % population.size();
		second = rand() % population.size();
		break;
	default:
		break;
	}
	pair = new pair_parents(*population[first], *population[second]);
	return pair;
}

permutation* genetic_algorithm::create_child_for_crossover_OX(const permutation& first_parent, const permutation& second_parent,
	int first_point_section, int second_point_section)
{
	int size = param.get_count_operations();
	permutation temp;
	int pos_for_paste = 0;
	permutation* child = new permutation(param.get_count_operations());
	child->reserve(param.get_count_operations());

	for (int i = first_point_section; i <= second_point_section; ++i)
		(*child)[i] = first_parent[i];

	for (int i = second_point_section + 1; i < size; ++i)              // check after second point
		if ((first_parent.begin() + second_point_section + 1) ==
			std::find(first_parent.begin() + first_point_section, first_parent.begin() + second_point_section + 1, second_parent[i]))
			temp.push_back(second_parent[i]);
	for (int i = 0; i < second_point_section + 1; ++i)                    // check before second point
		if ((first_parent.begin() + second_point_section + 1) ==
			std::find(first_parent.begin() + first_point_section, first_parent.begin() + second_point_section + 1, second_parent[i]))
			temp.push_back(second_parent[i]);

	for (int i = second_point_section + 1; i < size; ++i)
		(*child)[i] = temp[pos_for_paste++];
	for (int i = 0; i < first_point_section; ++i)
		(*child)[i] = temp[pos_for_paste++];
	return child;
}

permutation* genetic_algorithm::create_child_for_crossover_CX(const permutation& first_parent, const permutation& second_parent)
{
	int choose_parent = 0;
	int ind_begin_cycle = 0;
	int ind_current = 0;

	permutation auxiliary(param.get_count_operations());

	permutation* child = new permutation(param.get_count_operations());
	child->reserve(param.get_count_operations());

	while ((ind_begin_cycle = find_begin_cycle(auxiliary)) != -1) {
		choose_parent = rand() % 2;
		ind_current = ind_begin_cycle;
		if (choose_parent == 0) {
			while (second_parent[ind_current] != first_parent[ind_begin_cycle]) {
				(*child)[ind_current] = first_parent[ind_current];
				auxiliary[ind_current] = 1;
				ind_current = find(first_parent, second_parent[ind_current]);
			}
			(*child)[ind_current] = first_parent[ind_current];
			auxiliary[ind_current] = 1;
		}
		else {
			while (second_parent[ind_current] != first_parent[ind_begin_cycle]) {
				(*child)[ind_current] = second_parent[ind_current];
				auxiliary[ind_current] = 1;
				ind_current = find(first_parent, second_parent[ind_current]);
			}
			(*child)[ind_current] = second_parent[ind_current];
			auxiliary[ind_current] = 1;
		}
	}
	return child;
}

pair_descendants * genetic_algorithm::create_descendants(const pair_parents & parents)
{
	int size = param.get_count_operations();
	int first_point_section = rand() % size;
	int second_point_section = rand() % size;

	if (second_point_section < first_point_section) {                          //swap
		first_point_section ^= second_point_section;
		second_point_section ^= first_point_section;
		first_point_section ^= second_point_section;
	}
	pair_descendants* childs = nullptr;
	permutation* first_child = nullptr;
	permutation* second_child = nullptr;

	switch (prima.get_strategy_creating_descendants()) {
	case crossover_OX:
		first_child = create_child_for_crossover_OX(parents.first, parents.second,
			first_point_section, second_point_section);
		second_child = create_child_for_crossover_OX(parents.second, parents.first,
			first_point_section, second_point_section);
		break;
	case crossover_CX:
		first_child = create_child_for_crossover_CX(parents.first, parents.second);
		second_child = create_child_for_crossover_CX(parents.second, parents.first);
		break;
	default:
		break;
	}
	childs = new pair_descendants(first_child, second_child);
	return childs;
}

Population* genetic_algorithm::create_initial_population(permutation* perm) {
	Population* population = new Population;
	population->reserve(size_population);
	population->set_adapt(nullptr);
	int size = param.get_count_operations();
	if (perm == nullptr) {
		switch (prima.get_strategy_creating_initial_population()) {
		case random_control:
			for (int i = 0; i < size_population; ++i) {
				(*population).push_back(permutation::random_permutation(size));
			}
			break;
		}
	}
	else {
		permutation* perm_for_popul = new permutation(*perm);
		(*population).push_back(perm_for_popul);
		for (unsigned int i = 1; i < perm_for_popul->size(); ++i) {
			perm_for_popul = new permutation(*perm);
			int temp = (*perm_for_popul)[i - 1];
			(*perm_for_popul)[i - 1] = (*perm_for_popul)[i];
			(*perm_for_popul)[i] = temp;
			(*population).push_back(perm_for_popul);
		}

	}
	return population;
}

Population * genetic_algorithm::reproduction(const Population & population)
{
	Population* descendants = new Population;
	descendants->reserve(choose_size_population_childs());
	descendants->set_adapt(nullptr);
	for (int i = 0; i < choose_size_population_childs(); ++i) {
		pair_parents* parents = choose_parents(population);
		pair_descendants* childs = create_descendants(*parents);
		delete parents;
		descendants->push_back(const_cast<permutation*>(childs->first));
		descendants->push_back(const_cast<permutation*>(childs->second));
		delete childs;
	}
	return descendants;
}

Population * genetic_algorithm::create_mutants(const Population & descendants)
{
	/*the number of mutants is not const*/

	Population* mutants = new Population;
	mutants->set_adapt(nullptr);
	for (unsigned int i = 0; i < descendants.size(); ++i) {
		if (rand() % 100 < share_mutation)
			mutants->push_back(mutation(*descendants[i]));
	}
	return mutants;
}

permutation* genetic_algorithm::mutation(const permutation& descendant)
{
	permutation* mutant = new permutation(descendant);
	int point1 = 0;
	int point2 = 0;
	switch (prima.get_type_mutation()) {
	case point_mutation:                                         //replaceable neighboring alleles
		point1 = rand() % (param.get_count_operations() - 1);
		(*mutant)[point1] ^= (*mutant)[point1 + 1];
		(*mutant)[point1 + 1] ^= (*mutant)[point1];
		(*mutant)[point1] ^= (*mutant)[point1 + 1];
		break;
	case saltation:
		point1 = rand() % param.get_count_operations();
		point2 = rand() % param.get_count_operations();
		if (point1 == point2)
			if (point2 != 0) --point2;
			else ++point2;
			(*mutant)[point1] ^= (*mutant)[point2];
			(*mutant)[point2] ^= (*mutant)[point1];
			(*mutant)[point1] ^= (*mutant)[point2];
			break;
	default:
		break;
	}
	return mutant;
}

int genetic_algorithm::choose_size_population() {
	return size_population;
}

int genetic_algorithm::choose_size_population_childs()
{
	return choose_size_population() * 2;
}

void genetic_algorithm::set_Singleton(Singleton _prima) {
	prima = _prima;
}

bool genetic_algorithm::find(const Population & population, const vector<pair<int, float>>& indiv, int index)
{
	for (unsigned int i = 0; i < indiv.size(); ++i)
		if (*population[index] == *population[indiv[i].first]) return true;
	return false;
}

Population * genetic_algorithm::next_generation(Population * descendants, Population * mutants)
{
	vector<float>& adapt_indiv = const_cast<vector<float>&>(descendants->get_adapt());
	for (unsigned int i = 0; i < mutants->size(); ++i) {                                   // join population
		descendants->push_back((*mutants)[i]);
		adapt_indiv.push_back(mutants->get_adapt()[i]);
	}

	int ind_min = 0;
	int ind = 0;
	int size = descendants->size();
	Population* next_generation = new Population;
	next_generation->reserve(choose_size_population());

	float sum_adapt = 0;
	vector<pair<int, float>> for_roulette;
	float adapt_rand = 0;
	int size_roul = 0;

	int i = 0;
	int j = 0;
	switch (prima.get_strategy_selection_next_generation()) {
	case B_tournament:
		for (int i = 0; i < choose_size_population() - 1; ++i) {
			ind_min = rand() % size;
			for (int j = 0; j < size_tournament - 1; ++j) {
				ind = rand() % size;
				if (adapt_indiv[ind] < adapt_indiv[ind_min]) ind_min = ind;
			}
			next_generation->push_back((*descendants)[ind_min]);
			descendants->erase(descendants->begin() + ind_min);
			--size;
		}
		break;
	case roulette:
		for (int i = 0; i < size; ++i)
			sum_adapt += adapt_indiv[i];
		for (int i = 0; i < size; ++i) {
			if (!find(*descendants, for_roulette, i))
				for_roulette.emplace_back(i, (adapt_indiv[i] / sum_adapt) *
					descendants->count_individ(*(*descendants)[i]));
		}
		size_roul = for_roulette.size();
		sort(for_roulette.begin(), for_roulette.end(),
			[](const pair<int, float>& first, const pair<int, float>& second) {
			return first.second < second.second;
		});

		for (int i = 1; i < size_roul; ++i) {
			for_roulette[i].second += for_roulette[i - 1].second;
		}

		j = for_roulette.size() - 1;                         // we have min
		while (i < j) {
			float temp = for_roulette[i].second;
			for_roulette[i].second = for_roulette[j].second;
			for_roulette[j].second = temp;
			++i; --j;
		}
		sort(for_roulette.begin(), for_roulette.end(),
			[](const pair<int, float>& first, const pair<int, float>& second) {
			return first.second < second.second;
		});


		for (int i = 0; i < choose_size_population() - 1; ++i) {
			adapt_rand = (rand() % (int)sum_adapt) / sum_adapt;
			for (int j = 0; j < size_roul; ++j)
				if (adapt_rand < for_roulette[j].second) {
					ind = for_roulette[j].first;
					break;
				}
			next_generation->push_back(new permutation(*(*descendants)[ind]));        //you have to allocate memory
		}
		break;
	default:
		break;
	}
	return next_generation;
}

/*Если number_generations_wait поколений нет особи, которая бы стала лучше приспособленной, чем лучшая особь предыдущих поколений, то алгоритм заканчивает работу*/
bool genetic_algorithm::continue_evolve(float best_criterion)
{
	++count_generations;                                 //подсчитываем общее число поколений
	static int counter = 0;
	static int number_generations_wait = param.get_count_operations() * 6;
	static float max_criterion = best_criterion;
	if (max_criterion >= best_criterion) ++counter;
	else {
		counter = 0;
		max_criterion = best_criterion;
	}
	if (counter < number_generations_wait) return true;
	counter = 0;
	return false;
}

genetic_algorithm::genetic_algorithm(input_data& _param, Singleton _prima) : param(_param), prima(_prima), count_generations(1)
{
	size_population = 10;
}

permutation genetic_algorithm::start(permutation* perm) {
	Population* parents = create_initial_population(perm);
	parents->set_adapt(parents->calculate_adaptability(param));

	cout << "initial population:" << endl << endl;
	parents->print_population();
	cout << endl;
	cout << "average_fitness: " << parents->calculate_average_fitness() << endl;
	permutation* best = nullptr;
	do {
		Population* descendants = reproduction(*parents);
		descendants->set_adapt(descendants->calculate_adaptability(param));

		Population* mutants = create_mutants(*descendants);
		mutants->set_adapt(mutants->calculate_adaptability(param));

		int index_best_permutation = parents->find_best_permutation();
		best = (*parents)[index_best_permutation];
		(*parents).erase(parents->begin() + index_best_permutation);


		delete parents;
		parents = next_generation(descendants, mutants);
		parents->push_back(best);
		delete descendants;

		parents->set_adapt(parents->calculate_adaptability(param));
	} while (continue_evolve(best->criterion(param)));

	cout << endl;
	cout << "last population: " << endl << endl;
	parents->print_population();
	cout << endl << endl;

	int index_best_permutation = parents->find_best_permutation();
	best = (*parents)[index_best_permutation];
	(*parents).erase(parents->begin() + index_best_permutation);
	return *best;
}

int genetic_algorithm::get_count_generations() const {
	return count_generations;
}
/////////////////////////////////////////////////////////////////


bool test_population() {
	input_data param({
		{ 1.2f, 2.3f, 4.1f, 2.4f, 3.3f },
		{ 1.5f, 1.4f, 1.3f, 4.1f, 3.1f },
		{ 2.1f, 4.2f, 2.1f, 1.7f, 6.1f }
	});
	Population popul;
	popul.push_back(new permutation(vector<int>({0, 1, 2, 3, 4})));
	popul.push_back(new permutation(vector<int>({ 1, 2, 0, 3, 4})));
	popul.set_adapt(popul.calculate_adaptability(param));
	return is_equal(129, popul.calculate_average_fitness());
}

bool friend_gen_alg_test() {
	input_data param({
		{ 1.2f, 2.3f, 4.1f, 2.4f, 3.3f },
		{ 1.5f, 1.4f, 1.3f, 4.1f, 3.1f },
		{ 2.1f, 4.2f, 2.1f, 1.7f, 6.1f }
	});
	bool flag = true;
	genetic_algorithm genetic_alg(param, Singleton(random_control, panmixia, crossover_CX, saltation, B_tournament));
	Population* init = genetic_alg.create_initial_population(nullptr);
	init->set_adapt(init->calculate_adaptability(param));
	flag = init->size() == 10;
	flag = (*init)[0]->size() == 5;
	Population* mutants = genetic_alg.create_mutants(*init);
	mutants->set_adapt(mutants->calculate_adaptability(param));
	flag = genetic_alg.create_mutants(*init)->size() != 0;
	flag = genetic_alg.next_generation(init, mutants)->size() == 9;     //10 станет лучшая особь из популяции (элитарная стратегия)
	for (int i = 0; i < param.get_count_operations() * 6 - 1; ++i) {
		flag = genetic_alg.continue_evolve(180) == true;
	}
	flag = genetic_alg.count_generations == param.get_count_operations() * 6;
	flag = genetic_alg.continue_evolve(180) == false;   // если param.get_count_operations() * 6 поколений не нашлась более приспособленная особь, то алгоритм заканчивает работу
	return flag;
}