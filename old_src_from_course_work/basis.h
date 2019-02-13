#pragma once
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <string>
#include <cmath>
#include <limits>

#define epsilon 0.001

using std::vector;
using std::string;
using std::cout;

struct input_data {
private:
	int count_operations;
	int count_machines;
	vector<vector<float>> matrix_time;
public:
	input_data(vector<vector<float>> _matrix_time);
	static input_data read_input_data_test();
	static input_data read_input_data(string file_name);
	void print_matrix();
	int get_count_operations() const;
	int get_count_machines() const;
	const vector<vector<float>>& get_matrix() const;
};

struct pair_front_alg {
	int operation_number;
	float all_machines_time;
	pair_front_alg(int _operation_number, float _all_machines_time);
};

class permutation: public vector<int> {
public:
	permutation(vector<int> _content);
	permutation();
	permutation(int size);
	void print();
	void print_way();
	float criterion(input_data& param);
	bool operator==(const permutation & second);
	static permutation* random_permutation(int size);
};

bool is_equal(float x, float y);
bool test_permutation();