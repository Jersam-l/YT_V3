from dataclasses import dataclass

@dataclass
class NACA6Designation:
    series:int
    design_lift_coefficient:float
    thickness_ratio:float

def parse_designation(text: str) -> NACA6Designation:
    text = text.strip()
    series_part, remainder = (text.split("(",1))
    bracket_part , thickness_part = (remainder.split(")-",1))
    series = int(series_part)
    design_lift_coefficient = (float(bracket_part))/10
    thickness_ratio = (float(thickness_part)) / 100
    return NACA6Designation(series=series, design_lift_coefficient=design_lift_coefficient, thickness_ratio=thickness_ratio)
