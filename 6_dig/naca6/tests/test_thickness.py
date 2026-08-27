import numpy as np
import pytest

from naca6.input.designation import parse_designation
from naca6.core.parameters import parse_parameters
from naca6.equations.thickness import calculate_thickness


def make_parameters(
    designation="66(2)-015",
    chord="1.0",
    points="201",
):
    designation = parse_designation(
        designation
    )

    return parse_parameters(
        chord,
        points,
        designation,
    )


def test_thickness_returns_correct_size():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    x_bar, thickness = calculate_thickness(
        phi,
        parameters,
    )

    assert x_bar.shape == phi.shape
    assert thickness.shape == phi.shape


def test_thickness_is_finite():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    x_bar, thickness = calculate_thickness(
        phi,
        parameters,
    )

    assert np.all(
        np.isfinite(x_bar)
    )

    assert np.all(
        np.isfinite(thickness)
    )


def test_thickness_is_non_negative():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    x_bar, thickness = calculate_thickness(
        phi,
        parameters,
    )

    assert np.all(
        thickness >= 0.0
    )


def test_thickness_changes_with_designation():

    p1 = make_parameters(
        designation="66(2)-012"
    )

    p2 = make_parameters(
        designation="66(2)-018"
    )

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    _, t1 = calculate_thickness(
        phi,
        p1,
    )

    _, t2 = calculate_thickness(
        phi,
        p2,
    )

    assert not np.allclose(
        t1,
        t2,
    )


def test_invalid_phi_is_rejected():

    parameters = make_parameters()

    phi = np.array(
        [-0.1, 0.5, np.pi]
    )

    with pytest.raises(ValueError):
        calculate_thickness(
            phi,
            parameters,
        )