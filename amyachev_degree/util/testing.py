from amyachev_degree.core import JobSchedulingFrame


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
