#include "front_algorithm.h"
#include "genetic_algorithm.h"
//#define count_iterations 5
using namespace std;

int main() {
	srand(unsigned int(time(0)));
	input_data param = input_data::read_input_data("D:\\pipeline_transp.txt");
	clock_t currentTime = clock();
	cout << "----------Frontal algorithm----------------" << endl << endl;
	front_alg front_algorithm(param);
	permutation best_perm(front_algorithm.start());
	cout << "Best permutation found by frontal algorithm:   " << endl;
	best_perm.print();
	cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
	cout << "----------Genetic algorithm----------------" << endl << endl;

	cout << "---------------1 stage---------------------" << endl << endl;
	genetic_algorithm genetic_alg(param, Singleton(random_control, panmixia, crossover_CX, saltation, B_tournament));
	best_perm = genetic_alg.start(&best_perm);
	cout << "Best permutation:  ";
	best_perm.print();
	cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
	cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

	cout << "---------------2 stage---------------------" << endl << endl;
	genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_CX, point_mutation, B_tournament));
	best_perm = genetic_alg.start(&best_perm);
	cout << "Best permutation:  ";
	best_perm.print();
	cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
	cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

	cout << "---------------3 stage---------------------" << endl << endl;
	genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_OX, saltation, B_tournament));
	best_perm = genetic_alg.start(&best_perm);
	cout << "Best permutation:  ";
	best_perm.print();
	cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
	cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

	cout << "---------------4 stage---------------------" << endl << endl;
	genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_OX, point_mutation, B_tournament));
	best_perm = genetic_alg.start(&best_perm);
	cout << "Best permutation:  ";
	best_perm.print();
	cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
	cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

	cout << "---------------5 stage---------------------" << endl << endl;
	genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_OX, point_mutation, roulette));
	best_perm = genetic_alg.start(&best_perm);
	cout << "Best permutation:  ";
	best_perm.print();
	cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
	cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;
	currentTime = clock() - currentTime;
	currentTime = (clock_t)((double)currentTime / CLOCKS_PER_SEC);
	cout << "the running time of an algorithm in sec: " << currentTime << endl;
	system("pause");
	return 0;
}



/*int main() {
	srand(unsigned int(time(0)));
	//input_data param = input_data::read_input_data("D:\\test.txt");
	float crit_alg = 0.;
	clock_t temp[count_iterations];
	float procent[count_iterations];
	int temp2[count_iterations];
	for (int i = 0; i < count_iterations; ++i) {
		input_data param = input_data::read_input_data("D:\\test.txt");
		clock_t currentTime = clock();
		cout << "----------Frontal algorithm----------------" << endl << endl;
		front_alg front_algorithm(param);
		permutation best_perm(front_algorithm.start());
		cout << "Best permutation found by frontal algorithm:   " << endl;
		best_perm.print();
		cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
		crit_alg = best_perm.criterion(param);
		cout << "----------Genetic algorithm----------------" << endl << endl;

		cout << "---------------1 stage---------------------" << endl << endl;
		genetic_algorithm genetic_alg(param, Singleton(random_control, panmixia, crossover_CX, saltation, B_tournament));
		best_perm = genetic_alg.start(&best_perm);
		cout << "Best permutation:  ";
		best_perm.print();
		cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
		cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

		cout << "---------------2 stage---------------------" << endl << endl;
		genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_CX, point_mutation, B_tournament));
		best_perm = genetic_alg.start(&best_perm);
		cout << "Best permutation:  ";
		best_perm.print();
		cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
		cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

		cout << "---------------3 stage---------------------" << endl << endl;
		genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_OX, saltation, B_tournament));
		best_perm = genetic_alg.start(&best_perm);
		cout << "Best permutation:  ";
		best_perm.print();
		cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
		cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

		cout << "---------------4 stage---------------------" << endl << endl;
		genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_OX, point_mutation, B_tournament));
		best_perm = genetic_alg.start(&best_perm);
		cout << "Best permutation:  ";
		best_perm.print();
		cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
		cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;

		cout << "---------------5 stage---------------------" << endl << endl;
		genetic_alg.set_Singleton(Singleton(random_control, panmixia, crossover_OX, point_mutation, roulette));
		best_perm = genetic_alg.start(&best_perm);
		cout << "Best permutation:  ";
		best_perm.print();
		cout << "Criterion: " << best_perm.criterion(param) << endl << endl;
		cout << "Count generations: " << genetic_alg.get_count_generations() << endl << endl;
		temp2[i] = genetic_alg.get_count_generations();
		procent[i] = (crit_alg - best_perm.criterion(param)) / crit_alg;
		currentTime = clock() - currentTime;
		currentTime = (clock_t)((double)currentTime / CLOCKS_PER_SEC);
		temp[i] = currentTime;
		cout << "the running time of an algorithm in sec: " << currentTime << endl;
	}
	for (int i = 1; i < count_iterations; ++i) {
		temp[0] += temp[i];
		procent[0] += procent[i];
		temp2[0] += temp2[i];
	}
	cout << (temp[0] / count_iterations) << endl;
	cout << (procent[0] / count_iterations) << endl;
	cout << (temp2[0] / count_iterations) << endl;
	system("pause");
	return 0;
	}*/