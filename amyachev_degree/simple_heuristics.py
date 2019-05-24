from amyachev_degree.core import (
    JobSchedulingFrame, compute_end_time, create_schedule)
from amyachev_degree.exact_algorithm import johnson_algorithm
from amyachev_degree.composite_heuristics import (
    local_search_partitial_sequence)


def slope_index_func(frame: JobSchedulingFrame, idx_job: int) -> int:
    """
    Compute slope index for `idx_job` using the method invented by Palmer, D.S.

    Parameters
    ----------
    frame: JobSchedulingFrame
    idx_job: int

    Returns
    -------
    slope index: int

    Notes
    -----
    Journal Paper:
        Palmer, D.S., 1965. Sequencing jobs through a multi-stage process in
        the minimum total time a quick method of obtaining a near optimum.
        Operations Research Quarterly 16(1), 101-107

    """
    count_machines = frame.count_machines
    slope_index = 0
    for idx_machine in range(count_machines):
        slope_index -= (count_machines - (2 * (idx_machine + 1) - 1)) * \
                        frame.get_processing_time(idx_job, idx_machine)

    return slope_index


def palmer_heuristics(frame: JobSchedulingFrame) -> list:
    """
    Compute approximate solution for instance of Flow Job problem by
    Palmer's heuristic.

    Parameters
    ----------
    frame: JobSchedulingFrame

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
    count_jobs = frame.count_jobs

    slope_indexes = []
    for idx_job in range(count_jobs):
        slope_indexes.append(slope_index_func(frame, idx_job))

    solution = [idx_job for idx_job in range(count_jobs)]
    solution.sort(key=lambda _idx_job: slope_indexes[_idx_job], reverse=True)
    return solution


def cds_create_proc_times(frame: JobSchedulingFrame, sub_problem: int) -> list:
    """
    Create processing time matrix with 2 machines from matrix with M machines
    according to the CDS heuristic rule.

    Parameters
    ----------
    frame: JobSchedulingFrame
    sub_problem: int
        `sub_problem` values start with 1

    Returns
    -------
    matrix of processing times: list

    Notes
    -----
    Developed by Campbell, Dudek, and Smith in 1970.

    """
    processing_times = []
    count_machines = frame.count_machines

    for idx_job in range(frame.count_jobs):
        first_machine_time = 0
        second_machine_time = 0

        # From `sub_problem` count machines will make one artificial,
        # summing up the processing times on each of them.
        for idx_machine in range(sub_problem):
            first_machine_time += frame.get_processing_time(idx_job,
                                                            idx_machine)

        # From `sub_problem` machines will make one artificial,
        # summing up the processing times on each of them.
        for idx_machine in range(count_machines - sub_problem, count_machines):
            second_machine_time += frame.get_processing_time(idx_job,
                                                             idx_machine)

        processing_times.append([first_machine_time, second_machine_time])

    return processing_times


def cds_heuristics(frame: JobSchedulingFrame) -> list:
    """
    Compute approximate solution for instance of Flow Job problem by
    Campbell, Dudek, and Smith (CDS) heuristic.

    Parameters
    ----------
    frame: JobSchedulingFrame

    Returns
    -------
    solution: list
        sequence of job index

    Notes
    -----
    Developed by Campbell, Dudek, and Smith in 1970.

    """
    johnson_frame = JobSchedulingFrame([[]])
    johnson_solutions_with_end_time = []

    # Create `count_machines - 1` sub-problems
    # which will be solved by Johnson's algorithm
    for sub_problem in range(1, frame.count_machines):
        # Create processing times matrix for all jobs on only 2 machines
        proc_times = cds_create_proc_times(frame, sub_problem)
        johnson_frame.set_processing_times(proc_times)
        johnson_solution = johnson_algorithm(johnson_frame)

        # end time compute for the original task, that is `frame`
        end_time = compute_end_time(frame, johnson_solution)
        johnson_solutions_with_end_time.append((johnson_solution, end_time))

    johnson_solutions_with_end_time.sort(key=lambda elem: elem[1])

    # return only solution with minimum makespan (end_time)
    return johnson_solutions_with_end_time[0][0]


def neh_heuristics(frame: JobSchedulingFrame) -> list:
    """
    Compute approximate solution for instance of Flow Job problem by
    NEH heuristic.

    Parameters
    ----------
    frame: JobSchedulingFrame

    Returns
    -------
    solution: list
        sequence of job index

    Notes
    -----
    Journal Paper:
        Nawaz,M., Enscore,Jr.E.E, and Ham,I. (1983) A Heuristics Algorithm for
        the m Machine, n Job Flowshop Sequencing Problem.
        Omega-International Journal of Management Science 11(1), 91-95

    """
    count_jobs = frame.count_jobs

    all_processing_times = [0] * count_jobs
    for j in range(count_jobs):
        all_processing_times[j] = frame.get_sum_processing_time(j)

    init_jobs = [j for j in range(count_jobs)]
    init_jobs.sort(key=lambda x: all_processing_times[x], reverse=True)

    solution = local_search_partitial_sequence(frame, init_jobs)
    return solution


# supported functions for liu_reeves_heuristric heuristics ####################
def _weighted_idle_time(frame: JobSchedulingFrame,
                        scheduled_jobs: list, next_job: int) -> float:
    # TODO make sure that `jobs` does not change
    # during the operation of the function
    scheduled_jobs.append(next_job)
    sch = create_schedule(frame, scheduled_jobs)
    idle_time = 0.

    if len(scheduled_jobs) != 1:
        idx_second_last_job = scheduled_jobs[-2]
        idx_last_job = scheduled_jobs[-1]
        for idx_machine in range(1, frame.count_machines):
            cmpl_time1 = sch.end_time(idx_last_job, idx_machine - 1)
            cmpl_time2 = sch.end_time(idx_second_last_job, idx_machine)
            numerator = frame.count_machines * max(cmpl_time1 - cmpl_time2, 0)
            denominator = idx_machine + (len(scheduled_jobs) - 1) * \
                (frame.count_machines - idx_machine) / (frame.count_jobs - 2)
            idle_time += numerator / denominator
    else:
        idx_last_job = scheduled_jobs[-1]
        for idx_machine in range(1, frame.count_machines):
            cmpl_time1 = sch.end_time(idx_last_job, idx_machine - 1)
            numerator = frame.count_machines * cmpl_time1
            denominator = idx_machine + (len(scheduled_jobs) - 1) * \
                (frame.count_machines - idx_machine) / (frame.count_jobs - 2)
            idle_time += numerator / denominator

    scheduled_jobs.pop()  # remove this; see TODO
    return idle_time


def _artificial_time(frame: JobSchedulingFrame,
                     jobs: list, unscheduled_jobs: list) -> int:
    #  copy processing time matrix jobs x machines from frame
    processing_times = frame.copy_proc_time

    #  creating processing times for artificial job as average of
    #  the processing times of jobs from `unscheduled_jobs`
    artificial_prc_times = []
    for idx_machine in range(frame.count_machines):
        average_time = 0.
        for idx_job in range(len(unscheduled_jobs)):
            average_time += processing_times[idx_job][idx_machine]

        average_time /= len(unscheduled_jobs)
        artificial_prc_times.append(round(average_time))

    processing_times.append(artificial_prc_times)

    assert frame.count_jobs + 1 == len(processing_times)
    assert frame.count_machines == len(processing_times[0])

    frame_with_artificial_job = JobSchedulingFrame(processing_times)
    jobs.append(frame.count_jobs - 1)  # added index of artificial job

    if len(jobs) != 1:
        end_time_sec_last_job = compute_end_time(frame_with_artificial_job,
                                                 jobs, len(jobs) - 1,
                                                 frame.count_machines - 1)
    else:
        end_time_sec_last_job = 0

    end_time_last_job = compute_end_time(frame_with_artificial_job,
                                         jobs, len(jobs),
                                         frame.count_machines - 1)
    result_time = end_time_sec_last_job + end_time_last_job
    jobs.pop()
    return result_time


def _index_function(frame: JobSchedulingFrame, jobs: list,
                    unscheduled_jobs: list, next_job: int) -> float:
    return (frame.count_jobs - len(jobs) - 2) * \
        _weighted_idle_time(frame, jobs, next_job) + \
        _artificial_time(frame, jobs, unscheduled_jobs)
###############################################################################


def liu_reeves_heuristics(frame: JobSchedulingFrame, count_sequences: int):
    init_sequence = [idx_job for idx_job in range(frame.count_jobs)]
    from copy import copy
    unscheduled_jobs = copy(init_sequence)
    init_sequence.sort(key=lambda next_job: _index_function(frame, [],
                                                            unscheduled_jobs,
                                                            next_job))

    solutions = []

    for idx in range(count_sequences):
        solution = [init_sequence[idx]]

        unscheduled_jobs.remove(init_sequence[idx])
        for _ in range(frame.count_jobs - 1):
            min_job = min(unscheduled_jobs,
                          key=lambda next_job: _index_function(
                                                    frame, solution,
                                                    unscheduled_jobs,
                                                    next_job))
            solution.append(min_job)
            unscheduled_jobs.remove(min_job)
        solutions.append(solution)
        unscheduled_jobs = copy(init_sequence)

    solutions.sort(key=lambda solution: compute_end_time(frame, solution))
    return solutions[0]
