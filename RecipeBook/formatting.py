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
        unit = None
        cups = None
        pounds = None
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

        whole_number = 0
        if cups is not None:
            new_cups = cups * multiplier
            while new_cups >= 1:
                whole_number += 1
                new_cups -= 1
            if new_cups < Fraction(1/8):
                new_cups = new_cups * 16
                unit = "tbsp"
            elif new_cups < Fraction(1/16):
                new_cups = new_cups * 48
                unit = "tsp"
            if whole_number > 0:
                new_volume += str(whole_number) + " " + unit + " "
            elif new_cups > 0:
                new_volume += str(new_cups) + " " + unit
        elif pounds is not None:
            new_pounds = pounds * multiplier
            while new_pounds >= 1:
                whole_number += 1
                new_pounds -= 1
            if whole_number > 0:
                new_volume += str(whole_number) + " " + unit + " "
            if new_pounds > 0:
                new_pounds = new_pounds * 16
                unit = "oz"
                new_volume += str(new_pounds) + " " + unit
    else:
        # handle ingredients that use words like whole, half, quarter, etc... or things that don't use a unit of measure
        pass

    return new_volume


def parse_ingredient(ingredient):
    unit = None
    value = None
    unit_list = ["cups", "cup", "tablespoons", "tbsp", "tablespoon", "teaspoons", "tsp", "teaspoon", "pounds", "lbs",
                 "pound", "lb"]
    ingredient_listable = str(ingredient).split(' ')
    for item in ingredient_listable:
        if str(item) in unit_list:
            if unit is None:
                unit = unit_list.index(item)
            else:
                pass
        elif "/" in item:
            if value is None:
                if ingredient_listable.index(item) > 0:
                    value = ingredient_listable[ingredient_listable.index(item) - 1] + item
                else:
                    value = item
            else:
                pass
        elif item.isdigit():
            if value is None:
                value = item
            else:
                pass

    return value, unit
