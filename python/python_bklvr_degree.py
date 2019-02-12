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

    def all_time_job(self, job):          #heuristics
        sum = 0
        for i in range(int(count_machine)):
            sum += processing_time[job][i]
        return sum

    def Palmer_heuristics(self, job):
        slope_index = 0
        for i in range(int(count_machine)):
            slope_index -= (int(count_machine) - (2 * (i + 1) - 1)) * processing_time[job][i]
        return slope_index

    def list_ready(self, current_time):
        output = []
        for i in range(self.count_jobs):
            if self.job_release_time[i] <= current_time:
                output.append(i)
        #output.sort(key=self.all_time_job)
        output.sort(key=self.Palmer_heuristics, reverse=True)
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


count_job, count_machine, processing_time, processing_order = read_file('D:\\pipeline_task.txt',True) #for open shop use False

processing_time = list(zip(*processing_time)) # and comment this

#out = open('D:\\pipeline_transp.txt', 'w')

#for i in processing_time:
#    for j in i:
#        out.write(str(j) + ' ')
#    out.write('\n')
#out.close()

jobs = Jobs(int(count_job))
machines = Machines(int(count_machine))
print(frontal_algorithm(jobs, machines))

