import time
import random as rd
from collections import namedtuple
from typing import Union


Duration = namedtuple('Duration', ['machine_index', 'begin_time', 'end_time'])


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class _NaN(metaclass=Singleton):
    def __str__(self):
        return "NaN"


NaN = _NaN()  # there is only one instance


class Jobs:

    def __init__(self, count_job):
        self._count_jobs = count_job

    @property
    def count_jobs(self):
        return self._count_jobs


class Machines:

    def __init__(self, count_machines):
        self._count_machines = count_machines

    @property
    def count_machines(self):
        return self._count_machines


class Schedule(object):

    def __init__(self, jobs_duration_times: dict, end_time: int):
        """
        Create Schedule instance.

        Parameters
        ----------
        jobs_duration_times: dict
            keys - jobs indexes; value - list of Duration objects
        end_time: int
        """
        self._jobs_duration_times = jobs_duration_times

        if not isinstance(end_time, int):
            raise ValueError('end_time must be a integer')
        self._end_time = end_time

    @property
    def jobs(self) -> list:
        """
        Returns job indexes in Schedule.

        Returns
        -------
        : list[int]
        """
        return self._jobs_duration_times.keys()

    def __str__(self) -> str:
        """
        Example:
            18: (0, 43), (43, 134), (134, 145), (145, 158), (158, 238),
            13: (43, 83), (134, 141), (145, 158), (158, 181), (238, 247),
            5: (83, 138), (141, 205), (205, 225), (225, 234), (247, 345),
            19: (138, 188), (205, 242), (242, 247), (247, 345), (345, 417),
            2: (188, 215), (242, 286), (286, 350), (350, 397), (417, 478),

        Returns
        -------
        : str
        """
        string = ""
        for idx_job, list_durat in self._jobs_duration_times.items():
            string += "%s:" % idx_job
            for durat in list_durat:
                string += " (%s, %s)," % (durat.begin_time, durat.end_time)
            string += "\n"
        return string

    def end_time(self, idx_job: int = None, idx_machine: int = None) -> int:
        """
        By default computes time of completion of all jobs.

        If a job index and a machine index are specified then
        computes the completion time of `idx_job` on `idx_machine`.

        If only a job index is specified
        then computes the completion time of `idx_job` on the last machine.

        If only a machine index is specified
        then computes the completion time at which the last job
        was completed on the `idx_machine`.

        Returns
        -------
        : int
        """
        if idx_machine is None and idx_job is None:
            return self._end_time
        elif idx_machine is not None and idx_job is None:
            last_idx_job = list(self._jobs_duration_times.keys())[-1]
            last_job_duration_time = self._jobs_duration_times[last_idx_job]
            return last_job_duration_time[idx_machine].end_time
        elif idx_machine is None and idx_job is not None:
            return self._jobs_duration_times[idx_job][-1].end_time

        return self._jobs_duration_times[idx_job][idx_machine].end_time

    def process_times(self, idx_job: int) -> list:
        """
        Returns list of processing times of `idx_job` on all machines.

        Parameters
        ----------
        idx_job: int

        Returns
        -------
        : list
        """
        return self._jobs_duration_times[idx_job]


