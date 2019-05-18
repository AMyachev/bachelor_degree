import os

from amyachev_degree.core import create_schedule
from amyachev_degree.io import read_flow_shop_instances
from amyachev_degree.simple_heuristics import palmer_heuristics


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


def test_palmer_heuristics():
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR +
                                      "/20jobs_5machines.txt")
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = palmer_heuristics(frames[i])
        schedule = create_schedule(frames[i], solution)
        end_time_diff = schedule.end_time() - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    assert round(sum(solutions_ratio) / len(solutions_ratio) * 100) == 11
