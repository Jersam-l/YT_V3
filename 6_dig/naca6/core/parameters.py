from dataclasses import dataclass
from ..input.designation import NACA6Designation

@dataclass
class NACA6Parameters:
    designation: NACA6Designation
    chord: float
    number_of_points: int

def parse_parameters( text1:str, text2:str, designation: NACA6Designation) -> NACA6Parameters:
    text1= text1.strip()
    text2= text2.strip()
    chord = float(text1)
    number_of_points = int(text2)
    return NACA6Parameters(designation=designation, chord=chord, number_of_points=number_of_points)