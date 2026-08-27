from dataclasses import dataclass

from .validation import validate_parameters


@dataclass
class NACA6Parameters:
    chord: float
    number_of_points: int
    designation: object
    meanline_a: float


def parse_parameters(
    chord,
    number_of_points,
    designation,
    meanline_a=None,
):
    if meanline_a is None:
        meanline_a = designation.pressure_location

    parameters = NACA6Parameters(
        chord=float(chord),
        number_of_points=int(number_of_points),
        designation=designation,
        meanline_a=float(meanline_a),
    )

    validate_parameters(parameters)

    return parameters