import numpy as np
import pytest

from naca6.numerics.integration import integrate


def test_integral_of_constant():

    x = np.linspace(
        0.0,
        1.0,
        101,
    )

    y = np.ones_like(x)

    result = integrate(
        x,
        y,
    )

    assert np.isclose(
        result,
        1.0,
    )


def test_integral_of_x():

    x = np.linspace(
        0.0,
        1.0,
        101,
    )

    y = x

    result = integrate(
        x,
        y,
    )

    assert np.isclose(
        result,
        0.5,
        atol=1e-4,
    )


def test_integral_of_x_squared():

    x = np.linspace(
        0.0,
        1.0,
        1001,
    )

    y = x**2

    result = integrate(
        x,
        y,
    )

    assert np.isclose(
        result,
        1.0 / 3.0,
        atol=1e-5,
    )


def test_integral_sine():

    x = np.linspace(
        0.0,
        np.pi,
        1001,
    )

    y = np.sin(x)

    result = integrate(
        x,
        y,
    )

    assert np.isclose(
        result,
        2.0,
        atol=1e-5,
    )


def test_integral_requires_one_dimension():

    x = np.array(
        [[0.0, 1.0]]
    )

    y = np.array(
        [[0.0, 1.0]]
    )

    with pytest.raises(ValueError):

        integrate(
            x,
            y,
        )


def test_integral_requires_matching_lengths():

    x = np.array(
        [0.0, 0.5, 1.0]
    )

    y = np.array(
        [0.0, 1.0]
    )

    with pytest.raises(ValueError):

        integrate(
            x,
            y,
        )


def test_integral_requires_two_points():

    x = np.array(
        [0.0]
    )

    y = np.array(
        [1.0]
    )

    with pytest.raises(ValueError):

        integrate(
            x,
            y,
        )
        