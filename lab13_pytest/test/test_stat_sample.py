import pytest

from stat_sample import Sample

datatest_mean = [
    ([2.0, 4.0, 6.0], 4.0),
    ([12.0, 8.0, 4.0], 8.0)
]


@pytest.mark.parametrize('lst, mean', datatest_mean)
def test_sample_mean(lst, mean):
    s = Sample(lst)

    assert mean == s.avarage_mean()


datatest_variance = [
    ([2.0, 3.0, 4.0], 0.66667)
]


@pytest.mark.parametrize('lst, var', datatest_variance)
def test_sample_variance(lst, var):
    s = Sample(lst)
    v = s.variance()

    assert v == var


datatest_deviation = [
    ([2.0, 3.0, 4.0], 0.81650)
]


@pytest.mark.parametrize('lst, dev', datatest_deviation)
def test_sample_deviation(lst, dev):
    s = Sample(lst)
    d = s.standard_deviation()

    assert d == dev
