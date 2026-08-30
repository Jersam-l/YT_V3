# NACA 6-Series Airfoil Generator

A robust Python implementation for generating accurate NACA 6-series airfoil coordinates based on the conformal mapping equations.

## Project Structure

```text
YT-ASSERTS/V3
│   README.md
│   dev_plot.py
│
└── 6_dig
    └── naca6
        ├── core
        │   ├── parameters.py
        │   ├── result.py
        │   └── validation.py
        ├── equations
        │   ├── conformal_mapping.py
        │   ├── meanline.py
        │   ├── thickness.py
        │   └── velocity_distribution.py
        ├── input
        │   └── designation.py
        ├── numerics
        │   ├── fourier.py
        │   ├── integration.py
        │   ├── iteration.py
        │   └── quadrature.py
        ├── solvers
        │   ├── conformal_solver.py
        │   ├── meanline_solver.py
        │   ├── six_series_solver.py
        │   └── thickness_solver.py
        └── tests
```

---

## Known Issues and Fixes

During the development and testing of this generator against high-accuracy reference coordinates, two significant bugs were identified and fixed:

### 1. The Leading-Edge Distortion (The "Vertical Kink")
**The Issue:** When generating the airfoil coordinates, a sharp vertical straight line (a "kink") would sometimes appear right at the leading edge (`x=0`), cutting off the smooth nose curve.
**Why it behaved this way:** The generator was using a uniform linear spacing (`np.linspace`) to calculate the x-coordinates across the chord, and applying a `np.unique` filter. Because conformal mapping can cause parametric `x` values to fold back slightly negative at the very front of the leading edge, the interpolator got confused and dropped the curve's nose, drawing a straight vertical line instead.
**The Fix:** We updated the `six_series_solver.py` to use **cosine spacing**, which concentrates the generated points exactly at the leading and trailing edges where the curvature is highest. We also added a small coordinate `clip` so that no negative x-values are passed into the interpolator.

### 2. The Meanline Loading (`a`) Convention
**The Issue:** Standard UIUC NACA 6-series coordinates default to a meanline loading extent of `a = 1.0` (uniform loading across the entire chord). However, the original code defaulted `a` to the `pressure_location` (e.g., `0.3` for a 63-series). Fixing this to the standard `a=1.0` ruined the specific airfoil shapes the user was attempting to reproduce.
**Why it behaved this way:** The user's reference profiles were generated using the non-standard convention where `a = pressure_location`. By reverting our "fix" back to the original `a = designation.pressure_location` behavior, we restored the generator's ability to accurately match the specific target airfoils (90%+ accuracy).

---

## The 99.8% Accurate Match

To find the exact parameters that generated the user's reference coordinates, we ran a continuous numerical optimization (`scipy.optimize.minimize`) over the engine. 

The optimizer floated the parameters continuously and found the exact combination that yielded an **RMSE of 0.24 mm** (99.84% accuracy against a 150mm chord):

| Parameter | Value |
|-----------|-------|
| **Series Family** | `66` |
| **Pressure Location (`pl`)** | `0.5907` |
| **Design Lift Coefficient (`CL`)** | `0.9181` |
| **Thickness Ratio (`t/c`)** | `0.1487` |
| **Meanline Extent (`a`)** | `0.1967` |

### Python Code for the Exact Shape

You can inject these exact continuous parameters directly into the generator:

```python
from naca6.input.designation import NACA6Designation
from naca6.core.parameters import NACA6Parameters
from naca6.solvers.six_series_solver import generate_six_series

# 1. Define the continuous parameters
d = NACA6Designation(
    series=66, 
    pressure_location=0.5907, 
    design_lift_coefficient=0.9181, 
    thickness_ratio=0.1487
)

# 2. Inject into the generator along with the chord and meanline_a
p = NACA6Parameters(
    chord=150.0, 
    number_of_points=400, 
    designation=d, 
    meanline_a=0.1967
)

# 3. Generate the 99% perfect shape
r = generate_six_series(p)
```

### One-Liner Command (Standard Rounded Designation)

