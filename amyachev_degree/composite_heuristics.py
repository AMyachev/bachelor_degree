import copy
from amyachev_degree.core import JobSchedulingFrame, compute_end_time


def swap(sequence, fst, scnd):
    sequence[fst], sequence[scnd] = sequence[scnd], sequence[fst]


def local_search(frame: JobSchedulingFrame, init_jobs: list) -> list:
    """
    Local search occurs by pairwise exchange of jobs and evaluation
    of the total flow time.

    Parameters
    ----------
    frame: JobSchedulingFrame
    init_jobs: list

    Returns
    -------
    result of local search: list, bool
        if would be found a solution better than `init_jobs`, returns True.

    Notes
    -----
    don't modificate `init_jobs`

    """
    solution = copy.copy(init_jobs)
    different_from_init_jobs = False

    while True:
        improvement = False
        for idx in range(len(solution) - 1):
            best_flowshop_time = compute_end_time(frame, solution)
            swap(solution, idx, idx + 1)
            new_flowshop_time = compute_end_time(frame, solution)

            if best_flowshop_time > new_flowshop_time:
                best_flowshop_time = new_flowshop_time
                improvement = True
                different_from_init_jobs = True
            else:
                # reverse swap
                swap(solution, idx, idx + 1)

        if not improvement:
            break

    return solution, different_from_init_jobs


def local_search_partitial_sequence(frame: JobSchedulingFrame,
                                    init_jobs: list) -> list:
    """
    This perform for all jobs in `init_jobs`:
        Select the next job from `init_jobs` and insert it in all possible
        positions in the partial sequence and keep the best one (i.e. minimum
        flowsum) as the current partial sequence.

    Parameters
    ----------
    frame: JobSchedulingFrame
    init_jobs: list

    Returns
    -------
    result of local search: list, bool
        if would be found a solution better than `init_jobs`, returns True.

    Notes
    -----
    don't modificate `init_jobs`

    """
    solution = [init_jobs[0]]  # using job, which have max processing time
    better_than_init_jobs = False

    # init end time
    time_compare = compute_end_time(frame, init_jobs)

    # local search
    for position_job, idx_job in enumerate(init_jobs[1:], 1):
        min_end_time = time_compare
        for insert_place in range(position_job + 1):
            solution.insert(insert_place, idx_job)

            end_time = compute_end_time(frame, solution)
            if min_end_time > end_time:
                min_end_time = end_time
                best_insert_place = insert_place

            solution.pop(insert_place)
        solution.insert(best_insert_place, idx_job)

    solution_time = compute_end_time(frame, solution)
    better_than_init_jobs = solution_time < time_compare

    return solution, better_than_init_jobs
