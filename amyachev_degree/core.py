import time
import random as rd
from collections import namedtuple


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
        self.count_machines = count_machines
        self.release_time = []
        for i in range(count_machines):
            self.release_time.append(0)

    def take_machine_time(self, machine, current_time, busy_time):
        self.release_time[machine] = current_time + busy_time

    def list_ready(self, current_time):
        output = []
        for i in range(self.count_machines):
            if self.release_time[i] <= current_time:
                output.append(i)
        return output


class Schedule(object):
    def __init__(self, jobs_duration_times, end_time):
        self.jobs_duration_times = jobs_duration_times
        self._end_time = end_time

    @property
    def jobs(self):
        return self.jobs_duration_times.keys()

    def __str__(self):
        string = ""
        for idx_job, list_durat in self.jobs_duration_times.items():
            string += "%s: " % idx_job
            for durat in list_durat:
                string += "(%s, %s), " % (durat.begin_time, durat.end_time)
            string += "\n"
        return string

    @property
    def end_time(self):
        return self._end_time

    def process_times(self, job):
        return self.jobs_duration_times[job]

    def completion_time(self, machine: int, job: int) -> int:
        """
        Parameters
        ----------
        machine: int
            machine index
        job: int
            job index

        Returns
        -------
        the completion time of `job` on `machine`: int
        """
        return self.jobs_duration_times[job][machine].end_time


class JobSchedulingFrame:

    def __init__(self, processing_times, upper_bound_makespan=None,
                 initial_seed=NaN,  processing_order=None):
        """
        Creates frame from matrix of processing times.

        Parameters
        ----------
        processing_times: list of lists of integers
        upper_bound_makespan: int or None
        initial_seed: int or NaN
        processing_order: list of lists of integers or None
            used for open job problems
        """
        # raise ValueError if wrong type
        self._check_processing_times(processing_times)

        self.processing_times = processing_times
        self.upper_bound_makespan = upper_bound_makespan

        if not initial_seed == NaN and not isinstance(initial_seed, int):
            raise ValueError('initial_seed must be the NaN or int')
        self.init_seed = initial_seed

        self.jobs = Jobs(len(processing_times))
        self.machines = Machines(len(processing_times[0]))

        self.processing_order = processing_order

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
        return self.init_seed

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

    def set_processing_times(self, processing_times):
        self.processing_times = processing_times

    def __str__(self):
        taillard_pattern = """number of jobs, number of machines,\
initial seed, upper bound and lower bound :
          %s           %s   %s        Nan        Nan
processing times :
%s
"""
        processing_times = list(zip(*self.processing_times))  # transpose
        format = " %3s"
        format_next_line = format + '\n'
        proc_times = ''.join([format % time if idx != len(times) - 1
                              else format_next_line % time
                              for times in processing_times
                              for idx, time in enumerate(times)])

        return taillard_pattern % (self.count_jobs, self.count_machines,
                                   self.initial_seed, proc_times)


def create_schedule(flow_job_frame: JobSchedulingFrame, jobs_sequence,
                    count_job=None, count_machine=None) -> Schedule:
    """
    Create schedule for job sequence using information from `flow_job_frame`

    Parameters
    ----------
    flow_job_frame: JobSchedulingFrame
    jobs_sequence: sequence of jobs indexes
    count_job: int, default None
        count job from `jobs_sequence`, for that will be create schedule
    count_machine: int, default None
        count machines, for that will be create schedule

    Returns
    -------
    schedule: Schedule
    """
    if count_job is None:
        count_job = len(jobs_sequence)
        count_machine = flow_job_frame.count_machines

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


def flow_job_generator(count_jobs, count_machines, initial_seed=NaN):
    if initial_seed is not NaN:
        rd.seed(initial_seed)
    else:
        initial_seed = time.time()
        rd.seed(initial_seed)
    processing_time = []
    for j in range(count_jobs):
        machine_time = []
        for i in range(count_machines):
            machine_time.append(rd.randint(1, 99))
        processing_time.append(machine_time)

    assert count_jobs == len(processing_time)
    assert count_machines == len(processing_time[0])

    return JobSchedulingFrame(processing_time, initial_seed=initial_seed)


def johnson_three_machines_generator(count_jobs, initial_seed=NaN):
    if initial_seed is not NaN:
        rd.seed(initial_seed)
    else:
        initial_seed = int(time.time())
        rd.seed(initial_seed)
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
