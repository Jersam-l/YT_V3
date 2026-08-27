import numpy as np
import pytest

from naca6.numerics.fourier import (
    fourier_sine_coefficients,
    fourier_cosine_coefficients,
    reconstruct_from_fourier,
)


def test_sine_coefficients_return_correct_size():

    phi = np.linspace(
        0.0,
        np.pi,
        1001,
    )

    values = np.sin(phi)

    coefficients = fourier_sine_coefficients(
        phi,
        values,
        5,
    )

    assert coefficients.shape == (5,)


def test_cosine_coefficients_return_correct_size():

    phi = np.linspace(
        0.0,
        np.pi,
        1001,
    )

    values = np.cos(phi)

    coefficients = fourier_cosine_coefficients(
        phi,
        values,
        5,
    )

    assert coefficients.shape == (5,)


def test_first_sine_coefficient():

    phi = np.linspace(
        0.0,
        np.pi,
        1001,
    )

    values = np.sin(phi)

    coefficients = fourier_sine_coefficients(
        phi,
        values,
        5,
    )

    assert np.isclose(
        coefficients[0],
        1.0,
        atol=1e-3,
    )


def test_first_cosine_coefficient():

    phi = np.linspace(
        0.0,
        np.pi,
        1001,
    )

    values = np.cos(phi)

    coefficients = fourier_cosine_coefficients(
        phi,
        values,
        5,
    )

    assert np.isclose(
        coefficients[0],
        1.0,
        atol=1e-3,
    )


def test_sine_and_cosine_coefficients_are_finite():

    phi = np.linspace(
        0.0,
        np.pi,
        1001,
    )

    values = (
        np.sin(phi)
        + 0.5 * np.cos(phi)
    )

    sine = fourier_sine_coefficients(
        phi,
        values,
        10,
    )

    cosine = fourier_cosine_coefficients(
        phi,
        values,
        10,
    )

    assert np.all(
        np.isfinite(sine)
    )

    assert np.all(
        np.isfinite(cosine)
    )


def test_reconstruction_returns_correct_size():

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    sine = np.array(
        [1.0, 0.0, 0.0]
    )

    cosine = np.array(
        [0.0, 0.5, 0.0]
    )

    result = reconstruct_from_fourier(
        phi,
        sine,
        cosine,
    )

    assert result.shape == phi.shape


def test_reconstruction_is_correct():

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    sine = np.array(
        [1.0]
    )

    cosine = np.array(
        [0.0]
    )

    result = reconstruct_from_fourier(
        phi,
        sine,
        cosine,
    )

    expected = np.sin(phi)

    assert np.allclose(
        result,
        expected,
    )


def test_fourier_rejects_mismatched_shapes():

    phi = np.linspace(
        0.0,
        np.pi,
        100,
    )

    values = np.linspace(
        0.0,
        1.0,
        50,
    )

    with pytest.raises(ValueError):

        fourier_sine_coefficients(
            phi,
            values,
            5,
        )


def test_fourier_rejects_invalid_order():

    phi = np.linspace(
        0.0,
        np.pi,
        100,
    )

    values = np.sin(phi)

    with pytest.raises(ValueError):

        fourier_sine_coefficients(
            phi,
            values,
            0,
        )


def test_reconstruction_rejects_mismatched_coefficients():

    phi = np.linspace(
        0.0,
        np.pi,
        100,
    )

    sine = np.array(
        [1.0, 0.0]
    )

    cosine = np.array(
        [1.0]
    )

    with pytest.raises(ValueError):

        reconstruct_from_fourier(
            phi,
            sine,
            cosine,
        )
        