def validate_parameters(parameters):
    if parameters.chord <= 0.0:
        raise ValueError(
            "Chord must be positive."
        )

    if parameters.number_of_points < 2:
        raise ValueError(
            "Number of points must be at least 2."
        )

    if not (
        0.0 < parameters.meanline_a <= 1.0
    ):
        raise ValueError(
            "meanline_a must be greater than 0 "
            "and less than or equal to 1."
        )

    designation = parameters.designation

    if designation.series < 60:
        raise ValueError(
            "Unsupported NACA 6-series designation."
        )

    if not (
        0.0 < designation.pressure_location < 1.0
    ):
        raise ValueError(
            "Pressure location must lie between 0 and 1."
        )

    if designation.design_lift_coefficient < 0.0:
        raise ValueError(
            "Design lift coefficient cannot be negative."
        )

    if designation.thickness_ratio <= 0.0:
        raise ValueError(
            "Thickness ratio must be positive."
        )