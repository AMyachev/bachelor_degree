def johnson_algorithm(_johnson_scheduling_frame):
    """
    case of two machines of flow shop problem
    :param _johnson_scheduling_frame: JobSchedulingFrame
    :return: exact_solution: list of job index
    """
    if _johnson_scheduling_frame.count_machines != 2:
        raise ValueError

    # init job indexes
    exact_solution = [i for i in range(_johnson_scheduling_frame.count_jobs)]

    exact_solution.sort(
        key=lambda job_index: min(
            _johnson_scheduling_frame.get_processing_time(job_index, 0),
            _johnson_scheduling_frame.get_processing_time(job_index, 1)
        )
    )

    first_machine_jobs = []
    second_machine_jobs = []
    for job_index in exact_solution:
        frst = _johnson_scheduling_frame.get_processing_time(job_index, 0)
        scnd = _johnson_scheduling_frame.get_processing_time(job_index, 1)
        if frst < scnd:
            first_machine_jobs.append(job_index)
        else:
            second_machine_jobs.append(job_index)

    exact_solution = first_machine_jobs
    second_machine_jobs.reverse()
    exact_solution.extend(second_machine_jobs)

    return exact_solution
