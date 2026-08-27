from dataclasses import dataclass
import numpy as np

@dataclass
class NACA6Result:
    boundary_x: np.ndarray
    boundary_y: np.ndarray

    upper_x: np.ndarray
    upper_y: np.ndarray

    lower_x: np.ndarray
    lower_y: np.ndarray

    mean_x: np.ndarray
    mean_y: np.ndarray
