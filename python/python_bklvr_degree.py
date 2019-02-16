import re
import plotly
import plotly.figure_factory as ff


def read_file(file_name, transpose):
    f = open(file_name)
    count_jobs, count_machines = 0, 0
    processing_time, processing_order = [], []

    for string in iter(f):
        if string.startswith('number'):
            string = next(f)
            count_jobs, count_machines = [int(count) for count in re.findall(r'\d+', string)[:2]]
        if string.startswith('processing'):
            if transpose:
                count_machines, count_jobs = count_jobs, count_machines
            for _ in range(count_jobs):
                string = next(f)
                processing_time.append([int(number) for number in re.findall(r'\d+', string)])
        if string.startswith('machines'):
            if transpose:
                count_machines, count_jobs = count_jobs, count_machines
            for _ in range(count_jobs):
                string = next(f)
                processing_order.append([int(number) for number in re.findall(r'\d+', string)])
    if not processing_order:
        processing_order = None

    jobs_cl = Jobs(count_jobs)
    machines_cl = Machines(count_machines)

    return JobSchedulingFrame(jobs_cl, machines_cl, processing_time, processing_order)


class JobSchedulingFrame(object):
    def __init__(self, jobs_cl, machines_cl, processing_time, processing_order):
        self.jobs = jobs_cl
        self.machines = machines_cl
        self.processing_time = processing_time
        self.processing_order = processing_order

    @property
    def count_jobs(self):
        return self.jobs.count_jobs

    @property
    def count_machines(self):
        return self.machines.count_machines

    @property
    def schedule_ready(self):
        return self.jobs.all_ready()

    def ready_jobs(self, current_time):
        return self.jobs.list_ready(current_time)

    def ready_machines(self, current_time):
        return self.machines.list_ready(current_time)

    def work_on_machine(self, job, machine, _current_time):
        busy_time = self.processing_time[job][machine]
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


def frontal_algorithm(_job_scheduling_task):
    current_time = 0

    while not _job_scheduling_task.schedule_ready:
        ready_jobs = _job_scheduling_task.ready_jobs(current_time)
        ready_machines = _job_scheduling_task.ready_machines(current_time)
        for job in ready_jobs:
            next_car = _job_scheduling_task.next_ready_machine(job)
            if next_car in ready_machines:
                _job_scheduling_task.work_on_machine(job, next_car, current_time)
            ready_machines = _job_scheduling_task.ready_machines(current_time)
        current_time += 1

    return current_time


def min_with_check(job_times, job_in_permutation):
    min_time = -1
    for index, _time in enumerate(job_times):
        if job_in_permutation[index] == 0:
            if min_time == -1:
                min_time = _time
            elif _time < min_time:
                min_time = _time
    return min_time


def index_with_check(job_times, min_value, job_in_permutation):
    for index, _time in enumerate(job_times):
        if _time == min_value and job_in_permutation[index] == 0:
            return index
    return -1


def johnson_algorithm(_johnson_scheduling_frame):
    output = []
    index_insert = 0
    job_in_permutation = [0 for _ in range(_johnson_scheduling_frame.count_jobs)]
    if _johnson_scheduling_frame.count_machines != 2:
        raise ValueError

    first_machine_time = _johnson_scheduling_frame.processing_time[0]
    second_machine_time = _johnson_scheduling_frame.processing_time[1]

    min_item_first_machine = min_with_check(first_machine_time, job_in_permutation)
    min_item_second_machine = min_with_check(second_machine_time, job_in_permutation)

    for i in range(_johnson_scheduling_frame.count_jobs):
        if min_item_first_machine == -1 or min_item_second_machine == -1:
            raise ValueError
        if min_item_first_machine > min_item_second_machine:
            index_job = index_with_check(second_machine_time, min_item_second_machine, job_in_permutation)
            if index_job == -1:
                raise ValueError
            output.insert(index_insert, index_job)
            job_in_permutation[index_job] = 1

            min_item_first_machine = min_with_check(first_machine_time, job_in_permutation)
            min_item_second_machine = min_with_check(second_machine_time, job_in_permutation)

        else:
            index_job = index_with_check(first_machine_time, min_item_first_machine, job_in_permutation)
            if index_job == -1:
                raise ValueError
            output. insert(index_insert, index_job)
            job_in_permutation[index_job] = 1
            index_insert += 1

            min_item_first_machine = min_with_check(first_machine_time, job_in_permutation)
            min_item_second_machine = min_with_check(second_machine_time, job_in_permutation)

    return output


