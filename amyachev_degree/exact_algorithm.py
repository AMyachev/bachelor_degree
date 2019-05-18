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
        raise ValueError('count machines must be 2')

    # init job indexes
    exact_solution = [i for i in range(frame.count_jobs)]

    # sorting by increasing the minimum processing time
    exact_solution.sort(
        key=lambda idx_job: min(
            frame.get_processing_time(idx_job, idx_machine=0),
            frame.get_processing_time(idx_job, idx_machine=1)
        )
    )

    jobs_on_first_machine = []
    jobs_on_second_machine = []

    # distribution of jobs on machines
    for idx_job in exact_solution:
        frst = frame.get_processing_time(idx_job, idx_machine=0)
        scnd = frame.get_processing_time(idx_job, idx_machine=1)
        if frst < scnd:
            jobs_on_first_machine.append(idx_job)
        else:
            jobs_on_second_machine.append(idx_job)

    exact_solution = jobs_on_first_machine

    # simulating the installation of jobs that are processed faster on the
    # second machine to the end of the processing queue on the first machine
    jobs_on_second_machine.reverse()
    exact_solution.extend(jobs_on_second_machine)

    return exact_solution