class JobSchedulingFrame:

    def __init__(self, processing_times, upper_bound=NaN, initial_seed=NaN):
        """
        Creates frame from matrix of processing times.

        `processing_times` - matrix N x M,
        N - count of jobs, M - count of machines.

        Parameters
        ----------
        processing_times: list of lists of integers
            can be empty
        upper_bound: int or NaN
        initial_seed: int or NaN
        """
        self.set_processing_times(processing_times)

        if not upper_bound == NaN and not isinstance(upper_bound, int):
            raise ValueError('upper_bound must be the NaN or int')
        self._upper_bound = upper_bound

        if not initial_seed == NaN and not isinstance(initial_seed, int):
            raise ValueError('initial_seed must be the NaN or int')
        self._initial_seed = initial_seed

    def _check_processing_times(self, proc_times):
        try:
            length = len(proc_times[0])  # must be the same for all jobs
            for job_proc_times in proc_times:
                if length != len(job_proc_times):
                    raise
        except Exception:
            raise ValueError('processing_times must be '
                             'list of lists of integers; same length')

    @property
    def initial_seed(self):
        return self._initial_seed

    @property
    def upper_bound(self):
        return self._upper_bound

    @property
    def copy_proc_time(self):
        import copy
        return copy.copy(self.processing_times)

    @property
    def count_jobs(self):
        return self.jobs.count_jobs

    @property
    def count_machines(self):
        return self.machines.count_machines

    def get_processing_time(self, idx_job, idx_machine):
        """
        Returns processing time `idx_job` on `idx_machine`.

        Parameters
        ----------
        idx_job: int
        idx_machine: int

        Returns
        -------
        processing_time: int

        """
        return self.processing_times[idx_job][idx_machine]

    # TODO make test for this functionality
    def get_sum_processing_time(self, idx_job):
        proc_time = 0
        for m in range(self.count_machines):
            proc_time += self.get_processing_time(idx_job, m)

        return proc_time

    def set_processing_times(self, processing_times):
        # raise ValueError if wrong type
        self._check_processing_times(processing_times)

        self.processing_times = processing_times
        self.jobs = Jobs(len(processing_times))
        self.machines = Machines(len(processing_times[0]))

    def __str__(self):
        taillard_pattern = ("number of jobs, number of machines, "
                            "initial seed, upper bound and lower bound :\n"
                            "          %s           %s"
                            "   %s        %s        NaN\n"
                            "processing times :\n%s")
        processing_times = list(zip(*self.processing_times))  # transpose
        format = " %3s"
        format_next_line = format + '\n'
        proc_times = ''.join([format % time if idx != len(times) - 1
                              else format_next_line % time
                              for times in processing_times
                              for idx, time in enumerate(times)])

        return taillard_pattern % (self.count_jobs, self.count_machines,
                                   self.initial_seed, self.upper_bound,
                                   proc_times)


# aliases for annotation's purpose
JSFrame = JobSchedulingFrame


def create_schedule(flow_job_frame: JobSchedulingFrame,
                    jobs_sequence: list,
                    count_job: int = None,
                    count_machine: int = None) -> Schedule:
    """
    Create schedule for job sequence using JobSchedulingFrame.

    Parameters
    ----------
    flow_job_frame: JobSchedulingFrame
    jobs_sequence: list
        solution of Flow Job scheduling problem
    count_job: int, default None
        count job from `jobs_sequence`, for that will be create schedule
    count_machine: int, default None
        count machines, for that will be create schedule

    Returns
    -------
    : Schedule
    """
    if count_job is None:
        count_job = len(jobs_sequence)
    if count_machine is None:
        count_machine = flow_job_frame.count_machines

    if not isinstance(count_job, int) or not isinstance(count_machine, int) or\
            count_job < 1 or count_machine < 1:
        raise ValueError('count_job and count_machine must be integers > 0')

    schedule = {job: [] for job in jobs_sequence[:count_job]}
    machines_time = [0 for _ in range(count_machine)]

    for job in jobs_sequence[:count_job]:
        begin_time = machines_time[0]
        end_time = begin_time + flow_job_frame.get_processing_time(job, 0)
        schedule[job].append(Duration(0, begin_time, end_time))
        machines_time[0] = end_time
        for machine_index in range(1, count_machine):
            job_time = flow_job_frame.get_processing_time(job, machine_index)
            machine_release_time = machines_time[machine_index]
            prev_machine_release_time = machines_time[machine_index - 1]

            if machine_release_time >= prev_machine_release_time:
                begin_time = machine_release_time
            else:
                begin_time = prev_machine_release_time

            end_time = begin_time + job_time
            machines_time[machine_index] = end_time
            schedule[job].append(Duration(machine_index, begin_time, end_time))

    return Schedule(schedule, machines_time[len(machines_time) - 1])


