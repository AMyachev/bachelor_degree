from amyachev_degree.core import Machines, JobSchedulingFrame, create_schedule
from amyachev_degree.exact_algorithm import johnson_algorithm


def palmer_heuristics(flow_job_frame):
    """
    Journal Paper:
        Palmer, D.S., 1965. Sequencing jobs through a multi-stage process in the minimum total time a quick method of
        obtaining a near optimum. Operations Research Quarterly 16(1), 101-107
    :param flow_job_frame: JobSchedulingFrame
    :return: heuristics_solution: list
    """
    count_jobs = flow_job_frame.count_jobs
    count_machines = flow_job_frame.count_machines

    slope_indexes = []
    for job_index in range(count_jobs):
        slope_index = 0
        for machine_index in range(count_machines):
            slope_index -= (count_machines - (2 * (machine_index + 1) - 1)) * \
                           flow_job_frame.get_processing_time(job_index, machine_index)
        slope_indexes.append(slope_index)

    heuristics_solution = [job_index for job_index in range(count_jobs)]
    heuristics_solution.sort(key=lambda _job_index: slope_indexes[_job_index], reverse=True)
    return heuristics_solution


def campbell_dudek_smith(flow_job_frame):  # clean me
    """cds_sequence = campbell_dudek_smith(job_scheduling_task)
    print("CDS's sequence :", cds_sequence)
    schedule_1 = create_schedule(cds_sequence, job_scheduling_task.processing_time)
    create_gantt_chart(schedule_1)
    """
    def compute_processing_times_first_stage(_flow_job_frame, _sub_problem):
        processing_times = []
        for job_index in range(_flow_job_frame.count_jobs):
            sum_times = 0
            for machine_index in range(_sub_problem):
                sum_times += _flow_job_frame.get_processing_time(job_index, machine_index)
            processing_times.append(sum_times)
        return processing_times

    def compute_processing_times_second_stage(_flow_job_frame, _sub_problem):
        processing_times = []
        count_machines = _flow_job_frame.count_machines
        for job_index in range(_flow_job_frame.count_jobs):
            sum_times = 0
            for machine_index in range(count_machines - _sub_problem, count_machines):
                sum_times += _flow_job_frame.get_processing_time(job_index, machine_index)
            processing_times.append(sum_times)
        return processing_times

    johnson_scheduling_frame = JobSchedulingFrame(flow_job_frame.jobs, Machines(2), [], None, None)

    johnson_solutions_with_end_time = []
    for sub_problem in range(1, flow_job_frame.count_machines):
        johnson_scheduling_frame.set_processing_times(
            [compute_processing_times_first_stage(flow_job_frame, sub_problem),
             compute_processing_times_second_stage(flow_job_frame, sub_problem)]
        )
        johnson_solution = johnson_algorithm(johnson_scheduling_frame)
        end_time = create_schedule(johnson_solution, flow_job_frame.processing_times).end_time
        johnson_solutions_with_end_time.append((johnson_solution, end_time))

    johnson_solutions_with_end_time.sort(key=lambda elem: elem[1])
    return johnson_solutions_with_end_time[0][0]


def neh_heuristics(flow_job_scheduling_frame):  # clean me
    count_jobs = flow_job_scheduling_frame.count_jobs
    count_machines = flow_job_scheduling_frame.count_machines
    processing_time = flow_job_scheduling_frame.processing_times

    init_job_sequence = [index_job for index_job in range(count_jobs)]
    sum_sequence = []
    for job in range(count_jobs):
        sum_time = 0
        for i in range(count_machines):
            sum_time += processing_time[job][i]
        sum_sequence.append(sum_time)

    init_job_sequence.sort(key=lambda x: sum_sequence[x], reverse=True)
    result_sequence = [init_job_sequence[0]]
    for i in range(1, count_jobs):

        _min = -1
        best_sequence = []
        for j in range(0, i + 1):
            temp_sequence = list(result_sequence)
            temp_sequence.insert(j, init_job_sequence[i])
            if _min == -1:
                _min = create_schedule(temp_sequence, processing_time).end_time
                best_sequence = temp_sequence
            else:
                end_time = create_schedule(temp_sequence, processing_time).end_time
                if _min > end_time:
                    _min = end_time
                    best_sequence = temp_sequence
        result_sequence = list(best_sequence)

    return result_sequence