The closest standard string designation to this exact shape is **`66(9)-015`** with a custom `a=0.2`. You can run this directly in your terminal without any engine hardcoding:

```bash
python -c "from naca6.input.designation import parse_designation; from naca6.core.parameters import parse_parameters; from naca6.solvers.six_series_solver import generate_six_series; import matplotlib.pyplot as plt; d=parse_designation('66(9)-015'); p=parse_parameters('150.0','2000',d, meanline_a=0.2); r=generate_six_series(p); plt.figure(figsize=(14,5)); plt.plot(r.upper_x,r.upper_y,label='Upper surface'); plt.plot(r.lower_x,r.lower_y,label='Lower surface'); plt.plot(r.mean_x,r.mean_y,'--',label='Meanline'); plt.axis('equal'); plt.grid(); plt.xlabel('x (mm)'); plt.ylabel('y (mm)'); plt.title('NACA 66(9)-015 (a=0.2)'); plt.legend(); plt.show()"
```

---

## Frequently Asked Questions

### Why do I need to enter `chord = 150`? Can't I just use `1.0`?
Yes, using `chord = 1.0` absolutely works! The shape generated is mathematically identical and perfectly proportional. The only difference is the physical scale. 
If you use a chord of `1.0`, your maximum thickness for a 15% airfoil will be `0.15`. Because your original reference coordinates were physically scaled to 150 millimeters, you had to enter `150.0` so the resulting Y-coordinates would scale up to match your reference data (where the max thickness was 22.5 mm). 

### What is `meanline_a` and why isn't it part of the 6 digits?
In NACA airfoil theory, **`a` is the "extent of uniform loading fraction"**. 
A NACA 6-series camber line is designed to carry a uniform, constant pressure (lift) from the leading edge back to a specific point `a` (as a fraction of the chord length). From that point to the trailing edge, the load linearly drops to zero. 
- `a=1.0` means uniform lift across the entire wing.
- `a=0.2` means uniform lift only over the front 20% of the wing.

**Why isn't it in the 6 digits?**
The standard 6 digits only define three things: 
1. The series/minimum pressure location (e.g. `66`)
2. The Design Lift Coefficient (e.g. `9` for CL=0.9)
3. The thickness ratio (e.g. `015` for 15%)

The `a` value is an *independent modifier*. In standard NACA reports, if `a` is not 1.0, it is explicitly appended to the end of the designation string as a suffix (for example, `NACA 66(9)-015, a=0.2`). Because your specific 99% matched coordinates use an extreme, non-standard loading of `a=0.2`, we have to provide it explicitly!




# GPT
mod
```text
YT-ASSERTS/V3
│   README.md
│
└── 6_dig
    ├── dev_plot.py
    └── naca6
        ├── core
        │   └── validation.py
        ├── equations
        │   ├── conformal_mapping.py
        │   ├── meanline.py
        │   ├── thickness.py
        │   └── velocity_distribution.py
        ├── input
        │   └── designation.py
        ├── numerics
        │   ├── fourier.py
        │   └── integration.py
        ├── solvers
        │   └── six_series_solver.py
        └── tests
            ├── test_conformal_mapping.py
            ├── test_designation.py
            ├── test_generator.py
            └── test_thickness.py
```

# new
```text
YT-ASSERTS/V3
│   .~lock.lab.ods#
│
├── 6_dig
│   │   a_comparison.png
│   │   check_leading_edge.py
│   │   check_series.py
│   │   compare_63_8_015.png
│   │   final_comparison.png
│   │   final_user_plot.png
│   │   interp_compare.png
│   │   lower_surface_63_8_015.csv
│   │   opt_result.txt
│   │   optimized_match.png
│   │   reverted_plot.png
│   │
│   └── naca6
│       ├── data/
│       ├── equations
│       │   └── epsilon_psi.py
│       └── tests
│           ├── test_epsilon_psi.py
│           ├── test_fourier.py
│           ├── test_integration.py
│           └── test_solvers.py
│
└── ref
    └── 632215/```