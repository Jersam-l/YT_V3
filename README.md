1. input/designation.py ++++++++
          ↓
2. core/parameters.py ++++++++++(parameters.designation.series
parameters.designation.design_lift_coefficient parameters.designation thickness_ratio parameters.chord parameters.number_of_points)
```text
            NACA6Parameters
            │
            ├── designation
            │   ├── series = 66
            │   ├── design_lift_coefficient = 0.2
            │   └── thickness_ratio = 0.15
            │
            ├── chord = 1.0
            │
            └── number_of_points = 200```
          ↓
3. core/validation.py+++------- api should be linked 
          ↓
4. core/result.py+++++++---
          ↓
5. equations/meanline.py-------------------[errors due to limitss]
          ↓
6. equations/velocity_distribution.py
          ↓
7. equations/conformal_mapping.py
          ↓
8. equations/thickness.py
          ↓
9. numerics/
          ↓
10. solvers/
          ↓
11. api.py
          ↓
12. dev_plot.py
```
#
```text
Folder PATH listing for volume New Volume
Volume serial number is 0000001A 6E62:77B1
Z:.
│   dev_plot.py
│   gpt.py
│   naca_6.py
│   README.md
│   
└───naca6
    │   api.py
    │   __init__.py
    │   
    ├───core
    │       parameters.py
    │       result.py
    │       validation.py
    │       __init__.py
    │       
    ├───equations
    │       conformal_mapping.py
    │       meanline.py
    │       thickness.py
    │       velocity_distribution.py
    │       __init__.py
    │       
    ├───input
    │       designation.py
    │       __init__.py
    │       
    ├───numerics
    │       fourier.py
    │       integration.py
    │       iteration.py
    │       quadrature.py
    │       __init__.py
    │       
    ├───solvers
    │       conformal_solver.py
    │       meanline_solver.py
    │       six_series_solver.py
    │       thickness_solver.py
    │       __init__.py
    │       
    └───tests
            test_conformal_mapping.py
            test_designation.py
            test_generator.py
            test_meanline.py
            test_thickness.py
            __init__.py
            
PS Z:\YT-ASSERTS\V3\6_dig> 

```
T1>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"66(2)-015"
      ↓
designation parser
      ↓
series = 66
design lift coefficient = 0.2
thickness ratio = 0.15