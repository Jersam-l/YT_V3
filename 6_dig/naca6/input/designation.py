from dataclasses import dataclass


@dataclass
class NACA6Designation:
    series: int
    pressure_location: float
    design_lift_coefficient: float
    thickness_ratio: float


def parse_designation(text: str) -> NACA6Designation:
    """
    Parse a NACA 6-series designation.

    Project designation format:

        63(2)-215
        63(8)-015
        66(2)-015

    Fields:

        63(2)-215
        ││ │  │││
        ││ │  │└┴── thickness percentage
        ││ │  └──── design-lift field
        ││ └─────── design lift coefficient
        │└───────── pressure location
        └────────── 6-series

    Examples
    --------
    63(2)-215

        series                  = 63
        pressure_location       = 0.3
        design_lift_coefficient = 0.2
        thickness_ratio         = 0.15

    63(8)-015

        series                  = 63
        pressure_location       = 0.3
        design_lift_coefficient = 0.8
        thickness_ratio         = 0.15

    66(2)-015

        series                  = 66
        pressure_location       = 0.6
        design_lift_coefficient = 0.2
        thickness_ratio         = 0.15
    """

    # ---------------------------------------------------------
    # 1. Validate input
    # ---------------------------------------------------------

    if not isinstance(text, str):
        raise TypeError(
            "designation must be a string"
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "designation cannot be empty"
        )

    # ---------------------------------------------------------
    # 2. Remove optional NACA prefix
    # ---------------------------------------------------------

    if text.upper().startswith("NACA"):
        text = text[4:].strip()

    # ---------------------------------------------------------
    # 3. Remove whitespace
    # ---------------------------------------------------------

    text = "".join(
        text.split()
    )

    # ---------------------------------------------------------
    # 4. Validate basic structure
    # ---------------------------------------------------------

    if "(" not in text:
        raise ValueError(
            "6-series designation must contain '('"
        )

    if ")" not in text:
        raise ValueError(
            "6-series designation must contain ')'"
        )

    if ")-" not in text:
        raise ValueError(
            "6-series designation must contain ')-'"
        )

    # ---------------------------------------------------------
    # 5. Split designation
    #
    #     66(2)-015
    #
    # series_part = "66"
    # cl_part     = "2"
    # suffix      = "015"
    # ---------------------------------------------------------

    series_part, remainder = text.split(
        "(",
        1,
    )

    cl_part, thickness_part = remainder.split(
        ")-",
        1,
    )

    # ---------------------------------------------------------
    # 6. Validate series
    # ---------------------------------------------------------

    if not series_part.isdigit():
        raise ValueError(
            "series must contain digits"
        )

    if len(series_part) != 2:
        raise ValueError(
            "series must contain exactly two digits"
        )

    series = int(
        series_part
    )

    # ---------------------------------------------------------
    # 7. Validate parenthesized design-lift field
    # ---------------------------------------------------------

    if not cl_part.isdigit():
        raise ValueError(
            "design lift coefficient field "
            "must contain digits"
        )

    if len(cl_part) != 1:
        raise ValueError(
            "design lift coefficient field "
            "must contain exactly one digit"
        )

    # ---------------------------------------------------------
    # 8. Validate thickness field
    # ---------------------------------------------------------

    if not thickness_part.isdigit():
        raise ValueError(
            "thickness field must contain digits"
        )

    if len(thickness_part) != 3:
        raise ValueError(
            "thickness field must contain exactly "
            "three digits"
        )

    # ---------------------------------------------------------
    # 9. Pressure location
    #
    # Second digit of the series.
    #
    # 63 -> 0.3
    # 64 -> 0.4
    # 65 -> 0.5
    # 66 -> 0.6
    # 67 -> 0.7
    # ---------------------------------------------------------

    pressure_location = (
        int(series_part[1])
        / 10.0
    )

    if not (
        0.0 < pressure_location < 1.0
    ):
        raise ValueError(
            "pressure location must lie "
            "between 0 and 1"
        )

    # ---------------------------------------------------------
    # 10. Design lift coefficient
    #
    # IMPORTANT:
    #
    # In the current project/test convention, the digit
    # inside the parentheses defines the design CL.
    #
    # 66(2)-015 -> CL = 0.2
    # 63(8)-015 -> CL = 0.8
    #
    # ---------------------------------------------------------

    design_lift_coefficient = (
        int(cl_part)
        / 10.0
    )

    if not (
        0.0 <= design_lift_coefficient <= 1.0
    ):
        raise ValueError(
            "design lift coefficient must lie "
            "between 0 and 1"
        )

    # ---------------------------------------------------------
    # 11. Thickness ratio
    #
    # The suffix after the dash is interpreted as follows:
    #
    #   015  ->  t/c = 15%   (leading zero)
    #   215  ->  t/c = 15%   (first digit echoes CL)
    #   012  ->  t/c = 12%
    #   218  ->  t/c = 18%
    #
    # We always take the last two digits as the thickness
    # percentage.
    # ---------------------------------------------------------

    thickness_ratio = (
        int(thickness_part[-2:])
        / 100.0
    )

    if not (
        0.0 < thickness_ratio < 1.0
    ):
        raise ValueError(
            "thickness ratio must lie "
            "between 0 and 1"
        )

    # ---------------------------------------------------------
    # 12. Return
    # ---------------------------------------------------------

    return NACA6Designation(
        series=series,
        pressure_location=pressure_location,
        design_lift_coefficient=design_lift_coefficient,
        thickness_ratio=thickness_ratio,
    )