from amyachev_degree.core import (
    JobSchedulingFrame, compute_end_time, create_schedule)
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


# supported functions for CDS heuristics ######################################
def _cds_first_stage(frame: JobSchedulingFrame, sub_problem: int) -> list:
    processing_times = []

    for idx_job in range(frame.count_jobs):
        time = 0
        # From `sub_problem` count machines will make one artificial,
        # summing up the processing times on each of them.
        for idx_machine in range(sub_problem):
            time += frame.get_processing_time(idx_job, idx_machine)
        processing_times.append(time)

    return processing_times


def _cds_second_stage(frame: JobSchedulingFrame, sub_problem: int) -> list:
    processing_times = []
    count_machines = frame.count_machines

    for idx_job in range(frame.count_jobs):
        time = 0
        # From `sub_problem` machines will make one artificial,
        # summing up the processing times on each of them.
        for idx_machine in range(count_machines - sub_problem, count_machines):
            time += frame.get_processing_time(idx_job, idx_machine)
        processing_times.append(time)

    return processing_times
###############################################################################


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
    Developed by Campbell, Dudek, and Smith in 1970
    """
    frame = JobSchedulingFrame([[]])
    johnson_solutions_with_end_time = []

    # Create `count_machines - 1` sub-problems
    # which will be solved by Johnson's algorithm
    for sub_problem in range(1, flow_job_frame.count_machines):
        # Create processing times matrix for all jobs on only 2 machines
        proc_times = [_cds_first_stage(flow_job_frame, sub_problem),
                      _cds_second_stage(flow_job_frame, sub_problem)]
        proc_times = list(zip(*proc_times))  # transposition
        frame.set_processing_times(proc_times)

        johnson_solution = johnson_algorithm(frame)
        end_time = compute_end_time(flow_job_frame, johnson_solution)
        johnson_solutions_with_end_time.append((johnson_solution, end_time))

    johnson_solutions_with_end_time.sort(key=lambda elem: elem[1])

    # return only solution with minimum makespan (end_time)
    return johnson_solutions_with_end_time[0][0]


def neh_heuristics(flow_job_frame: JobSchedulingFrame) -> list:
    """
    Compute approximate solution for instance of Flow Job problem by
    NEH heuristic.

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
    solution = [init_jobs[0]]  # using job, which have max processing time

    # the number is obviously greater than the minimum end time
    time_compare = compute_end_time(flow_job_frame, init_jobs) + 1

    # local search
    for position_job, idx_job in enumerate(init_jobs[1:], 1):
        min_end_time = time_compare
        for insert_place in range(position_job + 1):
            solution.insert(insert_place, idx_job)

            end_time = compute_end_time(flow_job_frame, solution)
            if min_end_time > end_time:
                min_end_time = end_time
                best_insert_place = insert_place

            solution.pop(insert_place)
        solution.insert(best_insert_place, idx_job)

    return solution


# TODO removed using 'create_schedule' for receiving only end_time
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
