import numpy as np

from ..equations.meanline import calculate_meanline


def test_meanline_returns_correct_size():

    x_bar = np.linspace(0.0, 1.0, 100)

    a = 1.0
    cli = 0.2

    ym = calculate_meanline(x_bar, a, cli)

    assert isinstance(ym, np.ndarray)
    assert len(ym) == len(x_bar)


def test_meanline_starts_and_ends_at_zero():

    x_bar = np.linspace(0.0, 1.0, 100)

    a = 1.0
    cli = 0.2

    ym = calculate_meanline(x_bar, a, cli)

    assert np.isclose(ym[0], 0.0)
    assert np.isclose(ym[-1], 0.0)


def test_zero_lift_gives_zero_meanline():

    x_bar = np.linspace(0.0, 1.0, 100)

    a = 1.0
    cli = 0.0

    ym = calculate_meanline(x_bar, a, cli)

    assert np.allclose(ym, 0.0)


def test_meanline_changes_with_lift_coefficient():

    x_bar = np.linspace(0.0, 1.0, 100)

    a = 1.0

    ym_01 = calculate_meanline(x_bar, a, 0.1)
    ym_02 = calculate_meanline(x_bar, a, 0.2)

    assert not np.allclose(ym_01, ym_02)


def test_meanline_changes_with_a():

    x_bar = np.linspace(0.0, 1.0, 100)

    cli = 0.2

    ym_a1 = calculate_meanline(x_bar, 1.0, cli)
    ym_a08 = calculate_meanline(x_bar, 0.8, cli)

    assert not np.allclose(ym_a1, ym_a08)


def test_invalid_a_is_rejected():

    x_bar = np.linspace(0.0, 1.0, 100)

    try:
        calculate_meanline(x_bar, 0.0, 0.2)
    except ValueError:
        pass
    else:
        raise AssertionError("a = 0 should raise ValueError")