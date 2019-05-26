import pytest

from amyachev_degree.core import (flow_job_generator,
                                  johnson_three_machines_generator)
from amyachev_degree.simple_heuristics import (liu_reeves_heuristics,
                                               neh_heuristics,
                                               palmer_heuristics)
from amyachev_degree.exact_algorithm import johnson_algorithm
from amyachev_degree.util.testing import percentage_deviation


class TestJohnsonProblems:

    def generation_problems(self, count_problem: int, generator: object,
                            **kwargs: dict) -> list:
        """
        Generates `count_problem` problems by `generator`.

        Parameters
        ----------
        count_problem: int
        generator: object
            any function from: {flow_job_generator,
            johnson_three_machines_generator}
        kwargs: dict
            It can contain the following parameters: {count_jobs,
            count_machines, initial_seed}

        Returns
        -------
        frames: list
            list of `JobSchedulingFrame` objects

        """
        frames = []
        for i in range(count_problem):
            frames.append(generator(**kwargs))
            kwargs['initial_seed'] += 1

        return frames

    @pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                             [(20, 873654221, 0.56),
                              (50, 379008056, 0.23),
                              (100, 1866992158, 0.08),
                              (200, 216771124, 0.02),
                              (500, 495070989, 0.01)
                              ])
    def test_palmer_heuristic_johnson_problem(self, count_jobs, time_seed,
                                              expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Johnson's problem of two machines.

        Abstract
        --------
        The experiment consists in comparing the results of palmer heuristic
        with the exact solution found by Johnson's algorithm.

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_johnson_problem_algorithms.py\
            ::test_palmer_heuristic_johnson_problem`

        All tests run about 1.5 sec.

        """
        frames = self.generation_problems(
            count_problem=10, generator=flow_job_generator,
            count_jobs=count_jobs, count_machines=2, initial_seed=time_seed)

        average_percent_ratio = percentage_deviation(
            palmer_heuristics, {}, johnson_algorithm, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                             [(20, 873654221, 0.00),
                              (50, 379008056, 0.02),
                              # too long time for regular testing
                              # (100, 1866992158, 0.00),
                              # (200, 216771124, 0.00),
                              # (500, 495070989, 0.00)
                              ])
    def test_neh_heuristic_johnson_problem(self, count_jobs, time_seed,
                                           expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Johnson's problem of two machines.

        Abstract
        --------
        The experiment consists in comparing the results of NEH heuristic
        with the exact solution found by Johnson's algorithm.

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_johnson_problem_algorithms.py\
            ::test_neh_heuristic_johnson_problem`

        All tests run about 600 sec.

        """
        frames = self.generation_problems(
            count_problem=10, generator=flow_job_generator,
            count_jobs=count_jobs, count_machines=2, initial_seed=time_seed)

        average_percent_ratio = percentage_deviation(
            neh_heuristics, {}, johnson_algorithm, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                             [(20, 873654221, 0.82),
                              (50, 379008056, 0.54),
                              # too long time for regular testing
                              # (100, 1866992158, 0.74),
                              # (200, 216771124, 0.12),
                              # (500, 495070989, 0.08)
                              ])
    def test_liu_reeves_heuristic_johnson_problem(self, count_jobs, time_seed,
                                                  expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Johnson's problem of two machines.

        Abstract
        --------
        The experiment consists in comparing the results of LR(5) heuristic
        with the exact solution found by Johnson's algorithm.

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_johnson_problem_algorithms.py\
            ::test_liu_reeves_heuristic_johnson_problem`

        All tests run about 6600 sec.

        """
        frames = self.generation_problems(
            count_problem=10, generator=flow_job_generator,
            count_jobs=count_jobs, count_machines=2, initial_seed=time_seed)

        average_percent_ratio = percentage_deviation(
            liu_reeves_heuristics, {'count_sequences': 5},
            johnson_algorithm, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio
