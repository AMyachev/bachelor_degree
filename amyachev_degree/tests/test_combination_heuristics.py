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
        solution, _ = local_search_partitial_sequence(frame, solution)
        solution, changed = local_search(frame, solution)
        if not changed:
            break
        different_from_init_jobs = True

    return solution, different_from_init_jobs


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


class TestSimpleHeuristicsWithLocalSearch:

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 4.77),
                              ('/20jobs_10machines.txt', 8.43),
                              ('/20jobs_20machines.txt', 7.63),
                              ('/50jobs_5machines.txt', 2.55),
                              # too long time for regular testing
                              # ('/50jobs_10machines.txt', 8.31),
                              # ('/50jobs_20machines.txt', 11.14),
                              # ('/100jobs_5machines.txt', 1.38),
                              # ('/100jobs_10machines.txt', 6.06),
                              # ('/100jobs_20machines.txt', 9.53),
                              # ('/200jobs_10machines.txt', 3.36),
                              # ('/200jobs_20machines.txt', 9.18),
                              # ('/500jobs_20machines.txt', 5.56)
                              ])
    def test_palmer_heuristics_with_local_search(self, file_name,
                                                 expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Flow shop problem.

        Abstract
        --------
        The experiment consists in comparing the results of Palmer's heuristic
        with local search improvements with the best results obtained by many
        researchers for Taillard's Flow shop problems published on the website:
        http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_combination_heuristics.py\
            ::TestSimpleHeuristicsWithLocalSearch\
            ::test_palmer_heuristics_with_local_search`

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
                              ('/20jobs_20machines.txt', 5.93),
                              ('/50jobs_5machines.txt', 3.51),
                              ('/50jobs_10machines.txt', 9.35),
                              # too long time for regular testing
                              # ('/50jobs_20machines.txt', 9.89),
                              # ('/100jobs_5machines.txt', 2.91),
                              # ('/100jobs_10machines.txt', 7.18),
                              # ('/100jobs_20machines.txt', 8.93),
                              # ('/200jobs_10machines.txt', 6.08),
                              # ('/200jobs_20machines.txt', 9.11),
                              # ('/500jobs_20machines.txt', 7.29)
                              ])
    def test_cds_heuristics_with_local_search(self, file_name,
                                              expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Flow shop problem.

        Abstract
        --------
        The experiment consists in comparing the results of CDS heuristic
        with local search improvements with the best results obtained by many
        researchers for Taillard's Flow shop problems published on the website:
        http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_combination_heuristics.py\
            ::TestSimpleHeuristicsWithLocalSearch\
            ::test_cds_heuristics_with_local_search`

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
    def test_neh_heuristics_with_local_search(self, file_name,
                                              expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Flow shop problem.

        Abstract
        --------
        The experiment consists in comparing the results of NEH heuristic
        with local search improvements with the best results obtained by many
        researchers for Taillard's Flow shop problems published on the website:
        http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_combination_heuristics.py\
            ::TestSimpleHeuristicsWithLocalSearch\
            ::test_neh_heuristics_with_local_search`

        All tests run about 5175 sec.

        """
        frames = read_flow_shop_instances(FLOW_SHOP_INSTANCE_DIR + file_name)
        assert len(frames) == 10

        heuristic = make_heuristic_with_local_search(neh_heuristics,
                                                     local_search)

        average_percent_ratio = percentage_deviation_using_upper_bound(
            heuristic, {}, frames)

        assert round(average_percent_ratio, 2) == expected_percent_ratio


class TestSimpleHeuristicsWithCombinationLocalSearches:

    @pytest.mark.parametrize('file_name, expected_percent_ratio',
                             [('/20jobs_5machines.txt', 4.37),
                              ('/20jobs_10machines.txt', 5.83),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 3.88),
                              # ('/50jobs_5machines.txt', 3.61),
                              # ('/50jobs_10machines.txt', 6.86),
                              # ('/50jobs_20machines.txt', 7.20),
                              # ('/100jobs_5machines.txt', 1.3),
                              # ('/100jobs_10machines.txt', 3.79),
                              # ('/100jobs_20machines.txt', 5.54),
                              # ('/200jobs_10machines.txt', _),
                              # ('/200jobs_20machines.txt', _),
                              # ('/500jobs_20machines.txt', _)
                              ])
    def test_palmer_heuristic(self, file_name, expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Flow shop problem.

        Abstract
        --------
        The experiment consists in comparing the results of Palmer's heuristic
        with the improvement of the result developed by the algorithm combining
        varieties of local search with the best results obtained by many
        researchers for Taillard's Flow shop problems published on the website:
        http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_combination_heuristics.py\
            ::TestSimpleHeuristicsWithCombinationLocalSearches\
            ::test_palmer_heuristic`

        First 9 tests run about 1527 sec.
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
                             [('/20jobs_5machines.txt', 4.52),
                              ('/20jobs_10machines.txt', 4.85),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 4.88),
                              # ('/50jobs_5machines.txt', 3.36),
                              # ('/50jobs_10machines.txt', 5.85),
                              # ('/50jobs_20machines.txt', 7.30),
                              # ('/100jobs_5machines.txt', 1.40),
                              # ('/100jobs_10machines.txt', 3.65),
                              # ('/100jobs_20machines.txt', 5.29),
                              # ('/200jobs_10machines.txt', _),
                              # ('/200jobs_20machines.txt', _),
                              # ('/500jobs_20machines.txt', _)
                              ])
    def test_cds_heuristic(self, file_name, expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Flow shop problem.

        Abstract
        --------
        The experiment consists in comparing the results of CDS heuristic
        with the improvement of the result developed by the algorithm combining
        varieties of local search with the best results obtained by many
        researchers for Taillard's Flow shop problems published on the website:
        http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_combination_heuristics.py\
            ::TestSimpleHeuristicsWithCombinationLocalSearches\
            ::test_cds_heuristic`

        First 9 tests run about 1225 sec.
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
                             [('/20jobs_5machines.txt', 3.27),
                              ('/20jobs_10machines.txt', 4.85),
                              # too long time for regular testing
                              # ('/20jobs_20machines.txt', 4.34),
                              # ('/50jobs_5machines.txt', 1.91),
                              # ('/50jobs_10machines.txt', 5.71),
                              # ('/50jobs_20machines.txt', 6.48),
                              # ('/100jobs_5machines.txt', 1.04),
                              # ('/100jobs_10machines.txt', 3.53),
                              # ('/100jobs_20machines.txt', 5.69),
                              # ('/200jobs_10machines.txt', _),
                              # ('/200jobs_20machines.txt', _),
                              # ('/500jobs_20machines.txt', _)
                              ])
    def test_neh_heuristic(self, file_name, expected_percent_ratio):
        """
        Function for research.

        Problem
        -------
        Flow shop problem.

        Abstract
        --------
        The experiment consists in comparing the results of NEH heuristic
        with the improvement of the result developed by the algorithm combining
        varieties of local search with the best results obtained by many
        researchers for Taillard's Flow shop problems published on the website:
        http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html

        Notes
        -----
        Starts as follows (from root folder):
            `pytest amyachev_degree/tests/test_combination_heuristics.py\
            ::TestSimpleHeuristicsWithCombinationLocalSearches\
            ::test_neh_heuristic`

        First 9 tests run about 1454 sec.
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
