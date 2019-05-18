import os
import pytest

from amyachev_degree.core import create_schedule
from amyachev_degree.io import read_flow_shop_instances
from amyachev_degree.simple_heuristics import palmer_heuristics


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                        [('/20jobs_5machines.txt', 11),
                         ('/20jobs_10machines.txt', 15)])
def test_palmer_heuristics(file_name, expected_percent_ratio):
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = palmer_heuristics(frames[i])
        schedule = create_schedule(frames[i], solution)
        end_time_diff = schedule.end_time() - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio) == expected_percent_ratio
