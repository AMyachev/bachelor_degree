import pytest

from amyachev_degree.core import (create_schedule, Jobs, Machines,
                                  JobSchedulingFrame, NaN, Duration,
                                  Schedule, flow_job_generator,
                                  johnson_three_machines_generator)

from amyachev_degree.exact_algorithm import johnson_algorithm
import amyachev_degree.util.testing as tm


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


class TestSchedule:

    def setup_method(self):
        self.schedule_dict = {18: [(0, 0, 43), (1, 43, 134), (2, 134, 145)],
                              13: [(0, 43, 83), (1, 134, 141), (2, 145, 158)],
                              5: [(0, 83, 138), (1, 141, 205), (2, 205, 225)]}
        self.end_time = 225

        for durations in self.schedule_dict.values():
            for idx, duration_tuple in enumerate(durations):
                durations[idx] = Duration(*duration_tuple)

        self.schedule = Schedule(self.schedule_dict, self.end_time)

    @pytest.mark.parametrize('expect_end_time, idx_job, idx_machine',
                             [(225, None, None), (158, 13, None),
                              (205, None, 1), (141, 13, 1)])
    def test_end_time(self, expect_end_time, idx_job, idx_machine):
        assert expect_end_time == self.schedule.end_time(idx_job, idx_machine)

    @pytest.mark.parametrize('end_time', [None, NaN, "NaN", 123.09, []])
    def test_bad_end_time(self, end_time):
        msg = 'end_time must be a integer'

        with pytest.raises(ValueError, match=msg):
            Schedule(self.schedule_dict, end_time)

    def test__str__(self):
        schedule_str = ("18: (0, 43), (43, 134), (134, 145),\n"
                        "13: (43, 83), (134, 141), (145, 158),\n"
                        "5: (83, 138), (141, 205), (205, 225),\n")

        assert schedule_str == str(self.schedule)

    def test_jobs(self):
        assert self.schedule_dict.keys() == self.schedule.jobs

    def test_process_times(self):
        for idx_job, original_proc_times in self.schedule_dict.items():
            assert original_proc_times == self.schedule.process_times(idx_job)


class TestFlowJobGenerator:

    @pytest.mark.parametrize('count_jobs', [1, 100])
    @pytest.mark.parametrize('count_machines', [1, 20])
    @pytest.mark.parametrize('initial_seed', [None, "NaN", 123.09, []])
    def test_bad_initial_seed(self, count_jobs, count_machines, initial_seed):
        msg = 'initial_seed must be a integer'

        with pytest.raises(ValueError, match=msg):
            flow_job_generator(count_jobs, count_machines, initial_seed)

    @pytest.mark.parametrize('count_jobs, count_machines',
                             [(-1, 5), (5, -1), (-1, -1)])
    def test_bad_count_jobs_machines(self, count_jobs, count_machines):
        msg = 'count_jobs and count_machines must be greater than zero'

        with pytest.raises(ValueError, match=msg):
            flow_job_generator(count_jobs, count_machines)

    @pytest.mark.parametrize('count_jobs', [1, 2, 5, 100])
    @pytest.mark.parametrize('count_machines', [1, 2, 5, 20])
    def test_count_jobs_and_machines(self, count_jobs, count_machines):
        frame = flow_job_generator(count_jobs, count_machines)

        assert count_jobs == frame.count_jobs
        assert count_machines == frame.count_machines

    @pytest.mark.parametrize('count_jobs', [1, 2, 5])
    @pytest.mark.parametrize('count_machines', [1, 2])
    def test_nan_initial_seed(self, count_jobs, count_machines):
        frame1 = flow_job_generator(count_jobs, count_machines)
        frame2 = flow_job_generator(count_jobs, count_machines,
                                    frame1.initial_seed)

        tm.assert_js_frame(frame1, frame2)

    @pytest.mark.parametrize('initial_seed', [1, 12, 123, 1234])
    def test_initial_seed(self, initial_seed):
        frame = flow_job_generator(count_jobs=5, count_machines=3,
                                   initial_seed=initial_seed)

        assert initial_seed == frame.initial_seed


