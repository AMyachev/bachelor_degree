import time
import random as rd
from collections import namedtuple


Duration = namedtuple('Duration', ['machine_index', 'begin_time', 'end_time'])


class Jobs:
    def __init__(self, count_job):
        self.count_jobs = count_job
        self.job_release_time = []
        self.job_current_state = []
        for i in range(count_job):
            self.job_release_time.append(0)
        for i in range(count_job):
            self.job_current_state.append(-1)

    def list_ready(self, current_time):
        output = []
        for i in range(self.count_jobs):
            if self.job_release_time[i] <= current_time:
                output.append(i)
        return output

    def all_ready(self):
        for i in range(self.count_jobs):
            if self.job_release_time[i] != -1:
                return False
        return True


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


class JobSchedulingFrame:
    def __init__(self, jobs_cl, machines_cl,
                 processing_time, processing_order=None,
                 upper_bound_makespan=None, initial_seed="NaN"):
        self.jobs = jobs_cl
        self.machines = machines_cl
        self.processing_times = processing_time
        self.processing_order = processing_order
        self.upper_bound_makespan = upper_bound_makespan
        self.init_seed = initial_seed

    @property
    def initial_seed(self):
        return self.init_seed

    @property
    def count_jobs(self):
        return self.jobs.count_jobs

    @property
    def count_machines(self):
        return self.machines.count_machines

    @property
    def schedule_ready(self):
        return self.jobs.all_ready()

    def get_processing_time(self, idx_job, idx_machine):
        """
        Return processing time `idx_job` on `idx_macine`

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

    def ready_jobs(self, current_time):
        return self.jobs.list_ready(current_time)

    def ready_machines(self, current_time):
        return self.machines.list_ready(current_time)

    def work_on_machine(self, job, machine, _current_time):
        busy_time = self.processing_times[job][machine]
        self.jobs.job_release_time[job] = _current_time + busy_time
        self.machines.take_machine_time(machine, _current_time, busy_time)
        self.jobs.job_current_state[job] += 1

    def next_ready_machine(self, job):
        if self.processing_order:
            try:
                next_state = self.jobs.job_current_state[job] + 1
                return self.processing_order[job][next_state] - 1
            except IndexError:
                self.jobs.job_release_time[job] = -1
                return None
        else:
            state = self.jobs.job_current_state[job] + 1
            if state < self.machines.count_machines:
                return state
            else:
                self.jobs.job_release_time[job] = -1
                return None

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
                    count_job=None, count_machine=None):
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


def flow_job_generator(count_jobs, count_machines, initial_seed=None):
    if initial_seed is not None:
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
    jobs = Jobs(count_jobs)
    machines = Machines(count_machines)
    return JobSchedulingFrame(jobs, machines,
                              processing_time, initial_seed=initial_seed)


def johnson_three_machines_generator(count_jobs, initial_seed=None):
    if initial_seed is not None:
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
    jobs = Jobs(count_jobs)
    machines = Machines(3)
    return JobSchedulingFrame(jobs, machines,
                              processing_time, initial_seed=initial_seed)
