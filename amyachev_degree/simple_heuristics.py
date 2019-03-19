from amyachev_degree.core import Machines, JobSchedulingFrame, create_schedule
from amyachev_degree.exact_algorithm import johnson_algorithm


def palmer_heuristics(flow_job_frame):
    """
    Journal Paper:
        Palmer, D.S., 1965. Sequencing jobs through a multi-stage process in the minimum total time a quick method of
        obtaining a near optimum. Operations Research Quarterly 16(1), 101-107
    :param flow_job_frame: JobSchedulingFrame
    :return heuristics_solution: list of job index
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


def cds_heuristics(flow_job_frame):
    """
    Developed:
        Campbell, Dudek, and Smith in 1970
    :param flow_job_frame: JobSchedulingFrame
    :return heuristics_solution: list of job index
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


def neh_heuristics(flow_job_frame):
    """
    Journal Paper:
        Nawaz,M., Enscore,Jr.E.E, and Ham,I. (1983) A Heuristics Algorithm for the m Machine,
        n Job Flowshop Sequencing Problem. Omega-International Journal of Management Science
        11(1), 91-95
    :param flow_job_frame: JobSchedulingFrame
    :return heuristics_solution: list of job index
    """
    count_jobs = flow_job_frame.count_jobs
    count_machines = flow_job_frame.count_machines

    all_processing_times = [0] * count_jobs
    for j in range(count_jobs):
        for m in range(count_machines):
            all_processing_times[j] += flow_job_frame.get_processing_time(j, m)

    init_jobs = [j for j in range(count_jobs)]
    init_jobs.sort(key=lambda x: all_processing_times[x], reverse=True)
    neh_solution = [init_jobs[0]]  # create list with job, which have max processing time

    # local search
    for j in range(1, count_jobs):
        min_end_time = -1
        best_insert_place = 0
        for i in range(0, j + 1):
            neh_solution.insert(i, init_jobs[j])
            if min_end_time == -1:
                min_end_time = create_schedule(neh_solution, flow_job_frame.processing_times).end_time
                best_insert_place = i
            else:
                end_time = create_schedule(neh_solution, flow_job_frame.processing_times).end_time
                if min_end_time > end_time:
                    min_end_time = end_time
                    best_insert_place = i
            neh_solution.pop(i)
        neh_solution.insert(best_insert_place, init_jobs[j])

    return neh_solution
