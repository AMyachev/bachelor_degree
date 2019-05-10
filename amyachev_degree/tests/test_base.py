import pytest

from amyachev_degree.core import (create_schedule, Jobs,
                                  Machines, JobSchedulingFrame)

from amyachev_degree.exact_algorithm import johnson_algorithm

frame1 = JobSchedulingFrame(Jobs(5), Machines(3), [[17, 19, 13], [15, 11, 12],
                                                   [14, 21, 16], [20, 16, 20],
                                                   [16, 17, 17]])
test_1 = create_schedule(frame1, [2, 4, 3, 0, 1])
assert test_1.end_time == 114
test_2 = create_schedule(frame1, [4, 2, 3, 0, 1])
assert test_2.end_time == 115

frame2 = JobSchedulingFrame(Jobs(6), Machines(2), [[2, 3],
                                                   [8, 3],
                                                   [4, 6],
                                                   [9, 5],
                                                   [6, 8],
                                                   [9, 7]])
solution1 = johnson_algorithm(frame2)
assert solution1 == [0, 2, 4, 5, 3, 1]
assert create_schedule(frame2, solution1).end_time == 41


class TestJobSchedulingFrame:

    @pytest.mark.parametrize('seed', ["NaN", 12345])
    def test_initial_seed(self, seed):
        frame = JobSchedulingFrame(Jobs(1), Machines(2), [[5, 5]],
                                   initial_seed=seed)
        assert seed == frame.initial_seed