class TestFlowJobThreeMachinesGenerator:

    @pytest.mark.parametrize('count_jobs', [1, 100])
    @pytest.mark.parametrize('initial_seed', [None, "NaN", 123.09, []])
    def test_bad_initial_seed(self, count_jobs, initial_seed):
        msg = 'initial_seed must be a integer'

        with pytest.raises(ValueError, match=msg):
            johnson_three_machines_generator(count_jobs, initial_seed)

    def test_bad_count_jobs_machines(self):
        msg = 'count_jobs must be greater than zero'

        with pytest.raises(ValueError, match=msg):
            johnson_three_machines_generator(count_jobs=-1)

    @pytest.mark.parametrize('count_jobs', [1, 2, 5, 100])
    def test_count_jobs_and_machines(self, count_jobs):
        frame = johnson_three_machines_generator(count_jobs)

        assert count_jobs == frame.count_jobs
        assert 3 == frame.count_machines

    @pytest.mark.parametrize('count_jobs', [1, 2, 5])
    def test_nan_initial_seed(self, count_jobs):
        frame1 = johnson_three_machines_generator(count_jobs)
        frame2 = johnson_three_machines_generator(count_jobs,
                                                  frame1.initial_seed)

        tm.assert_js_frame(frame1, frame2)

    @pytest.mark.parametrize('initial_seed', [1, 12, 123, 1234])
    def test_initial_seed(self, initial_seed):
        frame = johnson_three_machines_generator(count_jobs=5,
                                                 initial_seed=initial_seed)

        assert initial_seed == frame.initial_seed

    def test_special_property(self):
        frame = johnson_three_machines_generator(count_jobs=2)

        min_proc_time1 = min([frame.get_processing_time(idx_job, 0)
                              for idx_job in range(frame.count_jobs)])
        max_proc_time = max([frame.get_processing_time(idx_job, 1)
                             for idx_job in range(frame.count_jobs)])
        min_proc_time2 = min([frame.get_processing_time(idx_job, 2)
                              for idx_job in range(frame.count_jobs)])

        assert min_proc_time1 > max_proc_time
        assert min_proc_time2 > max_proc_time


class TestScheduleCreate:

    def setup_method(self):
        self.frame1 = JobSchedulingFrame([[17, 19, 13], [15, 11, 12],
                                          [14, 21, 16], [20, 16, 20],
                                          [16, 17, 17]])
        self.frame1_solution1 = [2, 4, 3, 0, 1]
        self.end_time_f1_s1 = 114
        self.str_f1_s1 = ('2: (0, 14), (14, 35), (35, 51),\n'
                          '4: (14, 30), (35, 52), (52, 69),\n'
                          '3: (30, 50), (52, 68), (69, 89),\n'
                          '0: (50, 67), (68, 87), (89, 102),\n'
                          '1: (67, 82), (87, 98), (102, 114),\n')

        self.str_f1_s1_1machine = ('2: (0, 14),\n'
                                   '4: (14, 30),\n'
                                   '3: (30, 50),\n'
                                   '0: (50, 67),\n'
                                   '1: (67, 82),\n')

        self.frame1_solution2 = [4, 2, 3, 0, 1]
        self.end_time_f1_s2 = 115

        self.str_f1_s2 = ('4: (0, 16), (16, 33), (33, 50),\n'
                          '2: (16, 30), (33, 54), (54, 70),\n'
                          '3: (30, 50), (54, 70), (70, 90),\n'
                          '0: (50, 67), (70, 89), (90, 103),\n'
                          '1: (67, 82), (89, 100), (103, 115),\n')

    def test_create_schedule(self):
        sch = create_schedule(self.frame1, self.frame1_solution1)
        assert sch.end_time() == self.end_time_f1_s1
        assert str(sch) == self.str_f1_s1

        sch2 = create_schedule(self.frame1, self.frame1_solution2)
        assert sch2.end_time() == self.end_time_f1_s2
        assert str(sch2) == self.str_f1_s2

    @pytest.mark.parametrize('count_job, end_time', [(1, 51),
                                                     (3, 89),
                                                     (5, 114)])
    def test_create_schedule_with_count_job(self, count_job, end_time):
        sch = create_schedule(self.frame1, self.frame1_solution1, count_job)
        assert sch.end_time() == end_time
        assert self.str_f1_s1.startswith(str(sch))

    def test_create_schedule_with_count_machine(self):
        sch = create_schedule(self.frame1,
                              self.frame1_solution1,
                              count_machine=self.frame1.count_machines)
        assert sch.end_time() == self.end_time_f1_s1
        assert self.str_f1_s1.startswith(str(sch))

        sch2 = create_schedule(self.frame1,
                               self.frame1_solution1,
                               count_machine=1)
        assert sch2.end_time() == 82


frame2 = JobSchedulingFrame([[2, 3],
                             [8, 3],
                             [4, 6],
                             [9, 5],
                             [6, 8],
                             [9, 7]])
solution1 = johnson_algorithm(frame2)
assert solution1 == [0, 2, 4, 5, 3, 1]
assert create_schedule(frame2, solution1).end_time() == 41
