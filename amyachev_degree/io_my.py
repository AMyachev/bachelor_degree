import re
import time
import plotly
import plotly.figure_factory as ff

from amyachev_degree.core import JobSchedulingFrame


class FlowShopFormatError(Exception):
    def __init__(self, file_name, counter_lines):
        self.file_name = file_name
        if counter_lines is not None:
            self.error_message = "line " + str(counter_lines)
        else:
            self.error_message = "\nFile is empty or don't have strings with \
                                 these first words: 'number', 'processing'"

    def __str__(self):
        return 'File "%s", %s' % (self.file_name, self.error_message)


def read_flow_shop_instances(file_name):
    """
    Read from file with Tailard's instances to JobSchedulingFrames

    Parameters
    ----------
    file_name: str

    Returns
    -------
    Sequence of JobSchedulingFrame objects: list

    Notes
    -----
    http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html
    file format:
        number of jobs, number of machines, initial seed,
        upper bound and lower bound :
              20           5   873654221        1278        1232
        processing times :
        54 83 15 71 77 36 53 38 27 87 76 91 14 29 12 77 32 87 68 94
        79  3 11 99 56 70 99 60  5 56  3 61 73 75 47 14 21 86  5 77
        16 89 49 15 89 45 60 23 57 64  7  1 63 41 63 47 26 75 77 40
        66 58 31 68 78 91 13 59 49 85 85  9 39 41 56 40 54 77 51 31
        58 56 20 85 53 35 53 41 69 13 86 72  8 49 47 87 58 18 68 28
    """

    file = open(file_name)
    frames = []
    counter_lines = 0
    for string in iter(file):
        counter_lines += 1
        try:
            if string.strip().startswith('number'):
                string = next(file)
                counter_lines += 1
                params = re.findall(r'\d+', string)[:4]
                if len(params) != 4:
                    raise FlowShopFormatError(file_name, counter_lines)
                count_jobs, count_machines, \
                    _, upper_bound_makespan = (int(param) for param in params)

                string = next(file)
                counter_lines += 1
                if string.strip().startswith('processing'):
                    processing_time = []
                    for _ in range(count_machines):
                        string = next(file)
                        counter_lines += 1
                        times = re.findall(r'\d+', string)
                        if len(times) != count_jobs:
                            raise FlowShopFormatError(file_name, counter_lines)
                        processing_time.append((int(time) for time in times))

                    processing_time = list(zip(*processing_time))  # transpose

                    assert count_jobs == len(processing_time)
                    assert count_machines == len(processing_time[0])

                    frames.append(
                        JobSchedulingFrame(
                            processing_time,
                            upper_bound_makespan=upper_bound_makespan
                        )
                    )
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
    def sec_to_date_time(secs):  # secs count from 1970-01-01 03:00:00
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))

    texts = []
    tasks_schedule = []
    format = "Start: %s, Finish: %s, Job #%d"
    for index_job in schedule.jobs:
        for process_time in schedule.process_times(index_job):
            start_date = sec_to_date_time(process_time.begin_time)
            end_date = sec_to_date_time(process_time.end_time)
            machine_number = process_time.machine_index + 1  # index -> number
            tasks_schedule.append(dict(Task="Machine #%d" % machine_number,
                                       Start=start_date, Finish=end_date))
            text = format % (start_date, end_date, index_job + 1)
            texts.append(text)

    gantt_chart = ff.create_gantt(tasks_schedule, group_tasks=True)

    for dict_counter in range(len(gantt_chart["data"])):
        gantt_chart["data"][dict_counter].update(text=texts[dict_counter],
                                                 hoverinfo="text")

    plotly.offline.plot(gantt_chart, filename=filename, auto_open=True)
