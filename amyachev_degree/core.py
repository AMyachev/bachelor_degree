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


class JobSchedulingFrame(object):
    def __init__(self, jobs_cl, machines_cl, processing_time, processing_order, upper_bound_makespan):
        self.jobs = jobs_cl
        self.machines = machines_cl
        self.processing_time = processing_time
        self.processing_order = processing_order
        self.upper_bound_makespan = upper_bound_makespan

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
        return self.processing_time[job][machine]

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


def create_schedule(permutation, processing_time):
    Duration = namedtuple('Duration', ['machine_index', 'begin_time', 'end_time'])
    schedule = {job: [] for job in permutation}
    machines_time = [0 for _ in range(len(processing_time[0]))]

    for job in permutation:
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

