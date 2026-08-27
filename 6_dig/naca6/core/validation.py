from .parameters import NACA6Parameters

def validate_parameters(parameters: NACA6Parameters) -> None:
    if not 61<= parameters.designation.series <=69:
        raise ValueError("Invalid series Must be within: 61 to 69.")
    if parameters.designation.design_lift_coefficient < 0:
        raise ValueError("Design lift coefficient must be non-negative.")
    if parameters.designation.thickness_ratio <= 0:
        raise ValueError("Thickness ratio must be positive.")
    if parameters.chord <= 0:
        raise ValueError("Chord length must be positive.")
    if parameters.number_of_points < 100:
        raise ValueError("Number of points must be at least 100.")
