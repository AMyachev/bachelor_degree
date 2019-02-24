def johnson_algorithm(_johnson_scheduling_frame):
    def min_with_check(job_times, _job_in_permutation):
        min_time = -1
        for index, _time in enumerate(job_times):
            if _job_in_permutation[index] == 0:
                if min_time == -1:
                    min_time = _time
                elif _time < min_time:
                    min_time = _time
        return min_time

    def index_with_check(job_times, min_value, _job_in_permutation):
        for index, _time in enumerate(job_times):
            if _time == min_value and _job_in_permutation[index] == 0:
                return index
        return -1

    output = []
    index_insert = 0
    job_in_permutation = [0 for _ in range(_johnson_scheduling_frame.count_jobs)]
    if _johnson_scheduling_frame.count_machines != 2:
        raise ValueError

    first_machine_time = _johnson_scheduling_frame.processing_time[0]
    second_machine_time = _johnson_scheduling_frame.processing_time[1]

    min_item_first_machine = min_with_check(first_machine_time, job_in_permutation)
    min_item_second_machine = min_with_check(second_machine_time, job_in_permutation)

    for i in range(_johnson_scheduling_frame.count_jobs):
        if min_item_first_machine == -1 or min_item_second_machine == -1:
            raise ValueError
        if min_item_first_machine > min_item_second_machine:
            index_job = index_with_check(second_machine_time, min_item_second_machine, job_in_permutation)
            if index_job == -1:
                raise ValueError
            output.insert(index_insert, index_job)
            job_in_permutation[index_job] = 1

            min_item_first_machine = min_with_check(first_machine_time, job_in_permutation)
            min_item_second_machine = min_with_check(second_machine_time, job_in_permutation)

        else:
            index_job = index_with_check(first_machine_time, min_item_first_machine, job_in_permutation)
            if index_job == -1:
                raise ValueError
            output. insert(index_insert, index_job)
            job_in_permutation[index_job] = 1
            index_insert += 1

            min_item_first_machine = min_with_check(first_machine_time, job_in_permutation)
            min_item_second_machine = min_with_check(second_machine_time, job_in_permutation)

    return output
