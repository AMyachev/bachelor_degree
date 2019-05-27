import os
import pytest

from amyachev_degree.core import compute_end_time, JobSchedulingFrame
from amyachev_degree.io import read_flow_shop_instances
from amyachev_degree.simple_heuristics import (
    cds_create_proc_times, cds_heuristics, fgh_heuristic,
    liu_reeves_heuristics, neh_heuristics, palmer_heuristics,
    slope_index_func)
from amyachev_degree.composite_heuristics import local_search
from amyachev_degree.util.testing import assert_js_frame


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


# TODO a long run test optional instead of using comments


@pytest.mark.parametrize('idx_job, slope_index', [(0, -8), (1, -6), (2, 4),
                                                  (3, 0), (4, 2)])
def test_slope_index(idx_job, slope_index):
    processing_times = [[17, 19, 13], [15, 11, 12],
                        [14, 21, 16], [20, 16, 20], [16, 17, 17]]
    frame = JobSchedulingFrame(processing_times)

    assert slope_index == slope_index_func(frame, idx_job)


def test_cds_create_proc_times():
    processing_times = [[17, 19, 13], [15, 11, 12],
                        [14, 21, 16], [20, 16, 20], [16, 17, 17]]
    frame = JobSchedulingFrame(processing_times)
    johnson_frame = JobSchedulingFrame([[]])

    # sub problem index begin with 1
    processing_times_first = cds_create_proc_times(frame, 1)
    johnson_frame.set_processing_times(processing_times_first)

    assert_js_frame(johnson_frame, JobSchedulingFrame([[17, 13], [15, 12],
                                                       [14, 16], [20, 20],
                                                       [16, 17]]))

    processing_times_second = cds_create_proc_times(frame, 2)
    johnson_frame.set_processing_times(processing_times_second)

    assert_js_frame(johnson_frame, JobSchedulingFrame([[36, 32], [26, 23],
                                                       [35, 37], [36, 36],
                                                       [33, 34]]))


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 10.81),
                          ('/20jobs_10machines.txt', 15.27),
                          ('/20jobs_20machines.txt', 16.34),
                          ('/50jobs_5machines.txt', 5.34),
                          ('/50jobs_10machines.txt', 13.49),
                          ('/50jobs_20machines.txt', 15.46),
                          ('/100jobs_5machines.txt', 2.33),
                          ('/100jobs_10machines.txt', 9.09),
                          # too long time for regular testing
                          # ('/100jobs_20machines.txt', 13.44),
                          # ('/200jobs_10machines.txt', 5.02),
                          # ('/200jobs_20machines.txt', 12.16),
                          # ('/500jobs_20machines.txt', 6.76)
                          ])
def test_palmer_heuristics(file_name, expected_percent_ratio):
    """
    Function for research.

    Problem
    -------
    Flow shop problem.

    Abstract
    --------
    The experiment consists in comparing the results of Palmer's heuristic
    with the best results obtained by many researchers for Taillard's Flow shop
    problems published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_simple_heuristics.py\
            ::test_palmer_heuristics`

    All tests run about 1.58 sec.

    """
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = palmer_heuristics(frames[i])
        schedule_end_time = compute_end_time(frames[i], solution)

        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 9.55),
                          ('/20jobs_10machines.txt', 12.12),
                          ('/20jobs_20machines.txt', 9.72),
                          ('/50jobs_5machines.txt', 6.57),
                          ('/50jobs_10machines.txt', 12.45),
                          # too long time for regular testing
                          # ('/50jobs_20machines.txt', 13.51),
                          # ('/100jobs_5machines.txt', 4.79),
                          # ('/100jobs_10machines.txt', 9.19),
                          # ('/100jobs_20machines.txt', 12.11),
                          # ('/200jobs_10machines.txt', 7.32),
                          # ('/200jobs_20machines.txt', 11.16),
                          # ('/500jobs_20machines.txt', 8.20)
                          ])
