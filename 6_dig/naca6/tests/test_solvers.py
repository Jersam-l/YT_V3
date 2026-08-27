import numpy as np
import pytest

from naca6.input.designation import parse_designation
from naca6.core.parameters import parse_parameters

from naca6.solvers.six_series_solver import (
    generate_six_series,
)


def make_parameters(
    designation="66(2)-015",
    chord="1.0",
    points="201",
):

    d = parse_designation(
        designation
    )

    return parse_parameters(
        chord,
        points,
        d,
    )


def test_six_series_solver_returns_result():

    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert result is not None


def test_six_series_solver_returns_finite_boundary():

    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert np.all(
        np.isfinite(
            result.boundary_x
        )
    )

    assert np.all(
        np.isfinite(
            result.boundary_y
        )
    )


def test_six_series_solver_returns_finite_surfaces():

    parameters = make_parameters()

    result = generate_six_series(
        parameters
    )

    assert np.all(
        np.isfinite(
            result.upper_x
        )
    )

    assert np.all(
        np.isfinite(
            result.upper_y
        )
    )

    assert np.all(
        np.isfinite(
            result.lower_x
        )
    )

    assert np.all(
        np.isfinite(
            result.lower_y
        )
    )


def test_six_series_solver_changes_with_series():

    p63 = make_parameters(
        "63(2)-015"
    )

    p66 = make_parameters(
        "66(2)-015"
    )

    r63 = generate_six_series(
        p63
    )

    r66 = generate_six_series(
        p66
    )

    assert not np.allclose(
        r63.boundary_y,
        r66.boundary_y,
    )


def test_six_series_solver_changes_with_thickness():

    p12 = make_parameters(
        "66(2)-012"
    )

    p18 = make_parameters(
        "66(2)-018"
    )

    r12 = generate_six_series(
        p12
    )

    r18 = generate_six_series(
        p18
    )

    assert not np.allclose(
        r12.boundary_y,
        r18.boundary_y,
    )


def test_six_series_solver_scales_with_chord():

    p1 = make_parameters(
        chord="1.0"
    )

    p2 = make_parameters(
        chord="2.0"
    )

    r1 = generate_six_series(
        p1
    )

    r2 = generate_six_series(
        p2
    )

    assert np.allclose(
        r2.boundary_x,
        2.0 * r1.boundary_x,
    )

    assert np.allclose(
        r2.boundary_y,
        2.0 * r1.boundary_y,
    )


def test_six_series_solver_rejects_invalid_parameters():

    parameters = make_parameters(
        "68(2)-015"
    )

    with pytest.raises(ValueError):

        generate_six_series(
            parameters
        )
        