import pytest

from amyachev_degree.core import compute_end_time, JobSchedulingFrame
from amyachev_degree.exact_algorithm import johnson_algorithm


class TestJohnsonAlgorithm:

    def test_johnson_algorithm(self):
        frame = JobSchedulingFrame([[2, 3],
                                    [8, 3],
                                    [4, 6],
                                    [9, 5],
                                    [6, 8],
                                    [9, 7]])
        solution = johnson_algorithm(frame)
        assert solution == [0, 2, 4, 5, 3, 1]

        solution_end_time = compute_end_time(frame, solution)
        assert solution_end_time == 41

    def test_bad_frame(self):
        msg = 'count machines must be 2'
        frame = JobSchedulingFrame([[1, 2, 3], [4, 5, 6]])

        with pytest.raises(ValueError, match=msg):
            johnson_algorithm(frame)
