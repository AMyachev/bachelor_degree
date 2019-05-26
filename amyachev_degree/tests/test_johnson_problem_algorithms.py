import pytest

from amyachev_degree.core import compute_end_time, flow_job_generator
from amyachev_degree.simple_heuristics import neh_heuristics, palmer_heuristics
from amyachev_degree.exact_algorithm import johnson_algorithm


@pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                         [(20, 873654221, 0.56),
                          (50, 379008056, 0.23),
                          (100, 1866992158, 0.08),
                          (200, 216771124, 0.02),
                          (500, 495070989, 0.01)
                          ])
def test_palmer_heuristic_johnson_problem(count_jobs, time_seed,
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

    """
    count_machines = 2
    frames = []
    for i in range(10):
        frames.append(flow_job_generator(count_jobs,
                                         count_machines, time_seed + i))
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = palmer_heuristics(frames[i])
        schedule_end_time = compute_end_time(frames[i], solution)

        johnson_solution = johnson_algorithm(frames[i])
        best_end_time = compute_end_time(frames[i], johnson_solution)

        end_time_diff = schedule_end_time - best_end_time
        solutions_ratio.append(end_time_diff / best_end_time)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                         [(20, 873654221, 0.00),
                          (50, 379008056, 0.02),
                          (100, 1866992158, 0.00),
                          (200, 216771124, 0.00),
                          (500, 495070989, 0.00)
                          ])
def test_neh_heuristic_johnson_problem(count_jobs, time_seed,
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
    count_machines = 2
    frames = []
    for i in range(10):
        frames.append(flow_job_generator(count_jobs,
                                         count_machines, time_seed + i))
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = neh_heuristics(frames[i])
        schedule_end_time = compute_end_time(frames[i], solution)

        johnson_solution = johnson_algorithm(frames[i])
        best_end_time = compute_end_time(frames[i], johnson_solution)

        end_time_diff = schedule_end_time - best_end_time
        solutions_ratio.append(end_time_diff / best_end_time)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio
