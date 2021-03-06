import os
import pytest

from amyachev_degree.io import read_flow_shop_instances
from amyachev_degree.core import compute_end_time, JobSchedulingFrame
from amyachev_degree.simple_heuristics import (
    cds_heuristics, liu_reeves_heuristics, neh_heuristics, palmer_heuristics)

from amyachev_degree.composite_heuristics import (
    local_search, local_search_partitial_sequence)

from amyachev_degree.util.testing import percentage_deviation_using_upper_bound


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TAILLARD_INS_DIR = TEST_DIR + '/../Taillard_instances'
FLOW_SHOP_INSTANCE_DIR = TAILLARD_INS_DIR + '/flow_shop_sequences'


# TODO this function must be replaced to 'composite_heuristics.py'
def combination_local_searches(frame: JobSchedulingFrame,
                               init_jobs: list) -> list:
    solution = init_jobs
    different_from_init_jobs = False

    while True:
        temp, better = local_search_partitial_sequence(frame, solution)
        if better:
            solution = temp

        solution, changed = local_search(frame, solution)
        if not changed:
            break
        different_from_init_jobs = True

    return solution, different_from_init_jobs


# TODO make doc-string
def make_heuristic_with_local_search(heuristic: object,
                                     func_search: object) -> object:

    def heuristic_with_local_search(*args, **kwargs):
        solution = heuristic(*args, **kwargs)

        try:
            frame = kwargs['frame']
        except KeyError:
            frame = args[0]

        solution, _ = func_search(frame, solution)
        return solution

    return heuristic_with_local_search


class TestHeuristicsWithLocalSearch:
    """
    Class for research.

    Problem
    -------
    Flow shop.

    Abstract
    --------
    The experiment consists in comparing the results of heuristics
    with local search improvements with the best results obtained by many
    researchers for Taillard's Flow shop problems published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_combination_heuristics.py\
        ::TestHeuristicsWithLocalSearch`

    """

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 4.77),
                              ('/20jobs_10machines.txt', 8.43),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 7.63),
                              # ('/50jobs_5machines.txt', 2.55),
                              # ('/50jobs_10machines.txt', 8.31),
                              # ('/50jobs_20machines.txt', 11.14),
                              # ('/100jobs_5machines.txt', 1.38),
                              # ('/100jobs_10machines.txt', 6.06),
                              # ('/100jobs_20machines.txt', 9.53),
                              # ('/200jobs_10machines.txt', 3.36),
                              # ('/200jobs_20machines.txt', 9.18),
                              # ('/500jobs_20machines.txt', 5.56)
                              ])
    def test_palmer_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 25 sec.
        All tests run about 526 sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(palmer_heuristics,
                                                     local_search)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 5.12),
                              ('/20jobs_10machines.txt', 8.65),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 5.93),
                              # ('/50jobs_5machines.txt', 3.51),
                              # ('/50jobs_10machines.txt', 9.35),
                              # too long time for regular testing
                              # ('/50jobs_20machines.txt', 9.89),
                              # ('/100jobs_5machines.txt', 2.91),
                              # ('/100jobs_10machines.txt', 7.18),
                              # ('/100jobs_20machines.txt', 8.93),
                              # ('/200jobs_10machines.txt', 6.08),
                              # ('/200jobs_20machines.txt', 9.11),
                              # ('/500jobs_20machines.txt', 7.29)
                              ])
    def test_cds_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 28 sec.
        All tests run about 408 sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(cds_heuristics,
                                                     local_search)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 2.84),
                              ('/20jobs_10machines.txt', 4.47),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 3.49),
                              # ('/50jobs_5machines.txt', 0.67),
                              # ('/50jobs_10machines.txt', 4.2),
                              # ('/50jobs_20machines.txt', 5.66),
                              # ('/100jobs_5machines.txt', 0.47),
                              # ('/100jobs_10machines.txt', 2.04),
                              # ('/100jobs_20machines.txt', 4.12),
                              # ('/200jobs_10machines.txt', 1.16),
                              # ('/200jobs_20machines.txt', 3.14),
                              # ('/500jobs_20machines.txt', 1.68)
                              ])
    def test_neh_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 85 sec.
        All tests run about 5175 sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(neh_heuristics,
                                                     local_search)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio


