from fractions import Fraction
from RecipeBook.formatting import Volumes, format_weight

test_info = Volumes.format_volume(Fraction(1 + 1/2), "tsp", 2)
print(test_info)

test_info_2 = format_weight(1/2, "lb", 1/2)
print(test_info_2)
