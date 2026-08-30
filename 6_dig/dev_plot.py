from naca6.input.designation import parse_designation
input_1= parse_designation(input("Enter the NACA 6-series designation (e.g. 66(2)-015): "))
#2

from naca6.core.parameters import parse_parameters
# The chord length scales the final coordinates. A chord of 1.0 produces standard unit coordinates.
# If you want physical dimensions (e.g., matching a 150mm wing), enter 150.0.
chord_input = input("Enter the chord length (e.g. 150.0): ")
pts_input = input("Enter the number of points (e.g. 2000): ")

# 'a' is the extent of uniform loading (as a fraction of the chord).
# It is an independent modifier and not part of the standard 6 digits.
a_input = input("Enter the extent of uniform loading fraction 'a' (e.g. 0.2, or leave blank for default): ")

a_val = float(a_input) if a_input.strip() else None

input_2 = parse_parameters(chord_input, pts_input, input_1, meanline_a=a_val)

from naca6.solvers.six_series_solver import generate_six_series
import matplotlib.pyplot as plt

print(f"Generating NACA {input_1.series} series (CL={input_1.design_lift_coefficient}, t/c={input_1.thickness_ratio})...")

result = generate_six_series(input_2)
# Designation: 66(9)-015
# Chord length: 150
# Number of points: 2000
# meanline_a: 0.2

plt.figure(figsize=(12, 5))
plt.plot(result.upper_x, result.upper_y, 'b-', lw=1.5, label='Upper Surface')
plt.plot(result.lower_x, result.lower_y, 'r-', lw=1.5, label='Lower Surface')
plt.plot(result.mean_x, result.mean_y, 'g--', lw=1.0, label='Meanline')

title_str = f"NACA {input_1.series}({int(input_1.design_lift_coefficient*10)})-{int(input_1.thickness_ratio*100):03d}"
if a_val is not None:
    title_str += f" (a={a_val})"
plt.title(title_str)
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

filename = f"NACA{input_1.series}({int(input_1.design_lift_coefficient * 10)})-{int(input_1.thickness_ratio * 100):03d}_a-{a_input or 'default'}.dat"
with open(filename, "w") as file:
    for x,y in zip(result.boundary_x, result.boundary_y):
        file.write(f"{x:.8f}    {y:.8f}\n")