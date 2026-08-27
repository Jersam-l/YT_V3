from naca6.input.designation import parse_designation
from naca6.core.parameters import parse_parameters
from naca6.solvers.six_series_solver import generate_six_series

import numpy as np


# Reference lower-surface coordinates from the data book
x_ref = np.array(
    [
        20.0,
        40.0,
        60.0,
        80.0,
        100.0,
        120.0,
        140.0,
    ],
    dtype=float,
)

y_ref = np.array(
    [
        -0.243,
        -0.892,
        -1.950,
        -3.304,
        -3.197,
        -2.072,
        -0.149,
    ],
    dtype=float,
)


print(
    "SERIES   RMSE(mm)   "
    "YL20     YL40     YL60     YL80     "
    "YL100    YL120    YL140"
)

print("-" * 90)


for series in range(63, 68):

    designation = parse_designation(
        f"{series}(8)-015"
    )

    parameters = parse_parameters(
        "150.0",
        "2000",
        designation,
    )

    result = generate_six_series(
        parameters
    )

    y_lower = np.interp(
        x_ref,
        result.lower_x,
        result.lower_y,
    )

    error = y_lower - y_ref

    rmse = np.sqrt(
        np.mean(error ** 2)
    )

    print(
        f"{series}(8)   "
        f"{rmse:8.4f}   "
        f"{y_lower[0]:7.3f}  "
        f"{y_lower[1]:7.3f}  "
        f"{y_lower[2]:7.3f}  "
        f"{y_lower[3]:7.3f}  "
        f"{y_lower[4]:7.3f}  "
        f"{y_lower[5]:7.3f}  "
        f"{y_lower[6]:7.3f}"
    )