# Almost all code is duplicated from `create_schedule` func; need to fix this
# Reason: gives a significant increase in performance by reducing allocation
def compute_end_time(flow_job_frame: JobSchedulingFrame,
                     jobs_sequence: list,
                     count_job: int = None,
                     count_machine: int = None) -> Schedule:
    if count_job is None:
        count_job = len(jobs_sequence)
    if count_machine is None:
        count_machine = flow_job_frame.count_machines

    if not isinstance(count_job, int) or not isinstance(count_machine, int) or\
            count_job < 1 or count_machine < 1:
        raise ValueError('count_job and count_machine must be integers > 0')

    machines_time = [0 for _ in range(count_machine)]

    for job in jobs_sequence[:count_job]:
        begin_time = machines_time[0]
        end_time = begin_time + flow_job_frame.get_processing_time(job, 0)

        machines_time[0] = end_time
        for machine_index in range(1, count_machine):
            job_time = flow_job_frame.get_processing_time(job, machine_index)
            machine_release_time = machines_time[machine_index]
            prev_machine_release_time = machines_time[machine_index - 1]

            if machine_release_time >= prev_machine_release_time:
                begin_time = machine_release_time
            else:
                begin_time = prev_machine_release_time

            end_time = begin_time + job_time
            machines_time[machine_index] = end_time

    return machines_time[len(machines_time) - 1]


def _set_seed(initial_seed: Union[int, _NaN]):
    if initial_seed is not NaN:
        if not isinstance(initial_seed, int):
            raise ValueError('initial_seed must be a integer')
        rd.seed(initial_seed)
    else:
        initial_seed = int(time.time())
        rd.seed(initial_seed)


def flow_job_generator(count_jobs: int, count_machines: int,
                       initial_seed: Union[int, _NaN] = NaN) -> JSFrame:
    """
    Creates instance of Flow Job scheduling problem
    wrapped in `JobSchedulingFrame`.

    Parameters
    ----------
    count_jobs: int
    count_machines: int
    initial_seed: int or NaN
        if `initial_seed` is NaN then the current time, that casted to int,
        will be taken as the seed for random generator.

    Returns
    -------
    : JobSchedulingFrame
    """

    _set_seed(initial_seed)

    if count_jobs < 1 or count_machines < 1:
        raise ValueError('count_jobs and count_machines '
                         'must be greater than zero')

    processing_time = []
    for j in range(count_jobs):
        machine_time = []
        for i in range(count_machines):
            machine_time.append(rd.randint(1, 99))
        processing_time.append(machine_time)

    assert count_jobs == len(processing_time)
    assert count_machines == len(processing_time[0])

    return JobSchedulingFrame(processing_time, initial_seed=initial_seed)


def johnson_three_machines_generator(
    count_jobs: int,
    initial_seed: Union[int, _NaN] = NaN
) -> JSFrame:

    """
    Creates instance of special case of Flow Shop scheduling problem, on three
    machines, wrapped in `JobSchedulingFrame`.
    A polynomial algorithm to find the exact solution is known for this case.

    Special case description:
        the maximum processing time of all jobs on the second machine is less
        than minimum processing time on the first and second machine.

    Parameters
    ----------
    count_jobs: int
    initial_seed: int or NaN
        if `initial_seed` is NaN then the current time, that casted to int,
        will be taken as the seed for random generator.

    Returns
    -------
    : JobSchedulingFrame
    """

    _set_seed(initial_seed)

    if count_jobs < 1:
        raise ValueError('count_jobs must be greater than zero')

    processing_time = []
    for j in range(count_jobs):
        machine_time = []
        for i in range(-1, 2):
            min_value = 1 + 100 * (i * i)
            max_calue = 99 + 100 * (i * i)
            machine_time.append(rd.randint(min_value, max_calue))
        processing_time.append(machine_time)

    assert count_jobs == len(processing_time)
    assert 3 == len(processing_time[0])

    return JobSchedulingFrame(processing_time, initial_seed=initial_seed)
