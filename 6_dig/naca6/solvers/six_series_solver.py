import numpy as np

from ..core.validation import validate_parameters
from ..core.result import NACA6Result

from ..equations.epsilon_psi import (
    calculate_epsilon,
    calculate_psi,
)

from ..equations.conformal_mapping import (
    conformal_map,
)

from ..equations.meanline import (
    calculate_meanline,
    calculate_meanline_slope,
)


def generate_six_series(parameters):
    """
    Generate a NACA 6-series airfoil.

    Geometry is generated from the NACA 6-series mathematical
    formulation:

        1. Validate parameters
        2. Generate a sufficiently resolved phi grid
        3. Calculate epsilon and psi
        4. Apply the conformal transformation
        5. Obtain the thickness distribution
        6. Calculate the NACA 6-series mean line
        7. Calculate the mean-line slope
        8. Offset the thickness normal to the mean line
        9. Scale to the physical chord
        10. Interpolate onto the requested x grid
        11. Assemble the complete boundary
    """

    # =========================================================
    # 1. Validate parameters
    # =========================================================

    validate_parameters(
        parameters
    )

    n = parameters.number_of_points

    if n < 201:
        n = 201

    # =========================================================
    # 2. Angular coordinate
    #
    # The conformal geometry is generated at a resolution
    # related to the requested output resolution.
    #
    # This avoids generating only 201 geometry points when
    # the user requests thousands of output points.
    # =========================================================

    phi_points = max(
        201,
        2 * n + 1,
    )

    phi = np.linspace(
        0.0,
        np.pi,
        phi_points,
    )

    # =========================================================
    # 3. Calculate NACA epsilon and psi
    # =========================================================

    epsilon = calculate_epsilon(
        phi,
        parameters,
    )

    psi = calculate_psi(
        phi,
        parameters,
    )

    # =========================================================
    # 4. Conformal mapping
    # =========================================================

    x_thickness, y_thickness = conformal_map(
        phi,
        psi,
        epsilon,
    )

    x_bar = np.asarray(
        x_thickness,
        dtype=float,
    )

    y_thickness = np.asarray(
        y_thickness,
        dtype=float,
    )

    # =========================================================
    # 5. Normalized thickness distribution
    # =========================================================

    x_bar = np.clip(
        x_bar,
        0.0,
        1.0,
    )

    thickness = np.abs(
        y_thickness
    )

    # =========================================================
    # 6. NACA 6-series mean line
    # =========================================================

    a = parameters.meanline_a

    cl = parameters.designation.design_lift_coefficient

    mean_y = calculate_meanline(
        x_bar,
        a,
        cl,
    )

    # =========================================================
    # 7. Mean-line slope
    # =========================================================

    mean_slope = calculate_meanline_slope(
        x_bar,
        a,
        cl,
    )

    # =========================================================
    # 8. Mean-line angle
    # =========================================================

    theta = np.arctan(
        mean_slope
    )

    sin_theta = np.sin(
        theta
    )

    cos_theta = np.cos(
        theta
    )

    # =========================================================
    # 9. Normal thickness offset
    #
    # Upper:
    #
    #     xu = x - yt sin(theta)
    #     yu = yc + yt cos(theta)
    #
    # Lower:
    #
    #     xl = x + yt sin(theta)
    #     yl = yc - yt cos(theta)
    #
    # This is a normal offset from the mean line.
    # =========================================================

    upper_x = (
        x_bar
        - thickness * sin_theta
    )

    upper_y = (
        mean_y
        + thickness * cos_theta
    )

    lower_x = (
        x_bar
        + thickness * sin_theta
    )

    lower_y = (
        mean_y
        - thickness * cos_theta
    )

    # =========================================================
    # 10. Convert to physical coordinates
    # =========================================================

    chord = parameters.chord

    upper_x = upper_x * chord
    upper_y = upper_y * chord

    lower_x = lower_x * chord
    lower_y = lower_y * chord

    mean_x = x_bar * chord
    mean_y = mean_y * chord

    # =========================================================
    # 11. Requested output x-grid
    #
    # Cosine spacing concentrates points near the leading
    # and trailing edges where curvature is highest.
    # =========================================================

    beta = np.linspace(
        0.0,
        np.pi,
        n,
    )

    target_x = (
        0.5
        * chord
        * (1.0 - np.cos(beta))
    )

    # =========================================================
    # 11b. Clip raw surface x to valid chord range
    #
    # The normal offset can push upper_x slightly negative
    # near the leading edge. Clip to prevent fold-back from
    # corrupting the interpolation.
    # =========================================================

    upper_x = np.clip(upper_x, 0.0, chord)
    lower_x = np.clip(lower_x, 0.0, chord)

    # =========================================================
    # 12. Prepare upper surface for interpolation
    # =========================================================

    upper_order = np.argsort(
        upper_x
    )

    upper_x_sorted = upper_x[
        upper_order
    ]

    upper_y_sorted = upper_y[
        upper_order
    ]

    upper_x_unique, upper_indices = np.unique(
        upper_x_sorted,
        return_index=True,
    )

    upper_y_unique = upper_y_sorted[
        upper_indices
    ]

    # =========================================================
    # 13. Prepare lower surface for interpolation
    # =========================================================

    lower_order = np.argsort(
        lower_x
    )

    lower_x_sorted = lower_x[
        lower_order
    ]

    lower_y_sorted = lower_y[
        lower_order
    ]

    lower_x_unique, lower_indices = np.unique(
        lower_x_sorted,
        return_index=True,
    )

    lower_y_unique = lower_y_sorted[
        lower_indices
    ]

    # =========================================================
    # 14. Interpolate surfaces onto requested x-grid
    # =========================================================

    upper_x_final = target_x.copy()

    lower_x_final = target_x.copy()

    upper_y_final = np.interp(
        target_x,
        upper_x_unique,
        upper_y_unique,
    )

    lower_y_final = np.interp(
        target_x,
        lower_x_unique,
        lower_y_unique,
    )

    # =========================================================
    # 15. Mean line on requested grid
    # =========================================================

    x_bar_final = (
        target_x / chord
    )

    mean_y_final = calculate_meanline(
        x_bar_final,
        a,
        cl,
    ) * chord

    mean_x_final = target_x.copy()

    # =========================================================
    # 16. Assemble complete boundary
    #
    # Upper surface:
    #
    #     TE -> LE
    #
    # Lower surface:
    #
    #     LE -> TE
    #
    # The leading-edge point is shared, so it is not duplicated.
    # =========================================================

    boundary_x = np.concatenate(
        [
            upper_x_final[::-1],
            lower_x_final[1:],
        ]
    )

    boundary_y = np.concatenate(
        [
            upper_y_final[::-1],
            lower_y_final[1:],
        ]
    )

    # =========================================================
    # 17. Return result
    # =========================================================

    return NACA6Result(
        boundary_x=boundary_x,
        boundary_y=boundary_y,

        upper_x=upper_x_final,
        upper_y=upper_y_final,

        lower_x=lower_x_final,
        lower_y=lower_y_final,

        mean_x=mean_x_final,
        mean_y=mean_y_final,
    )