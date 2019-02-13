import re

def read_file(file_name, transp):
    f = open(file_name)
    count_job = 0
    count_machine = 0
    processing_time = []
    processing_order = []

    for i in iter(f):
        if i.startswith('number'):
            i = next(f)
            count_job, count_machine = re.findall(r'\d+', i)[:2]
        if i.startswith('processing'):
            if transp:
                count_machine, count_job = count_job, count_machine
            for str in range(int(count_job)):
                i = next(f)
                processing_time.append([int(number) for number in re.findall(r'\d+', i)])
        if i.startswith('machines'):
            if transp:
                count_machine, count_job = count_job, count_machine
            for str in range(int(count_job)):
                i = next(f)
                processing_order.append([int(number) for number in re.findall(r'\d+', i)])
    if processing_order == []:
        processing_order = None
    return count_job, count_machine, processing_time, processing_order


class Jobs:
    def __init__(self, count_job):
        self.count_jobs = count_job
        self.job_release_time = []
        self.job_current_state = []
        for i in range(count_job):
            self.job_release_time.append(0)
        for i in range(count_job):
            self.job_current_state.append(-1)

    def all_time_job(self, job):          # heuristics
        sum = 0
        for i in range(int(self.count_machine)):
            sum += processing_time[job][i]
        return sum

    def palmer_heuristics(self, job):
        slope_index = 0
        for i in range(int(self.count_machine)):
            slope_index -= (int(self.count_machine) - (2 * (i + 1) - 1)) * processing_time[job][i]
        return slope_index

    def list_ready(self, current_time):
        output = []
        for i in range(self.count_jobs):
            if self.job_release_time[i] <= current_time:
                output.append(i)
        # output.sort(key=self.all_time_job)
        output.sort(key=self.palmer_heuristics, reverse=True)
        return output

    def nextmachine(self, job, processing_order):
        try:
            return processing_order[job][self.job_current_state[job] + 1] - 1
        except:
            self.job_release_time[job] = -1
            return None

    def work_on_machine(self, job, machine, machines, current_time):
        busy_time = processing_time[job][machine]
        self.job_release_time[job] = current_time + busy_time
        machines.take_machine_time(machine, current_time, busy_time)
        self.job_current_state[job] += 1
    
    def all_ready(self):
        for i in range(self.count_jobs):
            if self.job_release_time[i] != -1:
               return False
        return True


class Machines:
    def __init__(self, count_machine):
        self.count_machine = count_machine
        self.release_time = []
        for i in range(count_machine):
            self.release_time.append(0)

    def take_machine_time(self, machine, current_time, busy_time):
        self.release_time[machine] = current_time + busy_time

    def list_ready(self, current_time):
        output = []
        for i in range(self.count_machine):
            if self.release_time[i] <= current_time:
                output.append(i)
        return output


def frontal_algorithm(jobs, machines):
    current_time = 0

    while (not jobs.all_ready()):
        ready_jobs = jobs.list_ready(current_time)
        ready_machines = machines.list_ready(current_time)
        for job in ready_jobs:
            next_car = jobs.nextmachine(job, processing_order)
            if next_car in ready_machines:
                jobs.work_on_machine(job, next_car, machines, current_time)
            ready_machines = machines.list_ready(current_time)
        current_time += 1

    return current_time


def min_with_bound(job_times, job_in_permutation):
    min = -1
    for index, time in enumerate(job_times):
        if job_in_permutation[index] == 0:
            if min == -1:
                min = time
            elif time < min:
                min = time
    return min


def index_with_check(job_times, min_value, job_in_permutation):
    for index, time in enumerate(job_times):
        if time == min_value and job_in_permutation[index] == 0:
            return index
    return -1


def johnson_algorithm(jobs, machines, processing_time):
    output = []
    index_insert = 0
    job_in_permutation = [0 for _ in range(int(count_job))]
    if len(processing_time) != 2:
        raise ValueError

    min_item_first_machine = min_with_bound(processing_time[0], job_in_permutation)
    min_item_second_machine = min_with_bound(processing_time[1], job_in_permutation)

    for i in range(int(count_job)):
        if min_item_first_machine == -1 or min_item_second_machine == -1:
            raise ValueError
        if min_item_first_machine > min_item_second_machine:
            index_job = index_with_check(processing_time[1], min_item_second_machine, job_in_permutation)
            if index_job == -1:
                raise ValueError
            output.insert(index_insert, index_job)
            job_in_permutation[index_job] = 1

            min_item_first_machine = min_with_bound(processing_time[0], job_in_permutation)
            min_item_second_machine = min_with_bound(processing_time[1], job_in_permutation)

        else:
            index_job = index_with_check(processing_time[0], min_item_first_machine, job_in_permutation)
            if index_job == -1:
                raise ValueError
            output. insert(index_insert, index_job)
            job_in_permutation[index_job] = 1
            index_insert += 1

            min_item_first_machine = min_with_bound(processing_time[0], job_in_permutation)
            min_item_second_machine = min_with_bound(processing_time[1], job_in_permutation)

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

def campbell_dudek_smith(jobs, machines, processing_time):
    def a(jobs, sub_problem):                 # first stage for CDS heuristics
        times_for_first_stage = []
        for i in range(jobs.count_jobs):
            sum = 0
            for j in range(sub_problem):
                sum += processing_time[i][j]
            times_for_first_stage.append(sum)
        return times_for_first_stage

    def b(jobs, sub_problem):                 # second stage for CDS heuristics
        times_for_second_stage = []
        for i in range(jobs.count_jobs):
            sum = 0
            for j in range(jobs.count_jobs - sub_problem, jobs.count_jobs):
                sum += processing_time[i][j]
            times_for_second_stage.append(sum)
        return times_for_second_stage

    jobs_sequences = []
    for sub_problem in range(1, jobs.count_jobs):
        jobs_sequences.append(johnson_algorithm(jobs, machines, [a(jobs, sub_problem), b(jobs, sub_problem)]))

    jobs_sequences.sort(key=lambda jobs_sequence: compute_permutation_end_time(jobs_sequence, processing_time))


# count_job, count_machine, processing_time, processing_order = read_file('D:\\pipeline_task.txt',True) # for open shop use False

# processing_time = list(zip(*processing_time)) # and comment this


count_job, count_machine, processing_time, processing_order = read_file('D:\\pipeline_task.txt', False)

jobs = Jobs(int(count_job))
machines = Machines(int(count_machine))

print(campbell_dudek_smith(jobs, machines, processing_time))

# print(frontal_algorithm(jobs, machines))
