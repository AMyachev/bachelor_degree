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
    result of local search: bool
        if the `init_jobs` is changed , returns True.

    Notes
    -----
    Modifies the original job sequence

    """
    changed_init_jobs = False

    # hack for start the loop
    improvement = True

    while improvement:
        improvement = False
        for idx in range(len(init_jobs) - 1):
            best_flowshop_time = compute_end_time(frame, init_jobs)

            swap(init_jobs, idx, idx + 1)

            new_flowshop_time = compute_end_time(frame, init_jobs)
            if best_flowshop_time > new_flowshop_time:
                best_flowshop_time = new_flowshop_time
                improvement = True
                changed_init_jobs = True
            else:
                # reverse swap
                swap(init_jobs, idx, idx + 1)

    return changed_init_jobs


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
    result of local search: list

    Notes
    -----
    don't modificate `init_jobs`

    """
    solution = [init_jobs[0]]  # using job, which have max processing time

    # the number is obviously greater than the minimum end time
    time_compare = compute_end_time(frame, init_jobs) + 1

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

    return solution
