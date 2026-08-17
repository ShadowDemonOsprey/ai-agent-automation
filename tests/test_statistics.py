"""
Statistics tool tests.
"""


from app.tools.statistics import statistics


def test_basic_statistics():
    result = statistics("1, 2, 3, 4, 5")

    assert result["count"] == 5
    assert result["sum"] == 15
    assert result["mean"] == 3
    assert result["median"] == 3
    assert result["min"] == 1
    assert result["max"] == 5
    assert result["range"] == 4


def test_even_count_median():
    result = statistics("1 2 3 4")
    assert result["median"] == 2.5


def test_odd_count_median():
    result = statistics("1 2 3 4 5 6 7")
    assert result["median"] == 4


def test_mode():
    result = statistics("1 1 2 2 2 3")
    assert result["mode"] == [2]


def test_variance_and_stddev():
    result = statistics("2 4 4 4 5 5 7 9")

    assert result["mean"] == 5

    assert result["variance_population"] == 4

    assert result["stddev_population"] == 2


def test_quartiles_and_iqr():
    result = statistics("1 2 3 4 5 6 7 8")

    assert result["q1"] == 2.5
    assert result["q3"] == 6.5
    assert result["iqr"] == 4


def test_no_numbers_returns_error():
    result = statistics("hello world")
    assert "error" in result


def test_negative_numbers():
    result = statistics("-5 -3 0 3 5")
    assert result["sum"] == 0
    assert result["min"] == -5
    assert result["max"] == 5
