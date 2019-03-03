from amyachev_degree.core import create_schedule
from amyachev_degree.io_my import read_flow_shop_instances
from amyachev_degree.simple_heuristics import neh_heuristics, palmer_heuristics, campbell_dudek_smith

criterion = []
job_scheduling_frames = read_flow_shop_instances('D:/pipeline_task.txt')
print('count job - ' + str(job_scheduling_frames[0].count_jobs) + ' count_machines - ' +
      str(job_scheduling_frames[0].count_machines))
for frame in job_scheduling_frames:
    sequence = neh_heuristics(frame)
    schedule_1 = create_schedule(sequence, frame.processing_time)
    criterion.append(schedule_1.end_time / frame.upper_bound_makespan)
    print('one task done - ' + str(schedule_1.end_time))

answer = sum(criterion) / len(criterion)
print(str(round(answer * 100 - 100)) + '%')

# TODO implement lower bound of flow shop problem
