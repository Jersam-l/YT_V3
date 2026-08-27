import numpy as np

from .epsilon_psi import (
    calculate_epsilon,
    calculate_psi,
)
from .conformal_mapping import conformal_map


def calculate_thickness(phi, parameters):
    """
    Calculate the actual NACA 6-series half-thickness
    from the NACA epsilon/psi conformal transformation.

    Parameters
    ----------
    phi : ndarray
        Angular coordinate, 0 <= phi <= pi.

    parameters : NACA6Parameters
        Validated NACA 6-series parameters.

    Returns
    -------
    x_bar : ndarray
        Chord-normalized thickness-section x coordinate.

    thickness : ndarray
        Chord-normalized half-thickness.
    """

    phi = np.asarray(phi, dtype=float)

    if phi.ndim != 1:
        raise ValueError(
            "phi must be one-dimensional."
        )

    if np.any(phi < 0.0) or np.any(phi > np.pi):
        raise ValueError(
            "phi must be between 0 and pi."
        )

    epsilon = calculate_epsilon(
        phi,
        parameters,
    )

    psi = calculate_psi(
        phi,
        parameters,
    )

    x_bar, y_bar = conformal_map(
        phi,
        psi,
        epsilon,
    )

    thickness = np.abs(y_bar)

    return x_bar, thickness