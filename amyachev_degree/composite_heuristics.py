from amyachev_degree.core import JobSchedulingFrame, compute_end_time


def swap(sequence, fst, scnd):
    sequence[fst], sequence[scnd] = sequence[scnd], sequence[fst]


def local_search(frame: JobSchedulingFrame, init_sequence: list) -> list:
    for idx in range(len(init_sequence) - 1):
        best_flowshop_time = compute_end_time(frame, init_sequence)

        swap(init_sequence, idx, idx + 1)

        new_flowshop_time = compute_end_time(frame, init_sequence)
        if best_flowshop_time > new_flowshop_time:
            best_flowshop_time = new_flowshop_time
        else:
            # reverse swap
            swap(init_sequence, idx, idx + 1)

    return init_sequence