def test_cds_heuristics(file_name, expected_percent_ratio):
    """
    Function for research.

    Problem
    -------
    Flow shop problem.

    Abstract
    --------
    The experiment consists in comparing the results of CDS heuristic
    with the best results obtained by many researchers for Taillard's Flow shop
    problems published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_simple_heuristics.py\
            ::test_cds_heuristics`

    All tests run about 5.24 sec.

    """
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = cds_heuristics(frames[i])
        schedule_end_time = compute_end_time(frames[i], solution)

        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 3.25),
                          ('/20jobs_10machines.txt', 4.59),
                          # too long time for regular testing
                          # ('/20jobs_20machines.txt', 3.73),
                          # ('/50jobs_5machines.txt', 0.73),
                          # ('/50jobs_10machines.txt', 4.57),
                          # ('/50jobs_20machines.txt', 6.06),
                          # ('/100jobs_5machines.txt', 0.48),
                          # ('/100jobs_10machines.txt', 2.17),
                          # ('/100jobs_20machines.txt', 4.28),
                          # ('/200jobs_10machines.txt', 1.23),
                          # ('/200jobs_20machines.txt', 3.33),
                          # ('/500jobs_20machines.txt', 1.73)
                          ])
def test_neh_heuristics(file_name, expected_percent_ratio):
    """
    Function for research.

    Problem
    -------
    Flow shop problem.

    Abstract
    --------
    The experiment consists in comparing the results of NEH heuristic
    with the best results obtained by many researchers for Taillard's Flow shop
    problems published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_simple_heuristics.py\
            ::test_neh_heuristics`

    All tests run about 5154 sec.

    """
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = neh_heuristics(frames[i])
        schedule_end_time = compute_end_time(frames[i], solution)

        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 7.96),
                          ('/20jobs_10machines.txt', 11.99),
                          # too long time for regular testing
                          # ('/20jobs_20machines.txt', 13.36),
                          # ('/50jobs_5machines.txt', 5.28),
                          # ('/50jobs_10machines.txt', 11.62),
                          # ('/50jobs_20machines.txt', 14.15),
                          # ('/100jobs_5machines.txt', 2.53),
                          # ('/100jobs_10machines.txt', 6.35),
                          # ('/100jobs_20machines.txt', 13.55),
                          # ('/200jobs_10machines.txt', 4.03),
                          # ('/200jobs_20machines.txt', 10.58),

                          # TODO fix expected_percent_ratio
                          # ('/500jobs_20machines.txt', 7)
                          ])
def test_liu_reeves_heuristics(file_name, expected_percent_ratio):
    """
    Function for research.

    Problem
    -------
    Flow shop problem.

    Abstract
    --------
    The experiment consists in comparing the results of LR(5) heuristic
    with the best results obtained by many researchers for Taillard's Flow shop
    problems published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_simple_heuristics.py\
            ::test_liu_reeves_heuristics`

    All tests run > 40000 sec. (problem: 500x20 run > 36000 sec)

    """
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = liu_reeves_heuristics(frames[i], 5)
        schedule_end_time = compute_end_time(frames[i], solution)

        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 2),
                          ('/20jobs_10machines.txt', 3),
                          # too long time for regular testing
                          # ('/20jobs_20machines.txt', 4),
                          # ('/50jobs_5machines.txt', 1),
                          # ('/50jobs_10machines.txt', 5),
                          # ('/50jobs_20machines.txt', 6),
                          # ('/100jobs_5machines.txt', 0),
                          # ('/100jobs_10machines.txt', 2),
                          # ('/100jobs_20machines.txt', 4),
                          # ('/200jobs_10machines.txt', 1),
                          # ('/200jobs_20machines.txt', 3),
                          # ('/500jobs_20machines.txt', 2)
                          ])
def test_fgh_heuristic(file_name, expected_percent_ratio):
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        # TODO need a way to automatically define `count_alpha` variable
        solution = fgh_heuristic(frames[i], count_alpha=11)
        schedule_end_time = compute_end_time(frames[i], solution)
        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


