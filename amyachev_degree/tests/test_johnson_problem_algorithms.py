import pytest

from amyachev_degree.core import compute_end_time, flow_job_generator
from amyachev_degree.simple_heuristics import (liu_reeves_heuristics,
                                               neh_heuristics,
                                               palmer_heuristics)
from amyachev_degree.exact_algorithm import johnson_algorithm


def percentage_deviation(fst_heuristic: object, fst_args: dict,
                         scnd_heuristic: object, scnd_args: dict,
                         frames: list) -> float:
    """
    The calculations are performed with respect to the results
    of the second heuristics.

    Parameters
    ----------
    fst_heuristic: object
        function callback
    fst_args: dict
        named arguments for `fst_heuristic`
    scnd_heuristic: object
        function callback
    scnd_args: dict
        named arguments for `scnd_heuristic`
    frames: list
        list of `JobSchedulingFrame` objects

    Returns
    -------
    average_deviation: float

    Notes
    -----
    Averaging occurs by the count of frames.

    """
    solutions_ratio = 0.
    for frame in frames:
        fst_solution = fst_heuristic(frame, **fst_args)
        fst_end_time = compute_end_time(frame, fst_solution)

        scnd_solution = scnd_heuristic(frame)
        scnd_end_time = compute_end_time(frame, scnd_solution)

        end_time_diff = fst_end_time - scnd_end_time
        solutions_ratio += end_time_diff / scnd_end_time

    return solutions_ratio / len(frames) * 100


def _percentage_deviation_johnson_problem(count_jobs: int, time_seed: int,
                                          count_problem: int,
                                          heuristic: object, **kwargs,
                                          ) -> float:
    """
    Calculates the average deviation of the completion time of the
    solution found by `heuristic` from the completion time of exact
    solution found by `johnson_algorithm`.

    Parameters
    ----------
    count_jobs: int
        count of jobs in generated Johnson problems
    time_seed: int
        time seed to generate the first Johnson problem;
        for each next problem - the seed is increased by 1
    count_problem: int
        count of generated Johnson problems
    heuristic: object
        any function from {`palmer_heuristics`, `neh_heuristics`,
                           `liu_reeves_heuristics`}
    args: dict
        named argument for `heuristic`

    Returns
    -------
    average_deviation: float

    """
    count_machines = 2
    frames = []
    for i in range(count_problem):
        frames.append(flow_job_generator(count_jobs,
                                         count_machines, time_seed + i))

    return percentage_deviation(heuristic, kwargs,
                                johnson_algorithm, {}, frames)


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

    All tests run about 1.5 sec.

    """
    average_percent_ratio = _percentage_deviation_johnson_problem(
        count_jobs, time_seed, count_problem=10, heuristic=palmer_heuristics)

    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                         [(20, 873654221, 0.00),
                          (50, 379008056, 0.02),
                          # too long time for regular testing
                          # (100, 1866992158, 0.00),
                          # (200, 216771124, 0.00),
                          # (500, 495070989, 0.00)
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
    average_percent_ratio = _percentage_deviation_johnson_problem(
        count_jobs, time_seed, count_problem=10, heuristic=neh_heuristics)

    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('count_jobs, time_seed, expected_percent_ratio',
                         [(20, 873654221, 0.82),
                          (50, 379008056, 0.54),
                          # too long time for regular testing
                          # (100, 1866992158, 0.74),
                          # (200, 216771124, 0.12),
                          # (500, 495070989, 0.08)
                          ])
def test_liu_reeves_heuristic_johnson_problem(count_jobs, time_seed,
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
    average_percent_ratio = _percentage_deviation_johnson_problem(
        count_jobs, time_seed, count_problem=10,
        heuristic=liu_reeves_heuristics, count_sequences=5)

    assert round(average_percent_ratio, 2) == expected_percent_ratio
