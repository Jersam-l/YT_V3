from naca6.input.designation import parse_designation

input_1= parse_designation(input("Enter the NACA 6-series designation (e.g. 66(2)-015): "))

print(" ",input_1.series,"\n",input_1.design_lift_coefficient,"\n",input_1.thickness_ratio)
