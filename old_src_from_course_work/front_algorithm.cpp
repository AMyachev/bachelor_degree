#include "front_algorithm.h"

/* Implementation class front_alg */
front_alg::front_alg(input_data& _param) : param(_param) {}

permutation front_alg::create_init_permutation() {
	vector<int> init_permutation;
	for (int i = 0; i < param.get_count_operations(); ++i)
		init_permutation.push_back(i);
	return init_permutation;
}

permutation front_alg::start() {
	permutation perm = create_init_permutation();
	vector<vector<float>> matrix_time = param.get_matrix();
	vector<pair_front_alg> operation_all_time;
	for (int i = 0; i < param.get_count_operations(); ++i) {
		float temp = 0;
		for (int j = 0; j < param.get_count_machines(); ++j) {
			temp += matrix_time[j][perm[i]];
		}
		operation_all_time.push_back(pair_front_alg(perm[i], temp));
	}
	sort(operation_all_time.begin(), operation_all_time.end(),
		[](const pair_front_alg& first, const pair_front_alg& second)
	{return first.all_machines_time < second.all_machines_time; });

	permutation result;
	for (unsigned int i = 0; i < operation_all_time.size(); ++i)
		result.push_back(operation_all_time[i].operation_number);
	return result;
}
/////////////////////////////////////////////////////////////////

bool test_front_alg() {
	input_data param({
		{ 1.2f, 2.3f, 4.1f, 2.4f, 3.3f },
		{ 1.5f, 1.4f, 1.3f, 4.1f, 3.1f },
		{ 2.1f, 4.2f, 2.1f, 1.7f, 6.1f }
	});
	front_alg alg(param);
	bool flag = true;
	permutation perm(alg.start());
	flag = is_equal(127.7f, perm.criterion(param));
	return flag;
}