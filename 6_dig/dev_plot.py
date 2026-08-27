from naca6.input.designation import parse_designation
input_1= parse_designation(input("Enter the NACA 6-series designation (e.g. 66(2)-015): "))
#2

from naca6.core.parameters import parse_parameters
input_2= parse_parameters(input("Enter the chord length (e.g. 1.0): "), input("Enter the number of points (e.g. 100): "), input_1)

#test print statements
print(" ",input_1.series,"\n",input_1.design_lift_coefficient,"\n",input_1.thickness_ratio)
print(" ",input_2.chord,"\n",input_2.number_of_points)