from math import floor
from fractions import Fraction


def format_time(time_minutes):
    hours = floor(time_minutes / 60)
    minutes = time_minutes % 60
    time = ""

    if hours > 1:
        time += str(hours) + " hours "
    elif hours == 1:
        time += str(hours) + " hour "
    if minutes > 1:
        time += str(minutes) + " minutes"
    elif minutes == 1:
        time += str(minutes) + " minute"

    return time


def format_volume(volume, units, multiplier):
    unit_list = ["cups", "cup", "tablespoons", "tbsp", "tablespoon", "teaspoons", "tsp", "teaspoon", "pounds", "lbs",
                 "pound", "lb"]
    new_volume = ""
    if units in unit_list:
        if "c" in str(units).lower():
            unit = "cup"
            cups = Fraction(volume)
        elif any(x in str(units).lower() for x in ["tbsp", "tablespoon"]):
            unit = "tbsp"
            cups = Fraction(volume / 16)
        elif any(x in str(units).lower() for x in ["tsp", "teaspoon"]):
            unit = "tsp"
            cups = Fraction(volume / 48)
        elif any(x in str(units).lower() for x in ["fl oz", "oz", "ounce"]):
            unit = "oz"
            cups = Fraction(volume / 8)
        elif any(x in str(units).lower() for x in ["pound", "lb"]):
            unit = "lb"
            pounds = Fraction(volume)


    return new_volume
