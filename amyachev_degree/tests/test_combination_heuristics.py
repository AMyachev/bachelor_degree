import os
import pytest

from amyachev_degree.io import read_flow_shop_instances
from amyachev_degree.core import compute_end_time, JobSchedulingFrame
from amyachev_degree.simple_heuristics import palmer_heuristics
from amyachev_degree.composite_heuristics import (
    local_search, local_search_partitial_sequence
)


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


def combination_local_searches(frame: JobSchedulingFrame,
                               init_jobs: list) -> list:
    while True:
        init_jobs = local_search_partitial_sequence(frame, init_jobs)

        if not local_search(frame, init_jobs):
            break

    return init_jobs


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [# ('/20jobs_5machines.txt', 4.5),
                          # ('/20jobs_10machines.txt', 5.83),
                          # ('/20jobs_20machines.txt', 3.88),
                          # ('/50jobs_5machines.txt', 3.58),
                          # ('/50jobs_10machines.txt', 7.19),
                          # ('/50jobs_20machines.txt', 6.9),
                          # ('/100jobs_5machines.txt', 1.3),
                          # ('/100jobs_10machines.txt', 3.49),
                          # too long time for regular testing
                          ('/100jobs_20machines.txt', 13.44),
                          ('/200jobs_10machines.txt', 5.02),
                          ('/200jobs_20machines.txt', 12.16),
                          ('/500jobs_20machines.txt', 6.76)
                          ])
def test_palmer_heuristic_with_combination_local_searches(
        file_name, expected_percent_ratio):
    # all tests run about _ + 273 + _ = _ sec
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = palmer_heuristics(frames[i])

        solution = combination_local_searches(frames[i], solution)

        schedule_end_time = compute_end_time(frames[i], solution)
        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio
