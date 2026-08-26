from dataclasses import dataclass
from ..input.designation import NACA6Designation

@dataclass
class NACA6Parameters:
    designation=NACA6Designation
    chord
    number_of_points
    