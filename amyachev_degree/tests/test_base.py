import pytest

from amyachev_degree.core import (create_schedule,
                                  JobSchedulingFrame, NaN)

from amyachev_degree.exact_algorithm import johnson_algorithm

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