class TestHeuristicsWithLocalSearchPartitialSequence:
    """
    Class for research.

    Problem
    -------
    Flow shop.

    Abstract
    --------
    The experiment consists in comparing the results of heuristics with local
    search using partitial sequence improvements with the best results obtained
    by many researchers for Taillard's Flow shop problems
    published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_combination_heuristics.py\
        ::TestHeuristicsWithLocalSearchPartitialSequence`

    """

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 6.08),
                              ('/20jobs_10machines.txt', 7.14),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 4.91),
                              # ('/50jobs_5machines.txt', 7.72),
                              # ('/50jobs_10machines.txt', 8.24),
                              # ('/50jobs_20machines.txt', 8.35),
                              # ('/100jobs_5machines.txt', 11.82),
                              # ('/100jobs_10machines.txt', 7.11),
                              # ('/100jobs_20machines.txt', 7.2),
                              # ('/200jobs_10machines.txt', 3.36),
                              # ('/200jobs_20machines.txt', 9.18),
                              # ('/500jobs_20machines.txt', 5.56)
                              ])
    def test_palmer_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 78 sec.
        All tests run about _ sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(
            palmer_heuristics, local_search_partitial_sequence)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 6.76),
                              ('/20jobs_10machines.txt', 6.53),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 4.52),
                              # ('/50jobs_5machines.txt', 6.74),
                              # ('/50jobs_10machines.txt', 7.02),
                              # ('/50jobs_20machines.txt', 8.04),
                              # ('/100jobs_5machines.txt', 5.12),
                              # ('/100jobs_10machines.txt', 5.95),
                              # ('/100jobs_20machines.txt', 6.24),
                              # ('/200jobs_10machines.txt', 3.36),
                              # ('/200jobs_20machines.txt', 9.18),
                              # ('/500jobs_20machines.txt', 5.56)
                              ])
    def test_cds_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 75 sec.
        All tests run about _ sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(
            cds_heuristics, local_search_partitial_sequence)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 4.69),
                              ('/20jobs_10machines.txt', 9.62),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 7.52),
                              # ('/50jobs_5machines.txt', 4.64),
                              # ('/50jobs_10machines.txt', 9.61),
                              # ('/50jobs_20machines.txt', 8.57),
                              # ('/100jobs_5machines.txt', 3.87),
                              # ('/100jobs_10machines.txt', 6.01),
                              # ('/100jobs_20machines.txt', 6.71),
                              # ('/200jobs_10machines.txt', 3.36),
                              # ('/200jobs_20machines.txt', 9.18),
                              # ('/500jobs_20machines.txt', 5.56)
                              ])
    def test_neh_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 151 sec.
        All tests run about _ sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(
            neh_heuristics, local_search_partitial_sequence)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio


class TestHeuristicsWithCombinationLocalSearches:
    """
    Class for research.

    Problem
    -------
    Flow shop problem.

    Abstract
    --------
    The experiment consists in comparing the results of heuristics
    with the improvement of the result developed by the algorithm combining
    varieties of local search with the best results obtained by many
    researchers for Taillard's Flow shop problems published on the website:
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

    Notes
    -----
    Starts as follows (from root folder):
        `pytest amyachev_degree/tests/test_combination_heuristics.py\
        ::TestHeuristicsWithCombinationLocalSearches`

    """

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 2.94),
                              ('/20jobs_10machines.txt', 5.73),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 3.78),
                              # ('/50jobs_5machines.txt', 2.02),
                              # ('/50jobs_10machines.txt', 5.70),
                              # ('/50jobs_20machines.txt', 6.43),
                              # ('/100jobs_5machines.txt', 1.38),
                              # ('/100jobs_10machines.txt', 3.07),
                              # ('/100jobs_20machines.txt', 4.78),
                              # ('/200jobs_10machines.txt', _),
                              # ('/200jobs_20machines.txt', _),
                              # ('/500jobs_20machines.txt', _)
                              ])
    def test_palmer_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 230 sec.
        All tests run about _ sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(
            palmer_heuristics, combination_local_searches)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 4.07),
                              ('/20jobs_10machines.txt', 4.82),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 4.34),
                              # ('/50jobs_5machines.txt', 2.80),
                              # ('/50jobs_10machines.txt', 5.52),
                              # ('/50jobs_20machines.txt', 6.28),
                              # ('/100jobs_5machines.txt', 2.19),
                              # ('/100jobs_10machines.txt', 3.95),
                              # ('/100jobs_20machines.txt', 5.16),
                              # ('/200jobs_10machines.txt', _),
                              # ('/200jobs_20machines.txt', _),
                              # ('/500jobs_20machines.txt', _)
                              ])
    def test_cds_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 190 sec.
        All tests run about _ sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(
            cds_heuristics, combination_local_searches)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 2.46),
                              ('/20jobs_10machines.txt', 4.29),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 3.52),
                              # ('/50jobs_5machines.txt', 0.61),
                              # ('/50jobs_10machines.txt', 4.20),
                              # ('/50jobs_20machines.txt', 5.41),
                              # ('/100jobs_5machines.txt', 0.47),
                              # ('/100jobs_10machines.txt', 1.99),
                              # ('/100jobs_20machines.txt', 3.88),
                              # ('/200jobs_10machines.txt', _),
                              # ('/200jobs_20machines.txt', _),
                              # ('/500jobs_20machines.txt', _)
                              ])
    def test_neh_heuristic(self, file_name, expected_percent_ratio):
        """
        Results
        -------
        First 9 tests run about 222 sec.
        All tests run about _ sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(
            neh_heuristics, combination_local_searches)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio


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
