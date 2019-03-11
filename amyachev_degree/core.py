import time
import random as rd
from collections import namedtuple


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

    @property
    def end_time(self):
        return self._end_time

    def process_times(self, job):
        return self.jobs_duration_times[job]


class JobSchedulingFrame:
    def __init__(self, jobs_cl, machines_cl, processing_time, processing_order=None,
                 upper_bound_makespan=None, initial_seed=None):
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

    def get_processing_time(self, job, machine):
        return self.processing_times[job][machine]

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
                return self.processing_order[job][self.jobs.job_current_state[job] + 1] - 1
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

    def __repr__(self):  # processing time is transposed regarding taillard pattern now
        taillard_pattern = """number of jobs, number of machines, initial seed, upper bound and lower bound :
          %d           %d   %d        Nan        Nan
processing times :
%s
"""
        proc_time_str = ''.join([" %3s" % time if j != len(times) - 1 else " %3s\n" % time
                                 for times in self.processing_times for j, time in enumerate(times)])
        return taillard_pattern % (self.count_jobs, self.count_machines, self.initial_seed, proc_time_str)


def create_schedule(jobs_sequence, processing_time):
    Duration = namedtuple('Duration', ['machine_index', 'begin_time', 'end_time'])
    schedule = {job: [] for job in jobs_sequence}
    machines_time = [0 for _ in range(len(processing_time[0]))]

    for job in jobs_sequence:
        begin_time = machines_time[0]
        end_time = begin_time + processing_time[job][0]
        schedule[job].append(Duration(0, begin_time, end_time))
        machines_time[0] = end_time
        for machine_index in range(1, len(processing_time[0])):
            job_time = processing_time[job][machine_index]
            machine_release_time = machines_time[machine_index]
            prev_machine_release_time = machines_time[machine_index - 1]

            if machine_release_time >= prev_machine_release_time:
                begin_time = machine_release_time
                end_time = begin_time + job_time
                machines_time[machine_index] = end_time
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
    return JobSchedulingFrame(jobs, machines, processing_time, initial_seed=initial_seed)


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
            machine_time.append(rd.randint(1 + 100 * (i * i), 99 + 100 * (i * i)))
        processing_time.append(machine_time)
    jobs = Jobs(count_jobs)
    machines = Machines(3)
    return JobSchedulingFrame(jobs, machines, processing_time, initial_seed=initial_seed)
