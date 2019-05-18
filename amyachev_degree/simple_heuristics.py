from amyachev_degree.core import (JobSchedulingFrame, create_schedule)
from amyachev_degree.exact_algorithm import johnson_algorithm


def palmer_heuristics(flow_job_frame: JobSchedulingFrame) -> list:
    """
    Compute approximate solution for instance of Flow Job problem by
    Palmer's heuristic.

    Parameters
    ----------
    flow_job_frame: JobSchedulingFrame

    Returns
    -------
    solution: list
        sequence of job index

    Notes
    -----
    Journal Paper:
        Palmer, D.S., 1965. Sequencing jobs through a multi-stage process in
        the minimum total time a quick method of obtaining a near optimum.
        Operations Research Quarterly 16(1), 101-107
    """
    count_jobs = flow_job_frame.count_jobs
    count_machines = flow_job_frame.count_machines

    slope_indexes = []
    for idx_job in range(count_jobs):
        slope_index = 0
        for idx_machine in range(count_machines):
            slope_index -= (count_machines - (2 * (idx_machine + 1) - 1)) * \
                            flow_job_frame.get_processing_time(idx_job,
                                                               idx_machine)
        slope_indexes.append(slope_index)

    solution = [idx_job for idx_job in range(count_jobs)]
    solution.sort(key=lambda _idx_job: slope_indexes[_idx_job], reverse=True)
    return solution


def _compute_processing_times_frst_stage(frame, sub_problem):
    processing_times = []
    for job_index in range(frame.count_jobs):
        sum_times = 0
        for machine_index in range(sub_problem):
            sum_times += frame.get_processing_time(job_index,
                                                   machine_index)
        processing_times.append(sum_times)
    return processing_times


def _compute_processing_times_scnd_stage(frame, sub_problem):
    processing_times = []
    count_machines = frame.count_machines
    for job_index in range(frame.count_jobs):
        sum_times = 0
        for machine_index in range(count_machines - sub_problem,
                                   count_machines):
            sum_times += frame.get_processing_time(job_index,
                                                   machine_index)
        processing_times.append(sum_times)
    return processing_times


def cds_heuristics(flow_job_frame: JobSchedulingFrame) -> list:
    """
    Compute approximate solution for instance of Flow Job problem by
    Campbell, Dudek, and Smith (CDS) heuristic.

    Parameters
    ----------
    flow_job_frame: JobSchedulingFrame

    Returns
    -------
    solution: list
        sequence of job index

    Notes
    -----
    Developed:
        Campbell, Dudek, and Smith in 1970
    """
    frame = JobSchedulingFrame([[]])

    johnson_solutions_with_end_time = []
    for sub_problem in range(1, flow_job_frame.count_machines):
        frame.set_processing_times(
            [_compute_processing_times_frst_stage(flow_job_frame, sub_problem),
             _compute_processing_times_scnd_stage(flow_job_frame, sub_problem)]
        )
        johnson_solution = johnson_algorithm(frame)
        end_time = create_schedule(flow_job_frame, johnson_solution).end_time
        johnson_solutions_with_end_time.append((johnson_solution, end_time))

    johnson_solutions_with_end_time.sort(key=lambda elem: elem[1])
    return johnson_solutions_with_end_time[0][0]


def neh_heuristics(flow_job_frame):
    """
    Compute solution for instance of Flow Job problem by NEH heuristic.

    Parameters
    ----------
    flow_job_frame: JobSchedulingFrame

    Returns
    -------
    heuristics_solution: list of job index

    Notes
    -----
    Journal Paper:
        Nawaz,M., Enscore,Jr.E.E, and Ham,I. (1983) A Heuristics Algorithm for
        the m Machine, n Job Flowshop Sequencing Problem.
        Omega-International Journal of Management Science 11(1), 91-95
    """
    count_jobs = flow_job_frame.count_jobs
    count_machines = flow_job_frame.count_machines

    all_processing_times = [0] * count_jobs
    for j in range(count_jobs):
        for m in range(count_machines):
            all_processing_times[j] += flow_job_frame.get_processing_time(j, m)

    init_jobs = [j for j in range(count_jobs)]
    init_jobs.sort(key=lambda x: all_processing_times[x], reverse=True)
    neh_solution = [init_jobs[0]]  # using job, which have max processing time

    # local search
    for j in range(1, count_jobs):
        min_end_time = -1
        best_insert_place = 0
        for i in range(0, j + 1):
            neh_solution.insert(i, init_jobs[j])
            if min_end_time == -1:
                min_end_time = create_schedule(
                    flow_job_frame,
                    neh_solution,
                ).end_time
                best_insert_place = i
            else:
                end_time = create_schedule(
                    flow_job_frame,
                    neh_solution,
                ).end_time
                if min_end_time > end_time:
                    min_end_time = end_time
                    best_insert_place = i
            neh_solution.pop(i)
        neh_solution.insert(best_insert_place, init_jobs[j])

    return neh_solution


