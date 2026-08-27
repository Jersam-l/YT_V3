import numpy as np

from naca6.input.designation import parse_designation
from naca6.core.parameters import parse_parameters

from naca6.equations.epsilon_psi import (
    calculate_epsilon,
    calculate_psi,
)

from naca6.equations.conformal_mapping import conformal_map

from naca6.equations.meanline import (
    calculate_meanline,
    calculate_meanline_slope,
)


# ============================================================
# Parameters
# ============================================================

designation = parse_designation(
    "63(8)-015"
)

parameters = parse_parameters(
    "150.0",
    "2000",
    designation,
)


# ============================================================
# NACA parameter information
# ============================================================

print()
print("DESIGNATION")
print(designation)

print()
print("PARAMETERS")
print(parameters)

print()
print("pressure_location =", designation.pressure_location)
print("meanline_a        =", parameters.meanline_a)
print("CL                =", designation.design_lift_coefficient)
print("t/c               =", designation.thickness_ratio)


# ============================================================
# Generate a dense parametric grid
# ============================================================

phi = np.linspace(
    0.0,
    np.pi,
    4001,
)


# ============================================================
# Epsilon / psi
# ============================================================

epsilon = calculate_epsilon(
    phi,
    parameters,
)

psi = calculate_psi(
    phi,
    parameters,
)


# ============================================================
# Conformal mapping
# ============================================================

x_bar, y_thickness = conformal_map(
    phi,
    psi,
    epsilon,
)

x_bar = np.asarray(
    x_bar,
    dtype=float,
)

y_thickness = np.asarray(
    y_thickness,
    dtype=float,
)

x_bar = np.clip(
    x_bar,
    0.0,
    1.0,
)

thickness = np.abs(
    y_thickness
)


# ============================================================
# Mean line
# ============================================================

a = parameters.meanline_a

cl = designation.design_lift_coefficient

mean_y = calculate_meanline(
    x_bar,
    a,
    cl,
)

mean_slope = calculate_meanline_slope(
    x_bar,
    a,
    cl,
)


# ============================================================
# Normal direction
# ============================================================

theta = np.arctan(
    mean_slope
)

sin_theta = np.sin(
    theta
)

cos_theta = np.cos(
    theta
)


# ============================================================
# Parametric upper/lower surfaces
# ============================================================

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


# ============================================================
# Physical coordinates
# ============================================================

chord = parameters.chord

upper_x *= chord
upper_y *= chord

lower_x *= chord
lower_y *= chord

mean_x = x_bar * chord
mean_y *= chord


# ============================================================
# Print leading-edge parametric coordinates
# ============================================================

print()
print(
    "PARAMETRIC LEADING EDGE"
)

print(
    "phi(deg)    xbar       upper_x    upper_y    lower_x    lower_y"
)

for i in range(0, 80, 5):

    print(
        f"{np.degrees(phi[i]):8.3f} "
        f"{x_bar[i]:10.6f} "
        f"{upper_x[i]:10.6f} "
        f"{upper_y[i]:10.6f} "
        f"{lower_x[i]:10.6f} "
        f"{lower_y[i]:10.6f}"
    )


# ============================================================
# Print requested physical x positions
# ============================================================

target_x = np.array(
    [
        0.0,
        0.75,
        1.125,
        1.875,
        3.75,
        7.5,
        11.25,
        15.0,
        20.0,
        22.5,
        30.0,
        40.0,
    ],
    dtype=float,
)


# ============================================================
# Sort parametric surfaces
# ============================================================

upper_order = np.argsort(
    upper_x
)

lower_order = np.argsort(
    lower_x
)

upper_x_sorted = upper_x[
    upper_order
]

upper_y_sorted = upper_y[
    upper_order
]

lower_x_sorted = lower_x[
    lower_order
]

lower_y_sorted = lower_y[
    lower_order
]


# ============================================================
# Remove duplicate x coordinates
# ============================================================

upper_x_unique, upper_indices = np.unique(
    upper_x_sorted,
    return_index=True,
)

upper_y_unique = upper_y_sorted[
    upper_indices
]

lower_x_unique, lower_indices = np.unique(
    lower_x_sorted,
    return_index=True,
)

lower_y_unique = lower_y_sorted[
    lower_indices
]


# ============================================================
# Interpolate
# ============================================================

upper_interpolated = np.interp(
    target_x,
    upper_x_unique,
    upper_y_unique,
)

lower_interpolated = np.interp(
    target_x,
    lower_x_unique,
    lower_y_unique,
)


# ============================================================
# Mean line
# ============================================================

mean_interpolated = np.interp(
    target_x,
    mean_x,
    mean_y,
)


# ============================================================
# Print
# ============================================================

print()
print(
    "FINAL INTERPOLATED GEOMETRY"
)

print(
    "X(mm)       UPPER        LOWER        MEAN"
)

for x, u, l, m in zip(
    target_x,
    upper_interpolated,
    lower_interpolated,
    mean_interpolated,
):

    print(
        f"{x:8.3f} "
        f"{u:12.6f} "
        f"{l:12.6f} "
        f"{m:12.6f}"
    )