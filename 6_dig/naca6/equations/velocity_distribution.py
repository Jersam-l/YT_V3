import numpy as np


def calculate_velocity_distribution(
    phi,
    psi,
    epsilon,
    alpha=0.0
):

    phi = np.asarray(phi, dtype=float)
    psi = np.asarray(psi, dtype=float)
    epsilon = np.asarray(epsilon, dtype=float)

    if phi.shape != psi.shape or phi.shape != epsilon.shape:
        raise ValueError(
            "phi, psi and epsilon must have identical shapes."
        )

    if phi.ndim != 1:
        raise ValueError("phi must be one-dimensional.")

    if len(phi) < 3:
        raise ValueError("At least three points are required.")

    theta = phi - epsilon

    dpsi = np.gradient(psi, phi)
    depsilon = np.gradient(epsilon, phi)

    numerator = (
        np.sin(alpha + phi)
        + np.sin(alpha + epsilon[-1])
    ) * np.exp(psi[0])

    denominator = np.sqrt(
        (
            np.sinh(psi) ** 2
            + np.sin(theta) ** 2
        )
        *
        (
            (1.0 - depsilon) ** 2
            + dpsi ** 2
        )
    )

    velocity_ratio = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(numerator),
        where=denominator > 0.0
    )

    return velocity_ratio