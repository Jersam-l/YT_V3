import numpy as np
import pytest

from naca6.input.designation import parse_designation
from naca6.core.parameters import parse_parameters
from naca6.equations.epsilon_psi import (
    calculate_epsilon,
    calculate_psi,
)


def make_parameters(
    designation="66(2)-015",
):
    d = parse_designation(designation)

    return parse_parameters(
        "1.0",
        "201",
        d,
    )


def test_epsilon_returns_correct_size():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    epsilon = calculate_epsilon(
        phi,
        parameters,
    )

    assert epsilon.shape == phi.shape


def test_psi_returns_correct_size():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    psi = calculate_psi(
        phi,
        parameters,
    )

    assert psi.shape == phi.shape


def test_epsilon_is_finite():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    epsilon = calculate_epsilon(
        phi,
        parameters,
    )

    assert np.all(
        np.isfinite(epsilon)
    )


def test_psi_is_finite():

    parameters = make_parameters()

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    psi = calculate_psi(
        phi,
        parameters,
    )

    assert np.all(
        np.isfinite(psi)
    )


def test_epsilon_changes_with_series():

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    p63 = make_parameters(
        "63(2)-015"
    )

    p66 = make_parameters(
        "66(2)-015"
    )

    e63 = calculate_epsilon(
        phi,
        p63,
    )

    e66 = calculate_epsilon(
        phi,
        p66,
    )

    assert not np.allclose(
        e63,
        e66,
    )


def test_psi_changes_with_series():

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    p63 = make_parameters(
        "63(2)-015"
    )

    p66 = make_parameters(
        "66(2)-015"
    )

    psi63 = calculate_psi(
        phi,
        p63,
    )

    psi66 = calculate_psi(
        phi,
        p66,
    )

    assert not np.allclose(
        psi63,
        psi66,
    )


def test_epsilon_rejects_invalid_phi():

    parameters = make_parameters()

    phi = np.array(
        [-0.1, 0.5, np.pi]
    )

    with pytest.raises(ValueError):

        calculate_epsilon(
            phi,
            parameters,
        )


def test_psi_rejects_invalid_phi():

    parameters = make_parameters()

    phi = np.array(
        [0.0, 0.5, np.pi + 0.1]
    )

    with pytest.raises(ValueError):

        calculate_psi(
            phi,
            parameters,
        )


def test_epsilon_rejects_unsupported_series():

    parameters = make_parameters(
        "68(2)-015"
    )

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    with pytest.raises(ValueError):

        calculate_epsilon(
            phi,
            parameters,
        )