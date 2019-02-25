from core import create_schedule
from io_my import read_file_with_flow_shop, create_gantt_chart
from simple_heuristics import neh_heuristics


job_scheduling_task = read_file_with_flow_shop('D:\\pipeline_task.txt')
neh_sequence = neh_heuristics(job_scheduling_task)
print("neh's sequence :", neh_sequence)
schedule_1 = create_schedule(neh_sequence, job_scheduling_task.processing_time)
create_gantt_chart(schedule_1)
print("neh's end_time", schedule_1.end_time)

# TODO implement lower bound of flow shop problem
