from amyachev_degree import (
    read_flow_shop_instances, neh_heuristics, create_schedule)

instances = read_flow_shop_instances("D:/pipeline_task.txt")

solution = neh_heuristics(instances[1])

schedule = create_schedule(instances[1], solution)
sch = create_schedule(instances[1], solution, 5, 5)
print(schedule.end_time)
print(schedule)
print(sch.end_time)
print(sch)


# TODO implement lower bound of flow shop problem