def compute_permutation_end_time(permutation, processing_time):
    machines_time = [0 for _ in range(len(processing_time[0]))]
    for job in permutation:
        machines_time[0] += processing_time[job][0]
        for machine_index in range(1, len(processing_time[0])):
            job_time = processing_time[job][machine_index]
            machine_release_time = machines_time[machine_index]
            prev_machine_release_time = machines_time[machine_index - 1]

            if machine_release_time >= prev_machine_release_time:
                machines_time[machine_index] = machine_release_time + job_time
            else:
                machines_time[machine_index] = prev_machine_release_time + job_time
    return machines_time[len(machines_time) - 1]


assert 114 == compute_permutation_end_time([2, 4, 3, 0, 1], [[17, 19, 13], [15, 11, 12], [14, 21, 16], [20, 16, 20], [16, 17, 17]])  # test
assert 115 == compute_permutation_end_time([4, 2, 3, 0, 1], [[17, 19, 13], [15, 11, 12], [14, 21, 16], [20, 16, 20], [16, 17, 17]])  # test


def campbell_dudek_smith(job_scheduling_frame):
    def a(_job_scheduling_frame, _sub_problem):                 # first stage for CDS heuristics
        times_for_first_stage = []
        for i in range(_job_scheduling_frame.count_jobs):
            sum_times = 0
            for j in range(_sub_problem):
                sum_times += _job_scheduling_frame.processing_time[i][j]
            times_for_first_stage.append(sum_times)
        return times_for_first_stage

    def b(_job_scheduling_frame, _sub_problem):                 # second stage for CDS heuristics
        times_for_second_stage = []
        count_machines = _job_scheduling_frame.count_machines
        for i in range(_job_scheduling_frame.count_jobs):
            sum_times = 0
            for j in range(count_machines - _sub_problem, count_machines):
                sum_times += _job_scheduling_frame.processing_time[i][j]
            times_for_second_stage.append(sum_times)
        return times_for_second_stage

    johnson_scheduling_frame = JobSchedulingFrame(job_scheduling_frame.jobs, Machines(2), [], None)

    jobs_sequences = []
    for sub_problem in range(1, job_scheduling_frame.count_machines):
        johnson_scheduling_frame.processing_time = [a(job_scheduling_frame, sub_problem),
                                                    b(job_scheduling_frame, sub_problem)]
        jobs_sequences.append(johnson_algorithm(johnson_scheduling_frame))

    jobs_sequences.sort(key=lambda jobs_sequence: compute_permutation_end_time(jobs_sequence,
                                                                               job_scheduling_frame.processing_time))
    return jobs_sequences[0]


def palmer_heuristics(flow_job_scheduling_frame):
    count_jobs = flow_job_scheduling_frame.count_jobs
    count_machines = flow_job_scheduling_frame.count_machines
    processing_time = flow_job_scheduling_frame.processing_time

    result_sequence = [index_job for index_job in range(count_jobs)]
    slope_sequence = []
    for job in range(count_jobs):
        slope_index = 0
        for i in range(count_machines):
            slope_index -= (count_machines - (2 * (i + 1) - 1)) * processing_time[job][i]
        slope_sequence.append(slope_index)

    result_sequence.sort(key=lambda x: slope_sequence[x], reverse=True)
    return result_sequence


def all_time_job(self, job):          # heuristics
    sum_time = 0
    for i in range(int(self.count_machine)):
        sum_time += processing_time[job][i]
    return sum_time


# for open shop use False
# count_job, count_machine, processing_time, processing_order = read_file('D:\\pipeline_task.txt',True)
# processing_time = list(zip(*processing_time)) # and comment this


job_scheduling_task = read_file('D:\\pipeline_task.txt', False)

palmer_sequence = palmer_heuristics(job_scheduling_task)
print("palmers's sequence :", palmer_sequence)
print(compute_permutation_end_time(palmer_sequence, job_scheduling_task.processing_time))

best_sequence = campbell_dudek_smith(job_scheduling_task)
print("CDS's sequence :", best_sequence)
print(compute_permutation_end_time(best_sequence, job_scheduling_task.processing_time))


import time


def sec_to_time(secs):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))


df = [dict(Task="Machine #1", Start=sec_to_time(1000), Finish=sec_to_time(10000)),
      dict(Task="Machine #1", Start=sec_to_time(10000), Finish=sec_to_time(20000)),
      dict(Task="Machine #1", Start=sec_to_time(20000), Finish=sec_to_time(60000))
      ]


# fig = ff.create_gantt(df, group_tasks=True)

# text = "Start: %s, Finish: %s, Job #%d, Operation #%d" % (sec_to_time(1000), sec_to_time(10000), 1, 1)
# fig["data"][0].update(text=text, hoverinfo="text")


# plotly.offline.plot(fig, filename='check_gantt.html', auto_open=True)

print(frontal_algorithm(job_scheduling_task))
