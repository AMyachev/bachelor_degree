import re
import time
import plotly
import plotly.figure_factory as ff

from core import Jobs, Machines, JobSchedulingFrame

# for open shop use False
# count_job, count_machine, processing_time, processing_order = read_file('D:\\pipeline_task.txt',True)
# processing_time = list(zip(*processing_time)) # and comment this
# TODO reimplemented for various input file formats


def read_file_with_open_shop(file_name):
    f = open(file_name)
    count_jobs, count_machines = 0, 0
    processing_time, processing_order = [], []

    for string in iter(f):
        if string.startswith('number'):
            string = next(f)
            count_jobs, count_machines = [int(count) for count in re.findall(r'\d+', string)[:2]]
        if string.startswith('processing'):
            for _ in range(count_jobs):
                string = next(f)
                processing_time.append([int(number) for number in re.findall(r'\d+', string)])
        if string.startswith('machines'):
            for _ in range(count_jobs):
                string = next(f)
                processing_order.append([int(number) for number in re.findall(r'\d+', string)])
    if not processing_order:
        processing_order = None

    jobs_cl = Jobs(count_jobs)
    machines_cl = Machines(count_machines)

    return JobSchedulingFrame(jobs_cl, machines_cl, processing_time, processing_order)


def read_file_with_flow_shop(file_name):
    f = open(file_name)
    count_jobs, count_machines = 0, 0
    processing_time, processing_order = [], []

    for string in iter(f):
        if string.startswith('number'):
            string = next(f)
            count_jobs, count_machines = [int(count) for count in re.findall(r'\d+', string)[:2]]
        if string.startswith('processing'):
            for _ in range(count_machines):
                string = next(f)
                processing_time.append([int(number) for number in re.findall(r'\d+', string)])

    jobs_cl = Jobs(count_jobs)
    machines_cl = Machines(count_machines)
    processing_time = list(zip(*processing_time))

    return JobSchedulingFrame(jobs_cl, machines_cl, processing_time, None)


def create_gantt_chart(_schedule, filename='gantt_chart.html'):
    def sec_to_time(secs):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))

    df = []
    for job in _schedule.jobs:
        for duration in _schedule.process_times(job):
            start_date = sec_to_time(duration[1])
            end_date = sec_to_time(duration[2])
            machine_number = duration[0] + 1
            temp_dict = dict(Task="Machine #%d" % machine_number, Start=start_date, Finish=end_date)
            df.append(temp_dict)

    fig = ff.create_gantt(df, group_tasks=True)

    sch = 0
    for job in _schedule.jobs:
        for operation, duration in enumerate(_schedule.process_times(job)):
            start_date = sec_to_time(duration[1])
            end_date = sec_to_time(duration[2])
            text = "Start: %s, Finish: %s, Job #%d, Operation #%d" % (start_date, end_date, job + 1, operation + 1)
            fig["data"][sch].update(text=text, hoverinfo="text")
            sch += 1

    plotly.offline.plot(fig, filename=filename, auto_open=True)
