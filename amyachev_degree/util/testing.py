from amyachev_degree.core import JobSchedulingFrame


def assert_js_frame(fst: JobSchedulingFrame, scnd: JobSchedulingFrame) -> bool:
    assert str(fst) == str(scnd)
