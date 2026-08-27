import numpy as np
import pytest

from naca6.equations.conformal_mapping import conformal_map


def test_conformal_map_returns_two_arrays():
    phi = np.linspace(0.0, np.pi, 201)
    psi = np.zeros(201)
    epsilon = np.zeros(201)

    x, y = conformal_map(
        phi,
        psi,
        epsilon,
    )

    assert isinstance(x, np.ndarray)
    assert isinstance(y, np.ndarray)

    assert x.shape == phi.shape
    assert y.shape == phi.shape


def test_conformal_map_produces_finite_values():
    phi = np.linspace(0.0, np.pi, 201)
    psi = np.zeros(201)
    epsilon = np.zeros(201)

    x, y = conformal_map(
        phi,
        psi,
        epsilon,
    )

    assert np.all(np.isfinite(x))
    assert np.all(np.isfinite(y))


def test_conformal_map_requires_matching_shapes():
    phi = np.linspace(0.0, np.pi, 201)
    psi = np.zeros(200)
    epsilon = np.zeros(201)

    with pytest.raises(ValueError):
        conformal_map(
            phi,
            psi,
            epsilon,
        )


def test_conformal_map_rejects_too_few_points():
    phi = np.linspace(0.0, np.pi, 1)
    psi = np.zeros(1)
    epsilon = np.zeros(1)

    with pytest.raises(ValueError):
        conformal_map(
            phi,
            psi,
            epsilon,
        )


def test_conformal_map_rejects_non_positive_a():
    phi = np.linspace(0.0, np.pi, 201)
    psi = np.zeros(201)
    epsilon = np.zeros(201)

    with pytest.raises(ValueError):
        conformal_map(
            phi,
            psi,
            epsilon,
            a=0.0,
        )