def weighted_idle_time(frame: JobSchedulingFrame,
                       jobs: list, next_job: int) -> float:
    # TODO make sure that `jobs` does not change
    # during the operation of the function
    sch = create_schedule(frame, jobs.append(next_job))
    idle_time = 0.
    idx_second_last_job = jobs[-2]
    idx_last_job = jobs[-1]
    for idx_machine in range(1, frame.count_machines):
        cmpl_time1 = sch.end_time(idx_last_job, idx_machine - 1)
        cmpl_time2 = sch.end_time(idx_second_last_job, idx_machine)
        numerator = frame.count_machines * max(cmpl_time1 - cmpl_time2, 0)
        denominator = idx_machine + (len(jobs) - 1) * \
            (frame.count_machines - idx_machine) / (frame.count_jobs - 2)
        idle_time += numerator / denominator

    jobs.pop()  # remove this; see TODO
    return idle_time


def artificial_time(frame: JobSchedulingFrame,
                    jobs: list, unscheduled_jobs: list) -> int:
    #  copy processing time matrix jobs x machines from frame
    processing_times = []
    for idx_job in range(frame.count_jobs):
        processing_times.append(
            [frame.get_processing_time(idx_job, idx_machine)
             for idx_machine in range(frame.count_machines)]
        )
    #  creating processing times for artificial job as average of
    #  the processing times of jobs from `unscheduled_jobs`
    artificial_prc_times = []
    for idx_machine in range(frame.count_machines):
        average_time = 0.
        for idx_job in range(unscheduled_jobs):
            average_time += frame.get_processing_time(idx_job, idx_machine)
        average_time /= len(unscheduled_jobs)
        artificial_prc_times.append(average_time)
    processing_times.append(artificial_prc_times)

    assert frame.count_jobs + 1 == len(processing_times)
    assert frame.count_machines == len(processing_times[0])

    frame_with_artificial_job = JobSchedulingFrame(processing_times)
    jobs.append(len(frame.count_jobs) - 1)  # added index of artificial job
    sch = create_schedule(frame_with_artificial_job, jobs)

    idx_second_last_job = jobs[-2]
    idx_last_job = jobs[-1]

    end_time_sec_last_job = sch.end_time(idx_second_last_job,
                                         len(frame.count_machines) - 1)
    end_time_last_job = sch.end_time(idx_last_job,
                                     len(frame.count_machines) - 1)
    result_time = end_time_sec_last_job + end_time_last_job
    jobs.pop()
    return result_time


def liu_reeves_heuristric(frame: JobSchedulingFrame, count_sequences: int):
    def index_function(frame: JobSchedulingFrame,
                       jobs: list,
                       unscheduled_jobs: list,
                       next_job: int):
        return (frame.count_jobs - len(jobs) - 2) * \
            weighted_idle_time(frame, jobs, next_job) + \
            artificial_time(frame, jobs, unscheduled_jobs)

    init_sequence = [idx_job for idx_job in range(frame.count_jobs)]
    from copy import copy
    unscheduled_jobs = copy(init_sequence)
    init_sequence.sort(lambda next_job: index_function(frame, [],
                                                       unscheduled_jobs,
                                                       next_job))

    solutions = []
    for idx in range(count_sequences):
        solution = [init_sequence[idx]]
        unscheduled_jobs.remove(init_sequence[idx])
        for jdx in range(frame.count_jobs):
            min_job = min(unscheduled_jobs,
                          key=lambda next_job: index_function(frame, solution,
                                                              unscheduled_jobs,
                                                              next_job))
            solution.append(min_job)
            unscheduled_jobs.remove(min_job)
        solutions.append(solution)
    return solutions.sort(lambda solution:
                          create_schedule(frame, solution).end_time)[0]
