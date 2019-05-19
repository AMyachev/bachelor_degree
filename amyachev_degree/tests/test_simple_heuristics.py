import os
import pytest

from amyachev_degree.core import create_schedule
from amyachev_degree.io import read_flow_shop_instances
from amyachev_degree.simple_heuristics import cds_heuristics, palmer_heuristics


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 11),
                          ('/20jobs_10machines.txt', 15),
                          ('/20jobs_20machines.txt', 16),
                          ('/50jobs_5machines.txt', 5),
                          ('/50jobs_10machines.txt', 13),
                          ('/50jobs_20machines.txt', 15),
                          ('/100jobs_5machines.txt', 2),
                          ('/100jobs_10machines.txt', 9),
                          ('/100jobs_20machines.txt', 13),
                          ('/200jobs_10machines.txt', 5),
                          ('/200jobs_20machines.txt', 12),
                          ('/500jobs_20machines.txt', 7)])
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


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 10),
                          ('/20jobs_10machines.txt', 12),
                          ('/20jobs_20machines.txt', 10),
                          ('/50jobs_5machines.txt', 7),
                          ('/50jobs_10machines.txt', 12),
                          ('/50jobs_20machines.txt', 14),
                          ('/100jobs_5machines.txt', 5),
                          ('/100jobs_10machines.txt', 9),
                          ('/100jobs_20machines.txt', 12),
                          ('/200jobs_10machines.txt', 7),
                          ('/200jobs_20machines.txt', 11),
                          ('/500jobs_20machines.txt', 8)])
def test_cds_heuristics(file_name, expected_percent_ratio):
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = cds_heuristics(frames[i])
        schedule = create_schedule(frames[i], solution)
        end_time_diff = schedule.end_time() - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio) == expected_percent_ratio
