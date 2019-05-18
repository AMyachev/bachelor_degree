import os
import pytest

from amyachev_degree.core import create_schedule, JobSchedulingFrame
from amyachev_degree.io import read_flow_shop_instances


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


def test_palmer_heuristics():
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR +
                                      "/20jobs_5machines.txt")
    assert len(frames) == 10
