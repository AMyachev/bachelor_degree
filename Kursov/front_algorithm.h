#pragma once
#include "basis.h"

class front_alg {
	input_data& param;
	permutation create_init_permutation();
public:
	front_alg(input_data& _param);
	permutation start();
};

bool test_front_alg();