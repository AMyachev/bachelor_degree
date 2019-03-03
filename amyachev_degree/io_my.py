import re
import time
import plotly
import plotly.figure_factory as ff

from amyachev_degree.core import Jobs, Machines, JobSchedulingFrame


def read_file_with_open_shop(file_name):  # FIXME
    """
    for open shop use False
    count_job, count_machine, processing_time, processing_order = read_file('D:/pipeline_task.txt',True)
    processing_time = list(zip(*processing_time)) # and comment this
    :param file_name:
    :return:
    """
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
    f.close()
    jobs_cl = Jobs(count_jobs)
    machines_cl = Machines(count_machines)

    return JobSchedulingFrame(jobs_cl, machines_cl, processing_time, processing_order, None)


class FlowShopFormatError(Exception):
    def __init__(self, file_name, counter_lines):
        self.file_name = file_name
        if counter_lines is not None:
            self.error_message = "line " + str(counter_lines)
        else:
            self.error_message = "\nFile is empty or don't have strings with these first words: 'number', 'processing'"

    def __str__(self):
        return 'File "%s", %s' % (self.file_name, self.error_message)


def read_flow_shop_instances(file_name):
    """
    file format (http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html)
        number of jobs, number of machines, initial seed, upper bound and lower bound :
              20           5   873654221        1278        1232
        processing times :
        54 83 15 71 77 36 53 38 27 87 76 91 14 29 12 77 32 87 68 94
        79  3 11 99 56 70 99 60  5 56  3 61 73 75 47 14 21 86  5 77
        16 89 49 15 89 45 60 23 57 64  7  1 63 41 63 47 26 75 77 40
        66 58 31 68 78 91 13 59 49 85 85  9 39 41 56 40 54 77 51 31
        58 56 20 85 53 35 53 41 69 13 86 72  8 49 47 87 58 18 68 28

    :param file_name
    :return list of JobSchedulingFrame objects
    """

    file = open(file_name)
    frames = []
    counter_lines = 0
    for string in iter(file):
        counter_lines += 1
        try:
            if string.strip().startswith('number'):
                string = next(file); counter_lines += 1
                params = re.findall(r'\d+', string)[:4]
                if len(params) != 4:
                    raise FlowShopFormatError(file_name, counter_lines)
                count_jobs, count_machines, _, upper_bound_makespan = (int(param) for param in params)

                string = next(file); counter_lines += 1
                if string.strip().startswith('processing'):
                    processing_time = []
                    for _ in range(count_machines):
                        string = next(file); counter_lines += 1
                        times = re.findall(r'\d+', string)
                        if len(times) != count_jobs:
                            raise FlowShopFormatError(file_name, counter_lines)
                        processing_time.append((int(number) for number in times))

                    jobs_cl = Jobs(count_jobs)
                    machines_cl = Machines(count_machines)
                    processing_time = list(zip(*processing_time))  # transpose
                    frames.append(JobSchedulingFrame(jobs_cl, machines_cl, processing_time, None, upper_bound_makespan))
                else:
                    raise FlowShopFormatError(file_name, counter_lines)
        except StopIteration:
            raise FlowShopFormatError(file_name, counter_lines)

    if len(frames) == 0:
        raise FlowShopFormatError(file_name, None)

    file.close()
    return frames


def create_gantt_chart(schedule, filename='gantt_chart.html'):
    """
    :param schedule: Schedule object
    :param filename: str object
    :return:
    """
    def sec_to_time(secs):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))

    tasks_schedule = []
    for job in schedule.jobs:
        for duration in schedule.process_times(job):
            start_date = sec_to_time(duration.begin_time)
            end_date = sec_to_time(duration.end_time)
            machine_number = duration.machine_number + 1
            tasks_schedule.append(dict(Task="Machine #%d" % machine_number, Start=start_date, Finish=end_date))

    gantt_chart = ff.create_gantt(tasks_schedule, group_tasks=True)

    task_counter = 0
    for job in schedule.jobs:
        for duration in schedule.process_times(job):
            start_date = sec_to_time(duration.begin_time)
            end_date = sec_to_time(duration.end_time)
            text = "Start: %s, Finish: %s, Job #%d" % (start_date, end_date, job + 1)
            gantt_chart["data"][task_counter].update(text=text, hoverinfo="text")
            task_counter += 1

    plotly.offline.plot(gantt_chart, filename=filename, auto_open=True)
