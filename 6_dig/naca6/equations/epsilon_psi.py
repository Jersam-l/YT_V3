from pathlib import Path
import re

import numpy as np


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

EPSPSI_FILE = DATA_DIR / "epspsi.f90"
NACAX_FILE = DATA_DIR / "nacax.f90"


def _read_array(name: str, filename: Path, size: int) -> np.ndarray:
    text = filename.read_text()

    pattern = rf"{name}\s*=\s*\(/\s*(.*?)\s*/\)"

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match is None:
        raise ValueError(
            f"Could not find {name} in {filename}"
        )

    numbers = re.findall(
        r"[-+]?(?:\d+\.\d*|\.\d+|\d+)"
        r"(?:[EeDd][-+]?\d+)?",
        match.group(1),
    )

    values = np.asarray(
        [
            float(value.replace("D", "E").replace("d", "e"))
            for value in numbers
        ],
        dtype=float,
    )

    if len(values) != size:
        raise ValueError(
            f"{name}: expected {size} values, "
            f"found {len(values)}"
        )

    return values


def _family_from_series(series: int) -> int:

    if not 63 <= series <= 67:
        raise ValueError(
            "The supplied NACA reference data supports "
            "6-series 63 through 67."
        )

    return series - 62


def _load_eps_psi(family: int):

    phi = np.linspace(
        0.0,
        np.pi,
        201,
    )

    epsilon = _read_array(
        f"EPS{family}",
        EPSPSI_FILE,
        201,
    )

    psi = _read_array(
        f"PSI{family}",
        EPSPSI_FILE,
        201,
    )

    return phi, epsilon, psi


def _scale_factor(family: int, thickness_ratio: float):

    if not 1 <= family <= 8:
        raise ValueError("Invalid NACA family.")

    if thickness_ratio <= 0.0:
        raise ValueError(
            "Thickness ratio must be positive."
        )

    text = NACAX_FILE.read_text()

    start = re.search(
        r"\bCOEFF\b",
        text,
        flags=re.IGNORECASE,
    )

    if start is None:
        raise ValueError(
            "COEFF was not found in nacax.f90."
        )

    block = text[start.end():]

    # The coefficient block ends at the first
    # closing parenthesis following the DATA values.
    end = block.find("/)")

    if end == -1:
        raise ValueError(
            "Could not find the end of the COEFF data."
        )

    block = block[:end]

    numbers = re.findall(
        r"[-+]?(?:\d+\.\d*|\.\d+|\d+)"
        r"(?:[EeDd][-+]?\d+)?",
        block,
    )

    coefficients = np.asarray(
        [
            float(
                value.replace("D", "E")
                     .replace("d", "e")
            )
            for value in numbers
        ],
        dtype=float,
    )

    if len(coefficients) < 40:
        raise ValueError(
            f"Expected at least 40 coefficients, "
            f"found {len(coefficients)}."
        )

    coefficients = coefficients[:40]

    # Fortran:
    #
    # DIMENSION(5,8)
    # RESHAPE(...)
    #
    # Therefore preserve column-major ordering.
    coefficients = coefficients.reshape(
        (5, 8),
        order="F",
    )

    c = coefficients[:, family - 1]

    t = thickness_ratio

    # Horner's method:
    #
    # c0 + c1*t + c2*t² + c3*t³ + c4*t⁴
    scale = c[4]

    for i in range(3, -1, -1):
        scale = scale * t + c[i]

    return scale

def calculate_epsilon(phi, parameters):

    phi = np.asarray(phi, dtype=float)

    if phi.ndim != 1:
        raise ValueError(
            "phi must be one-dimensional."
        )

    if np.any(phi < 0.0) or np.any(phi > np.pi):
        raise ValueError(
            "phi must be between 0 and pi."
        )

    series = parameters.designation.series

    family = _family_from_series(series)

    phi_ref, epsilon_ref, _ = _load_eps_psi(
        family
    )

    scale = _scale_factor(
        family,
        parameters.designation.thickness_ratio,
    )

    epsilon = np.interp(
        phi,
        phi_ref,
        epsilon_ref,
    )

    return scale * epsilon


def calculate_psi(phi, parameters):

    phi = np.asarray(phi, dtype=float)

    if phi.ndim != 1:
        raise ValueError(
            "phi must be one-dimensional."
        )

    if np.any(phi < 0.0) or np.any(phi > np.pi):
        raise ValueError(
            "phi must be between 0 and pi."
        )

    series = parameters.designation.series

    family = _family_from_series(series)

    phi_ref, _, psi_ref = _load_eps_psi(
        family
    )

    scale = _scale_factor(
        family,
        parameters.designation.thickness_ratio,
    )

    psi = np.interp(
        phi,
        phi_ref,
        psi_ref,
    )

    return scale * psi