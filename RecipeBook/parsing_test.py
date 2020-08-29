from fractions import Fraction

ingredient_1 = "1 1/2 cups flour"
ingredient_2 = "1/4 cups of sugar"
ingredient_3 = "3 tablespoons of salt"
ingredients = [ingredient_1, ingredient_2, ingredient_3]
for ingredient in ingredients:
    if "/" in ingredient:
        split_point = ingredient.find("/")
        values = ingredient[0:(split_point + 2)]
        ingredient_name = ingredient[(split_point + 3):]
        print("values:", values)
        if " " in values:
            whole_number = values.split(" ")[0]
            fraction = values.split(" ")[1]
            combined_fraction = int(whole_number) + Fraction(fraction)
            manipulated_fraction = Fraction(combined_fraction * 0.5)
            print("whole number:", whole_number)
            print("fraction:", fraction)
            print("combined fraction:", combined_fraction)
            print("manipulated fraction:", manipulated_fraction)
            print("Resized ingredient:", manipulated_fraction, ingredient_name)
            print()
        else:
            manipulated_fraction = Fraction(values) / 2
            print("manipulated fraction:", manipulated_fraction)
            if manipulated_fraction < Fraction(1/4):
                manipulated_fraction = manipulated_fraction * 16
                print("tablespoons:", manipulated_fraction)
                print("Resized ingredient:", manipulated_fraction, ingredient_name)
                print()

    else:
        whole_number = 0
        value = ingredient[0]
        print("value:", value)
        fraction = Fraction(value)
        print("fraction:", fraction)
        manipulated_fraction = fraction / 2
        print("manipulated fraction:", manipulated_fraction)
        while manipulated_fraction > 1:
            whole_number += 1
            manipulated_fraction -= 1
        if whole_number > 0:
            print("whole number:", whole_number)
        print("new manipulated fraction:", manipulated_fraction)
        print("new values:", str(whole_number) + " " + str(manipulated_fraction))
        print()
