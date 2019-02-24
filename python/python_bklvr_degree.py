from core import create_schedule
from io_my import read_file, create_gantt_chart
from simple_heuristics import campbell_dudek_smith

# TODO fix to NEH heuristics realization
def heuristics_all_time_job(flow_job_scheduling_frame):
    count_jobs = flow_job_scheduling_frame.count_jobs
    count_machines = flow_job_scheduling_frame.count_machines
    processing_time = flow_job_scheduling_frame.processing_time

    result_sequence = [index_job for index_job in range(count_jobs)]
    sum_sequence = []
    for job in range(count_jobs):
        sum_time = 0
        for i in range(count_machines):
            sum_time += processing_time[job][i]
        sum_sequence.append(sum_time)

    result_sequence.sort(key=lambda x: sum_sequence[x])
    return result_sequence


job_scheduling_task = read_file('D:\\pipeline_task.txt', False)

cds_sequence = campbell_dudek_smith(job_scheduling_task)
print("CDS's sequence :", cds_sequence)
schedule_1 = create_schedule(cds_sequence, job_scheduling_task.processing_time)
create_gantt_chart(schedule_1)

# TODO implement lower bound of flow shop problem
