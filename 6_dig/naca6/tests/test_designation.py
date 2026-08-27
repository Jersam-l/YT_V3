from naca6.input.designation import (
    NACA6Designation,
    parse_designation,
)


def test_parse_standard_designation():

    result = parse_designation(
        "66(2)-015"
    )

    assert isinstance(
        result,
        NACA6Designation
    )

    assert result.series == 66
    assert result.pressure_location == 0.6
    assert result.design_lift_coefficient == 0.2
    assert result.thickness_ratio == 0.15


def test_parse_designation_with_spaces():

    result = parse_designation(
        " 66(2)-015 "
    )

    assert result.series == 66
    assert result.pressure_location == 0.6
    assert result.design_lift_coefficient == 0.2
    assert result.thickness_ratio == 0.15


def test_parse_zero_lift_designation():

    result = parse_designation(
        "65(0)-012"
    )

    assert result.series == 65
    assert result.pressure_location == 0.5
    assert result.design_lift_coefficient == 0.0
    assert result.thickness_ratio == 0.12