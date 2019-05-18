from amyachev_degree.core import JobSchedulingFrame


def johnson_algorithm(frame: JobSchedulingFrame) -> list:
    """
    Compute solution for case of 2 machines of flow job problem by
    Johnson's algorithm.

    Parameters
    ----------
    frame: JobSchedulingFrame
        frame with exactly 2 machines

    Returns
    -------
    exact_solution: list
        list of job index
    """
    if frame.count_machines != 2:
        raise ValueError

    # init job indexes
    exact_solution = [i for i in range(frame.count_jobs)]

    exact_solution.sort(
        key=lambda job_index: min(
            frame.get_processing_time(job_index, 0),
            frame.get_processing_time(job_index, 1)
        )
    )

    first_machine_jobs = []
    second_machine_jobs = []
    for job_index in exact_solution:
        frst = frame.get_processing_time(job_index, 0)
        scnd = frame.get_processing_time(job_index, 1)
        if frst < scnd:
            first_machine_jobs.append(job_index)
        else:
            second_machine_jobs.append(job_index)

    exact_solution = first_machine_jobs
    second_machine_jobs.reverse()
    exact_solution.extend(second_machine_jobs)

    return exact_solution
