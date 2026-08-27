import numpy as np


def _validate_inputs(
    x_bar,
    a,
    cl,
):
    x_bar = np.asarray(
        x_bar,
        dtype=float,
    )

    if x_bar.ndim != 1:
        raise ValueError(
            "x_bar must be one-dimensional"
        )

    if np.any(x_bar < 0.0) or np.any(x_bar > 1.0):
        raise ValueError(
            "x_bar must lie between 0 and 1"
        )

    if not (
        0.0 < a <= 1.0
    ):
        raise ValueError(
            "a must satisfy 0 < a <= 1"
        )

    if not np.isfinite(cl):
        raise ValueError(
            "cl must be finite"
        )

    return x_bar


def _meanline_factor(
    x_bar,
    a,
):
    """
    NACA 6-series mean-line function.

    This is the dimensionless expression from
    NACA Report 824, equation (6).
    """

    x = np.asarray(
        x_bar,
        dtype=float,
    )

    result = np.zeros_like(
        x
    )

    # =========================================================
    # a = 1 limiting case
    # =========================================================

    if np.isclose(
        a,
        1.0,
    ):
        interior = (
            (x > 0.0)
            & (x < 1.0)
        )

        xi = x[interior]

        result[interior] = (
            (xi - 1.0)
            * np.log1p(-xi)
            - xi * np.log(xi)
        )

        return result

    # =========================================================
    # General case
    # =========================================================

    interior = (
        (x > 0.0)
        & (x < 1.0)
    )

    xi = x[interior]

    # ---------------------------------------------------------
    # (a-x)^2 ln|a-x|
    #
    # At x=a:
    #
    #     lim z→0 z² ln|z| = 0
    #
    # Therefore explicitly evaluate this limiting value as zero.
    # ---------------------------------------------------------

    delta = np.abs(
        a - xi
    )

    term1 = np.zeros_like(
        xi
    )

    nonzero = (
        delta > 0.0
    )

    term1[nonzero] = (
        0.5
        * delta[nonzero] ** 2
        * np.log(
            delta[nonzero]
        )
    )

    # ---------------------------------------------------------
    # Remaining terms from NACA equation (6)
    # ---------------------------------------------------------

    term2 = (
        -0.5
        * (1.0 - xi) ** 2
        * np.log(
            1.0 - xi
        )
    )

    term3 = (
        0.25
        * (1.0 - xi) ** 2
    )

    term4 = (
        -0.25
        * (a - xi) ** 2
    )

    bracket = (
        term1
        + term2
        + term3
        + term4
    )

    # ---------------------------------------------------------
    # NACA constants g and h
    # ---------------------------------------------------------

    g = -(
        a ** 2
        * (
            0.5 * np.log(a)
            - 0.25
        )
        + 0.25
    ) / (
        1.0 - a
    )

    h = (
        0.5
        * (1.0 - a) ** 2
        * np.log(
            1.0 - a
        )
        - 0.25
        * (1.0 - a) ** 2
    ) / (
        1.0 - a
    ) + g

    # ---------------------------------------------------------
    # Complete NACA equation (6)
    # ---------------------------------------------------------

    result[interior] = (
        bracket / (
            1.0 - a
        )
        - xi * np.log(xi)
        + g
        - h * xi
    )

    return result


def calculate_meanline(
    x_bar,
    a,
    cl,
):
    """
    Calculate NACA 6-series mean-line ordinate.

    Returns:

        yc/c
    """

    x_bar = _validate_inputs(
        x_bar,
        a,
        cl,
    )

    if cl == 0.0:
        return np.zeros_like(
            x_bar
        )

    factor = _meanline_factor(
        x_bar,
        a,
    )

    return (
        cl
        / (
            2.0
            * np.pi
            * (a + 1.0)
        )
        * factor
    )


def calculate_meanline_slope(
    x_bar,
    a,
    cl,
):
    """
    Calculate dyc/dx.

    The derivative is evaluated numerically from the
    same analytical mean-line function.
    """

    x_bar = _validate_inputs(
        x_bar,
        a,
        cl,
    )

    if x_bar.size < 2:
        raise ValueError(
            "At least two x coordinates are required"
        )

    y = calculate_meanline(
        x_bar,
        a,
        cl,
    )

    return np.gradient(
        y,
        x_bar,
    )