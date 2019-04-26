from amyachev_degree import (
    read_flow_shop_instances, neh_heuristics, create_schedule)
import time

start = time.time()
criterion = []
job_scheduling_frames = read_flow_shop_instances('D:/pipeline_task.txt')
# job_scheduling_frames = []

# for i in range(10):
#    job_scheduling_frames.append(flow_job_generator(20, 2, 873654221 + i))

print('count job - ' + str(job_scheduling_frames[0].count_jobs) +
      ' count_machines - ' + str(job_scheduling_frames[0].count_machines))
neh_end_times = []
for frame in job_scheduling_frames:
    print(frame)
    start_heuristics = time.time()
    neh_sequence = neh_heuristics(frame)
    print("johnson_sequence", neh_sequence)
    neh_schedule = create_schedule(neh_sequence, frame.processing_times)
    neh_end_times.append(neh_schedule.end_time)

diff = 0.
for i in range(len(job_scheduling_frames)):
    if job_scheduling_frames[i].upper_bound_makespan > neh_end_times[i]:
        print(neh_end_times[i])
    diff += neh_end_times[i] / job_scheduling_frames[i].upper_bound_makespan

print(neh_end_times)
print("diff ", diff / 10)
# TODO implement lower bound of flow shop problem
