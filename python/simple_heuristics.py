from core import Machines, JobSchedulingFrame, create_schedule
from exact_algorithm import johnson_algorithm
# palmer_sequence = palmer_heuristics(job_scheduling_task)
# print("palmer's sequence :", palmer_sequence)


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

# cds_sequence = campbell_dudek_smith(job_scheduling_task)
# print("CDS's sequence :", cds_sequence)
# schedule_1 = create_schedule(cds_sequence, job_scheduling_task.processing_time)
# create_gantt_chart(schedule_1)


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

    jobs_sequences.sort(key=lambda jobs_sequence:
                        create_schedule(jobs_sequence, job_scheduling_frame.processing_time).end_time)
    return jobs_sequences[0]
