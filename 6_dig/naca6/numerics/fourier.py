import numpy as np


def fourier_sine_coefficients(phi, values, order):

    phi = np.asarray(phi, dtype=float)
    values = np.asarray(values, dtype=float)

    if phi.ndim != 1 or values.ndim != 1:
        raise ValueError(
            "phi and values must be one-dimensional."
        )

    if phi.shape != values.shape:
        raise ValueError(
            "phi and values must have the same shape."
        )

    if len(phi) < 2:
        raise ValueError(
            "At least two points are required."
        )

    if order < 1:
        raise ValueError(
            "order must be positive."
        )

    if np.any(np.diff(phi) <= 0.0):
        raise ValueError(
            "phi must be strictly increasing."
        )

    coefficients = np.zeros(
        order,
        dtype=float,
    )

    for n in range(1, order + 1):

        coefficients[n - 1] = (
            2.0 / np.pi
            * np.trapezoid(
                values * np.sin(n * phi),
                phi,
            )
        )

    return coefficients


def fourier_cosine_coefficients(phi, values, order):

    phi = np.asarray(phi, dtype=float)
    values = np.asarray(values, dtype=float)

    if phi.ndim != 1 or values.ndim != 1:
        raise ValueError(
            "phi and values must be one-dimensional."
        )

    if phi.shape != values.shape:
        raise ValueError(
            "phi and values must have the same shape."
        )

    if len(phi) < 2:
        raise ValueError(
            "At least two points are required."
        )

    if order < 1:
        raise ValueError(
            "order must be positive."
        )

    if np.any(np.diff(phi) <= 0.0):
        raise ValueError(
            "phi must be strictly increasing."
        )

    coefficients = np.zeros(
        order,
        dtype=float,
    )

    for n in range(1, order + 1):

        coefficients[n - 1] = (
            2.0 / np.pi
            * np.trapezoid(
                values * np.cos(n * phi),
                phi,
            )
        )

    return coefficients


def reconstruct_from_fourier(
    phi,
    sine_coefficients,
    cosine_coefficients,
):

    phi = np.asarray(
        phi,
        dtype=float,
    )

    sine_coefficients = np.asarray(
        sine_coefficients,
        dtype=float,
    )

    cosine_coefficients = np.asarray(
        cosine_coefficients,
        dtype=float,
    )

    if phi.ndim != 1:
        raise ValueError(
            "phi must be one-dimensional."
        )

    if sine_coefficients.ndim != 1:
        raise ValueError(
            "sine_coefficients must be one-dimensional."
        )

    if cosine_coefficients.ndim != 1:
        raise ValueError(
            "cosine_coefficients must be one-dimensional."
        )

    if len(sine_coefficients) != len(
        cosine_coefficients
    ):
        raise ValueError(
            "Sine and cosine coefficient arrays "
            "must have the same length."
        )

    result = np.zeros_like(phi)

    for n in range(
        1,
        len(sine_coefficients) + 1,
    ):

        result += (
            sine_coefficients[n - 1]
            * np.sin(n * phi)
            +
            cosine_coefficients[n - 1]
            * np.cos(n * phi)
        )

    return result