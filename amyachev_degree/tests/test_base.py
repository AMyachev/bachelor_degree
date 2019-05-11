import pytest

from amyachev_degree.core import (create_schedule, Jobs, Machines,
                                  JobSchedulingFrame, NaN, Duration)

from amyachev_degree.exact_algorithm import johnson_algorithm
import amyachev_degree.tests.util_testing as tm

frame1 = JobSchedulingFrame([[17, 19, 13], [15, 11, 12],
                             [14, 21, 16], [20, 16, 20],
                             [16, 17, 17]])
test_1 = create_schedule(frame1, [2, 4, 3, 0, 1])
assert test_1.end_time == 114
test_2 = create_schedule(frame1, [4, 2, 3, 0, 1])
assert test_2.end_time == 115

frame2 = JobSchedulingFrame([[2, 3],
                             [8, 3],
                             [4, 6],
                             [9, 5],
                             [6, 8],
                             [9, 7]])
solution1 = johnson_algorithm(frame2)
assert solution1 == [0, 2, 4, 5, 3, 1]
assert create_schedule(frame2, solution1).end_time == 41


def test_NaN():
    assert "NaN" == str(NaN)


def test_duration():
    durat = Duration(machine_index=1, begin_time=0, end_time=10)
    assert 1 == durat.machine_index
    assert 0 == durat.begin_time
    assert 10 == durat.end_time


class TestJobs:

    def test_count_jobs(self):
        assert 5 == Jobs(5).count_jobs


class TestMachines:

    def test_count_machines(self):
        assert 3 == Machines(3).count_machines


class TestJobSchedulingFrame:

    def setup_method(self):
        self.processing_times = [[17, 19, 13], [15, 11, 12],
                                 [14, 21, 16], [20, 16, 20],
                                 [16, 17, 17]]

    @pytest.mark.parametrize('seed', [NaN, 12345])
    def test_initial_seed(self, seed):
        frame = JobSchedulingFrame(self.processing_times, initial_seed=seed)
        assert seed == frame.initial_seed

    @pytest.mark.parametrize('seed', [None, "NaN", 12345.4])
    def test_bad_initial_seed(self, seed):
        msg = 'initial_seed must be the NaN or int'

        with pytest.raises(ValueError, match=msg):
            JobSchedulingFrame(self.processing_times, initial_seed=seed)

    @pytest.mark.parametrize('upper_bound', [NaN, 12345])
    def test_upper_bound(self, upper_bound):
        frame = JobSchedulingFrame(self.processing_times,
                                   upper_bound=upper_bound)
        assert upper_bound == frame.upper_bound

    @pytest.mark.parametrize('upper_bound', [None, "NaN", 12345.4])
    def test_bad_upper_bound(self, upper_bound):
        msg = 'upper_bound must be the NaN or int'

        with pytest.raises(ValueError, match=msg):
            JobSchedulingFrame(self.processing_times, upper_bound=upper_bound)

    def test_count_jobs_and_machines(self):
        frame = JobSchedulingFrame(self.processing_times)

        count_jobs = len(self.processing_times)
        count_machines = len(self.processing_times[0])

        assert frame.count_jobs == count_jobs
        assert frame.count_machines == count_machines

    @pytest.mark.parametrize('processing_times', (None, NaN, 1, [1, 2],
                                                  [[1, 2], [1, 2, 3]]))
    def test_bad_processing_times(self, processing_times):
        msg = 'processing_times must be list of lists of integers; same length'

        with pytest.raises(ValueError, match=msg):
            JobSchedulingFrame(processing_times)

    @pytest.mark.parametrize('idx_job', [0, 1, 2, 3, 4])
    @pytest.mark.parametrize('idx_machine', [0, 1, 2])
    def test_get_processing_time(self, idx_job, idx_machine):
        frame = JobSchedulingFrame(self.processing_times)

        fst_time = self.processing_times[idx_job][idx_machine]
        scnd_time = frame.get_processing_time(idx_job, idx_machine)

        assert fst_time == scnd_time

    @pytest.mark.parametrize('idx_job, idx_machine', [(5, 1), (1, 5), (5, 3)])
    def test_bad_get_processing_time(self, idx_job, idx_machine):
        msg = 'idx_job or idx_machine out of range'
        frame = JobSchedulingFrame(self.processing_times)

        with pytest.raises(IndexError, match=msg):
            frame.get_processing_time(idx_job, idx_machine)

    def test_set_processing_times(self):
        frame = JobSchedulingFrame([[]])
        frame.set_processing_times(self.processing_times)

        expected_frame = JobSchedulingFrame(self.processing_times)

        tm.assert_js_frame(frame, expected_frame)

    def test_str(self):
        taillard_str = ("number of jobs, number of machines, "
                        "initial seed, upper bound and lower bound :\n"
                        "          5           3"
                        "   NaN        NaN        NaN\n"
                        "processing times :\n"
                        "  17  15  14  20  16\n"
                        "  19  11  21  16  17\n"
                        "  13  12  16  20  17\n")

        assert taillard_str == str(JobSchedulingFrame(self.processing_times))
