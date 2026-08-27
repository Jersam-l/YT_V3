import numpy as np


def conformal_map(phi, psi, epsilon, a=1.0):
    """
    NACA 6-series conformal transformation.

    This is the Python translation of SetSixDigitPoints()
    from the NACA/PDAS NacaAuxilary source.

    Returns
    -------
    x : ndarray
        Chord-normalized thickness-section x coordinates.
    y : ndarray
        Chord-normalized half-thickness coordinates.
    """

    phi = np.asarray(phi, dtype=float)
    psi = np.asarray(psi, dtype=float)
    epsilon = np.asarray(epsilon, dtype=float)

    if phi.ndim != 1:
        raise ValueError("phi must be one-dimensional.")

    if phi.shape != psi.shape or phi.shape != epsilon.shape:
        raise ValueError(
            "phi, psi and epsilon must have identical shapes."
        )

    if phi.size < 2:
        raise ValueError(
            "At least two points are required."
        )

    if a <= 0.0:
        raise ValueError("a must be positive.")

    # ------------------------------------------------------------------
    # NACA SetSixDigitPoints:
    #
    # z = a * exp(psi(1) + i*phi)
    #
    # zprime = z * exp((psi-psi(1)) - i*epsilon)
    #
    # zeta = zprime + a^2/zprime
    #
    # zfinal = (zeta(1)-zeta) /
    #          abs(zeta(N)-zeta(1))
    # ------------------------------------------------------------------

    z = a * np.exp(
        psi[0] + 1j * phi
    )

    zprime = z * np.exp(
        (psi - psi[0]) - 1j * epsilon
    )

    zeta = (
        zprime
        + (a * a) / zprime
    )

    denominator = np.abs(
        zeta[-1] - zeta[0]
    )

    if denominator == 0.0:
        raise ValueError(
            "Degenerate conformal transformation."
        )

    zfinal = (
        zeta[0] - zeta
    ) / denominator

    x = np.real(zfinal)
    y = -np.imag(zfinal)

    return x, y