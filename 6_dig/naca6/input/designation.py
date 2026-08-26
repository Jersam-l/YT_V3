from dataclasses import dataclass

@dataclass
class NACA6Designation:
    series:int
    design_lift_coefficient:float
    thickness_ratio:float