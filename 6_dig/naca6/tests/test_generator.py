import numpy as np

from naca6.input.designation import parse_designation
from naca6.core.parameters import parse_parameters
from naca6.core.result import NACA6Result
from naca6.solvers.six_series_solver import generate_six_series


def make_parameters(
    designation="66(2)-015",
    chord="1.0",
    points="201",
):
    d = parse_designation(designation)

    return parse_parameters(
        chord,
        points,
        d,
    )


def test_generator_returns_naca6_result():
    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert isinstance(
        result,
        NACA6Result,
    )


def test_generator_returns_correct_boundary_size():
    parameters = make_parameters(
        points="201"
    )

    result = generate_six_series(
        parameters
    )

    # 201 upper + 200 lower
    assert len(result.boundary_x) == 401
    assert len(result.boundary_y) == 401


def test_generator_surface_sizes_match():
    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert len(result.upper_x) == 201
    assert len(result.upper_y) == 201

    assert len(result.lower_x) == 201
    assert len(result.lower_y) == 201


def test_generator_meanline_size_matches():
    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert len(result.mean_x) == 201
    assert len(result.mean_y) == 201


def test_generator_coordinates_are_finite():
    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert np.all(
        np.isfinite(result.boundary_x)
    )

    assert np.all(
        np.isfinite(result.boundary_y)
    )


def test_generator_chord_range():
    parameters = make_parameters(
        chord="1.0"
    )

    result = generate_six_series(
        parameters
    )

    assert np.isclose(
        result.boundary_x.min(),
        0.0,
    )

    assert np.isclose(
        result.boundary_x.max(),
        1.0,
    )


def test_generator_scales_with_chord():
    p1 = make_parameters(
        chord="1.0"
    )

    p2 = make_parameters(
        chord="2.0"
    )

    r1 = generate_six_series(p1)
    r2 = generate_six_series(p2)

    assert np.isclose(
        r2.boundary_x.max(),
        2.0,
    )

    assert np.isclose(
        r2.boundary_y.max(),
        2.0 * r1.boundary_y.max(),
    )


def test_generator_zero_lift_has_zero_meanline():
    parameters = make_parameters(
        designation="66(0)-015"
    )

    result = generate_six_series(
        parameters
    )

    assert np.allclose(
        result.mean_y,
        0.0,
    )