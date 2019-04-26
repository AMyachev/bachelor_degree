from amyachev_degree.core import create_schedule

test_1 = create_schedule([2, 4, 3, 0, 1], [[17, 19, 13], [15, 11, 12],
                                           [14, 21, 16], [20, 16, 20],
                                           [16, 17, 17]])
assert test_1.end_time == 114
test_2 = create_schedule([4, 2, 3, 0, 1], [[17, 19, 13], [15, 11, 12],
                                           [14, 21, 16], [20, 16, 20],
                                           [16, 17, 17]])
assert test_2.end_time == 115
