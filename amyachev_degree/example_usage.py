from amyachev_degree.core import create_schedule, flow_job_generator, johnson_three_machines_generator
from amyachev_degree.io_my import read_flow_shop_instances, create_gantt_chart
from amyachev_degree.simple_heuristics import neh_heuristics, palmer_heuristics, campbell_dudek_smith
from amyachev_degree.exact_algorithm import johnson_algorithm
import time

start = time.time()
criterion = []
# job_scheduling_frames = read_flow_shop_instances('D:/pipeline_task.txt')
job_scheduling_frames = []

for i in range(10):
    job_scheduling_frames.append(johnson_three_machines_generator(500, 873654221 + i))

print('count job - ' + str(job_scheduling_frames[0].count_jobs) + ' count_machines - ' +
      str(job_scheduling_frames[0].count_machines))
cds_end_times = []
neh_end_times = []
for frame in job_scheduling_frames:
    start_heuristics = time.time()
    cds_sequence = campbell_dudek_smith(frame)
    cds_schedule = create_schedule(cds_sequence, frame.processing_times)
    # gnt = create_gantt_chart(schedule_1)
    cds_end_times.append(cds_schedule.end_time)
    print('cds task done - ' + str(cds_schedule.end_time))
    neh_sequence = neh_heuristics(frame)
    neh_schedule = create_schedule(neh_sequence, frame.processing_times)
    neh_end_times.append(neh_schedule.end_time)
    print('neh task done - ' + str(neh_schedule.end_time))

end = time.time() - start
print("Elapsed time - %f" % end)
sum = 0
for i in range(10):
    sum += (neh_end_times[i] / cds_end_times[i]) - 1
print("average % - ", sum / 10)
# TODO implement lower bound of flow shop problem
