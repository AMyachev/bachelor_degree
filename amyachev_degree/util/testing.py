from amyachev_degree.core import compute_end_time, JobSchedulingFrame


def assert_js_frame(fst: JobSchedulingFrame, scnd: JobSchedulingFrame) -> bool:
    assert str(fst) == str(scnd)


def my_round(value):
    """
    Arithmetic rounding.

    Parameters
    ----------
    value: numeric value

    Returns
    -------
    : int

    Notes
    -----
    Python3 uses default banking rounding.
    """
    return int(value + 0.5)


def percentage_deviation(fst_heuristic: object, fst_args: dict,
                         scnd_heuristic: object, scnd_args: dict,
                         frames: list) -> float:
    """
    The calculations are performed with respect to the results
    of the second heuristics.

    Parameters
    ----------
    fst_heuristic: object
        function callback
    fst_args: dict
        named arguments for `fst_heuristic`
    scnd_heuristic: object
        function callback
    scnd_args: dict
        named arguments for `scnd_heuristic`
    frames: list
        list of `JobSchedulingFrame` objects

    Returns
    -------
    average_deviation: float

    Notes
    -----
    Averaging occurs by the count of frames.

    """
    solutions_ratio = 0.
    for frame in frames:
        fst_solution = fst_heuristic(frame, **fst_args)
        fst_end_time = compute_end_time(frame, fst_solution)

        scnd_solution = scnd_heuristic(frame, **scnd_args)
        scnd_end_time = compute_end_time(frame, scnd_solution)

        end_time_diff = fst_end_time - scnd_end_time
        solutions_ratio += end_time_diff / scnd_end_time

    return solutions_ratio / len(frames) * 100


def percentage_deviation_using_upper_bound(fst_heuristic: object,
                                           fst_args: dict,
                                           frames: list) -> float:
    """
    The calculations are performed with respect to the results that are
    stored by frames in `upper_bound` property.

    Parameters
    ----------
    fst_heuristic: object
        function callback
    fst_args: dict
        named arguments for `fst_heuristic`
    frames: list
        list of `JobSchedulingFrame` objects

    Returns
    -------
    average_deviation: float

    Notes
    -----
    Averaging occurs by the count of frames.

    """
    solutions_ratio = 0.
    for frame in frames:
        fst_solution = fst_heuristic(frame, **fst_args)
        fst_end_time = compute_end_time(frame, fst_solution)

        end_time_diff = fst_end_time - frame.upper_bound
        solutions_ratio += end_time_diff / frame.upper_bound

    return solutions_ratio / len(frames) * 100
