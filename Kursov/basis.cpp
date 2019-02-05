#include "basis.h"

/* Implementation class input data */
input_data::input_data(vector<vector<float>> _matrix_time) :
	count_operations(_matrix_time[0].size()), count_machines(_matrix_time.size()), matrix_time(_matrix_time) {}

input_data input_data::read_input_data_test() {
	vector<vector<float>> _matrix_time;
	_matrix_time.push_back(vector<float>{1.7f, 2.3f, 4.5f, 2.9f, 6.1f, 5.6f, 1.2f, 6.3f, 8.8f, 3.7f});
	_matrix_time.push_back(vector<float>{0.7f, 2.8f, 2.2f, 3.4f, 1.1f, 5.5f, 3.6f, 4.7f, 2.4f, 5.8f});
	_matrix_time.push_back(vector<float>{1.8f, 2.2f, 4.5f, 2.1f, 4.1f, 3.2f, 2.6f, 6.2f, 8.0f, 7.1f});
	return input_data(_matrix_time);
}

input_data input_data::read_input_data(string file_name) {
	std::ifstream fin(file_name);
	int count_machines;
	int count_operations;
	fin >> count_machines;
	fin >> count_operations;
	float temp;
	vector<vector<float>> _matrix_time(count_machines);
	for (int i = 0; i < count_machines; ++i)
		for (int j = 0; j < count_operations; ++j) {
			fin >> temp;
			_matrix_time[i].push_back(temp);
		}
	fin.close();
	return input_data(_matrix_time);
}

void input_data::print_matrix()
{
	for (int i = 0; i < count_machines; ++i) {
		for (int j = 0; j < count_operations; ++j)
			cout << matrix_time[i][j] << " ";
		cout << std::endl;
	}
}

int input_data::get_count_operations() const {
	return count_operations;
}

int input_data::get_count_machines() const {
	return count_machines;
}

const vector<vector<float>>& input_data::get_matrix()  const {
	return matrix_time;
}
/////////////////////////////////////////////////////////////////

/* Implementation struct pair_front_alg */
pair_front_alg::pair_front_alg(int _operation_number, float _all_machines_time) : 
	operation_number(_operation_number), all_machines_time(_all_machines_time) {}
/////////////////////////////////////////////////////////////////

/* Implementation struct pair_front_alg */
permutation::permutation(vector<int> _content) : vector<int>(_content) {}

permutation::permutation() : vector<int>() {}

permutation::permutation(int size) : vector<int>(size) {}

void permutation::print() {
	for (unsigned int i = 0; i < size(); ++i)
		cout << ((*this)[i] + 1) << "  ";
	cout << std::endl;
}

void permutation::print_way()
{
	for (unsigned int i = 0; i < size(); ++i)
		cout << (operator[](i) + 1) << " ";
}

float permutation::criterion(input_data& param) {
	vector<vector<float>> matrix_time = param.get_matrix();
	vector<float> temp(size(), 0);
	for (int j = 0; j < param.get_count_machines(); ++j) {
		temp[0] += matrix_time[j][(*this)[0]];
		for (unsigned int i = 1; i < size(); ++i) {
			temp[i] += temp[i - 1] + matrix_time[j][(*this)[i]];
		}
	}
	return temp[temp.size() - 1];
}

bool permutation::operator==(const permutation & second)
{
	for (unsigned int i = 0; i < size(); ++i)
		if ((*this)[i] != second[i]) return false;
	return true;
}

permutation* permutation::random_permutation(int size)
{
	permutation* perm = new permutation;
	int index = 0;
	(*perm).reserve(size);
	permutation temp;
	for (int i = 0; i < size; ++i)
		temp.push_back(i);
	for (int i = 0; i < size; ++i) {
		index = rand() % temp.size();
		perm->push_back(temp[index]);
		temp.erase(temp.begin() + index);
	}
	return perm;
}
/////////////////////////////////////////////////////////////////

bool is_equal(float x, float y) {
	return std::fabs(x - y) < epsilon;
}
bool test_permutation() {
	permutation perm({ 0, 1, 2, 3, 4 });
	return is_equal(120.6f, perm.criterion(input_data({
		{ 1.2f, 2.3f, 4.1f, 2.4f, 3.3f },
		{ 1.5f, 1.4f, 1.3f, 4.1f, 3.1f },
		{ 2.1f, 4.2f, 2.1f, 1.7f, 6.1f }
	})));
}