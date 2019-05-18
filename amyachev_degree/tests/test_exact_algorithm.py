from amyachev_degree.core import create_schedule, JobSchedulingFrame
from amyachev_degree.exact_algorithm import johnson_algorithm


def test_johnson_algorithm():
    frame = JobSchedulingFrame([[2, 3],
                                [8, 3],
                                [4, 6],
                                [9, 5],
                                [6, 8],
                                [9, 7]])
    solution = johnson_algorithm(frame)
    assert solution == [0, 2, 4, 5, 3, 1]

    sch = create_schedule(frame, solution)
    assert sch.end_time() == 41
    # print('\n')
    # print(sch)
