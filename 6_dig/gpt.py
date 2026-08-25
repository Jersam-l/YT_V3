import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# NACA 6-SERIES AIRFOIL
# Example:
#       66(2)-015
#
# 6  -> 6-series family
# 6  -> position parameter
# (2)-> design lift coefficient
# 015-> thickness/chord = 0.15
# ============================================================


naca6 = input(
    "Enter the NACA 6-series designation (e.g. 66(2)-015): "
).strip()


# ------------------------------------------------------------
# Read designation
# ------------------------------------------------------------

try:

    series_part, remainder = naca6.split("(", 1)
    bracket_part, thickness_part = remainder.split(")-", 1)

    series = int(series_part)
    bracket_value = int(bracket_part)

    if len(thickness_part) != 3:
        raise ValueError

    if not thickness_part.isdigit():
        raise ValueError

    t_dc = int(thickness_part) / 100.0

except ValueError:

    print(
        "Please enter a valid designation, "
        "for example 66(2)-015"
    )

    exit()


# ------------------------------------------------------------
# Validate designation
# ------------------------------------------------------------

if series < 60 or series > 69:

    print("This program is for NACA 6-series airfoils.")

    exit()


# ------------------------------------------------------------
# Parameters contained in designation
# ------------------------------------------------------------

series_family = series // 10

pressure_location = (series % 10) / 10.0

cli = bracket_value / 10.0


# ------------------------------------------------------------
# User inputs
# ------------------------------------------------------------

chord = float(
    input("Enter the required chord length: ")
)

n = int(
    input(
        "Enter the number of points needed "
        "for the coordinates (whole number): "
    )
)


if chord <= 0:

    print("Chord must be greater than zero.")

    exit()


if n < 2:

    print("Number of points must be at least 2.")

    exit()


# ============================================================
# NORMALIZED X COORDINATE
# ============================================================

x_bar = np.linspace(0.0, 1.0, n)

x = chord * x_bar


# ============================================================
# ARRAYS
# ============================================================

ym = np.zeros(n)

dyc_dx = np.zeros(n)

yt = np.zeros(n)

xu = np.zeros(n)
yu = np.zeros(n)

xl = np.zeros(n)
yl = np.zeros(n)


# ============================================================
# A-SERIES MEAN LINE
#
# IMPORTANT:
#
# The present closed-form equation uses the parameter "a".
# For the standard a=1 limiting case, the original expression
# contains 1/(1-a), so we use its limiting form rather than
# dividing by zero.
#
# This is NOT the same thing as simply saying:
#
#       a = pressure_location
#
# ============================================================

a = 1.0


# ------------------------------------------------------------
# Standard a = 1 limiting mean-line calculation
#
# The limit of the a-series expression gives the standard
# 6-series mean-line form.
# ------------------------------------------------------------

# For a = 1 the mean-line expression reduces to:

for i, xi in enumerate(x_bar):

    if xi == 0.0:

        # limiting value at the leading edge
        ym_bar = 0.0
        slope = 0.0

    elif xi == 1.0:

        # trailing-edge condition
        ym_bar = 0.0
        slope = 0.0

    else:

        # ----------------------------------------------------
        # Standard a=1 loading form
        # ----------------------------------------------------

        term1 = (
            (1.0 - xi)**2
            * np.log(1.0 - xi)
        )

        term2 = (
            xi**2
            * np.log(xi)
        )

        ym_bar = (
            cli
            / (2.0 * np.pi)
            * (
                term1
                + term2
                + xi
                - xi**2
            )
        )

        # Numerical derivative of the normalized mean line
        # is obtained analytically from the expression above.

        dterm1 = (
            -2.0 * (1.0 - xi)
            * np.log(1.0 - xi)
            - (1.0 - xi)
        )

        dterm2 = (
            2.0 * xi * np.log(xi)
            + xi
        )

        slope = (
            cli
            / (2.0 * np.pi)
            * (
                dterm1
                + dterm2
                + 1.0
                - 2.0 * xi
            )
        )

    ym[i] = chord * ym_bar

    dyc_dx[i] = slope


# ============================================================
# CAMBER-LINE ANGLE
# ============================================================

theta = np.arctan(dyc_dx)


# ============================================================
# THICKNESS DISTRIBUTION
#
# The following analytical thickness law is the same type of
# closed polynomial thickness law used in the NACA 4-digit
# family.
#
# IMPORTANT:
#
# This is NOT the exact historical NACA 6-series thickness
# construction.
#
# A mathematically exact universal 6-series generator requires
# the inverse conformal-mapping construction used to generate
# the original 6-series thickness distributions.
# ============================================================

yt_bar = (
    5.0 * t_dc
    * (
        0.2969 * np.sqrt(x_bar)
        - 0.1260 * x_bar
        - 0.3516 * x_bar**2
        + 0.2843 * x_bar**3
        - 0.1015 * x_bar**4
    )
)

yt = chord * yt_bar


# ============================================================
# UPPER AND LOWER SURFACES
#
# Thickness is placed NORMAL to the mean line.
#
# This is the part that was missing from your current code.
# ============================================================

xu = x - yt * np.sin(theta)
yu = ym + yt * np.cos(theta)

xl = x + yt * np.sin(theta)
yl = ym - yt * np.cos(theta)


# ============================================================
# COMPLETE AIRFOIL COORDINATE ORDER
#
# TE -> upper surface -> LE -> lower surface -> TE
# ============================================================

airfoil_x = np.concatenate(
    (
        xu[::-1],
        xl[1:]
    )
)

airfoil_y = np.concatenate(
    (
        yu[::-1],
        yl[1:]
    )
)


# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(2.5, 2.5))

plt.plot(
    airfoil_x,
    airfoil_y,
    label="Airfoil"
)

plt.plot(
    x,
    ym,
    "--",
    label="Mean line"
)

plt.axis("equal")

plt.grid(True)

plt.xlabel("x")

plt.ylabel("y")

plt.legend()

plt.show()


# ============================================================
# WRITE COORDINATES
# ============================================================

filename = f"NACA{series}({bracket_value})-{thickness_part}.dat"


with open(filename, "w") as file:

    for xi, yi in zip(airfoil_x, airfoil_y):

        file.write(
            f"{xi:.8f} {yi:.8f}\n"
        )


print()
print("Coordinates generated successfully.")
print(f"File: {filename}")