# heuristics with local search ###############################################
@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 4.77),
                          ('/20jobs_10machines.txt', 8.43),
                          ('/20jobs_20machines.txt', 7.63),
                          ('/50jobs_5machines.txt', 2.55),
                          # too long time for regular testing
                          # ('/50jobs_10machines.txt', 8),
                          # ('/50jobs_20machines.txt', 11),
                          # ('/100jobs_5machines.txt', 1),
                          # ('/100jobs_10machines.txt', 6),
                          # ('/100jobs_20machines.txt', 10),
                          # ('/200jobs_10machines.txt', 3),
                          # ('/200jobs_20machines.txt', 9),
                          # ('/500jobs_20machines.txt', 6)
                          ])
def test_palmer_heuristics_with_local_search(file_name,
                                             expected_percent_ratio):
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        # TODO local search can be decorator
        solution = palmer_heuristics(frames[i])
        local_search(frames[i], solution)
        schedule_end_time = compute_end_time(frames[i], solution)
        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 5),
                          ('/20jobs_10machines.txt', 9),
                          ('/20jobs_20machines.txt', 6),
                          ('/50jobs_5machines.txt', 4),
                          ('/50jobs_10machines.txt', 9),
                          # too long time for regular testing
                          # ('/50jobs_20machines.txt', 10),
                          # ('/100jobs_5machines.txt', 3),
                          # ('/100jobs_10machines.txt', 7),
                          # ('/100jobs_20machines.txt', 9),
                          # ('/200jobs_10machines.txt', 6),
                          # ('/200jobs_20machines.txt', 9),
                          # ('/500jobs_20machines.txt', 7)
                          ])
def test_cds_heuristics_with_local_search(file_name, expected_percent_ratio):
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = cds_heuristics(frames[i])
        local_search(frames[i], solution)
        schedule_end_time = compute_end_time(frames[i], solution)
        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio


@pytest.mark.parametrize('file_name, expected_percent_ratio',
                         [('/20jobs_5machines.txt', 3),
                          ('/20jobs_10machines.txt', 4),
                          # too long time for regular testing
                          # ('/20jobs_20machines.txt', 3),
                          # ('/50jobs_5machines.txt', 1),
                          # ('/50jobs_10machines.txt', 4),
                          # ('/50jobs_20machines.txt', 6),
                          # ('/100jobs_5machines.txt', 0),
                          # ('/100jobs_10machines.txt', 2),
                          # ('/100jobs_20machines.txt', 4),
                          # ('/200jobs_10machines.txt', 1),
                          # ('/200jobs_20machines.txt', 3),
                          # ('/500jobs_20machines.txt', 2)
                          ])
def test_neh_heuristics_with_local_search(file_name, expected_percent_ratio):
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
    assert len(frames) == 10

    solutions_ratio = []
    for i in range(10):
        solution = neh_heuristics(frames[i])
        local_search(frames[i], solution)
        schedule_end_time = compute_end_time(frames[i], solution)
        end_time_diff = schedule_end_time - frames[i].upper_bound
        solutions_ratio.append(end_time_diff / frames[i].upper_bound)

    average_percent_ratio = sum(solutions_ratio) / len(solutions_ratio) * 100
    assert round(average_percent_ratio, 2) == expected_percent_ratio
###############################################################################


# for research interests
def test_difference():
    frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR
                                      + '/20jobs_5machines.txt')
    frame = frames[0]

    palmer_solution = palmer_heuristics(frame)
    local_search(frame, palmer_solution)
    print("\npalmer solution: ", palmer_solution, "\npalmer end time: %s\n\n"
          % str(compute_end_time(frame, palmer_solution)))

    cds_solution = cds_heuristics(frame)
    local_search(frame, cds_solution)
    print("cds solution: ", cds_solution, "\ncds end time: %s\n\n"
          % str(compute_end_time(frame, cds_solution)))

    neh_solution = neh_heuristics(frame)
    local_search(frame, neh_solution)
    print("neh solution: ", neh_solution, "\nneh end time: %s\n\n"
          % str(compute_end_time(frame, neh_solution)))

    liu_solution = liu_reeves_heuristics(frame, 20)
    local_search(frame, liu_solution)
    print("liu solution: ", liu_solution, "\nliu end time: %s\n\n"
          % str(compute_end_time(frame, liu_solution)))

# TODO to make a local search in a separate script
