from amyachev_degree.core import Schedule

# schedule_frontal = frontal_algorithm(job_scheduling_task)
# create_gantt_chart(schedule_frontal)
# print("frontal end_time", schedule_frontal.end_time)


def frontal_algorithm(_job_scheduling_task):
    current_time = 0
    _schedule = {job: [] for job in range(_job_scheduling_task.count_jobs)}

    while not _job_scheduling_task.schedule_ready:
        ready_jobs = _job_scheduling_task.ready_jobs(current_time)
        ready_machines = _job_scheduling_task.ready_machines(current_time)
        for job in ready_jobs:
            next_car = _job_scheduling_task.next_ready_machine(job)
            if next_car in ready_machines:
                _job_scheduling_task.work_on_machine(job, next_car, current_time)
                _schedule[job].append((next_car, current_time,
                                      current_time + _job_scheduling_task.processing_time[job][next_car]))
            ready_machines = _job_scheduling_task.ready_machines(current_time)
        current_time += 1

    return Schedule(_schedule, current_time - 1)
