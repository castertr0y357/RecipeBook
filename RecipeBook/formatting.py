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
    unit_list = ["cups", "cup", "tablespoons", "tablespoon", "tbsp", "tbsps", "teaspoons", "teaspoon", "tsp", "tsps",
                 "pounds", "lbs", "pound", "lb", "fl ozs", "fl oz", "oz", "ozs", "ounce", "ounces"]
    lower_volume = None
    if volume is not None:
        if "-" in volume:
            split_volumes = volume.split("-")
            lower_volume = Fraction(split_volumes[0])
            volume = Fraction(split_volumes[1])
        elif "/" in volume and " " in volume:
            split_volume = volume.split(" ")
            whole_number = Fraction(split_volume[0])
            fraction = Fraction(split_volume[1])
            volume = Fraction(whole_number + fraction)
        else:
            volume = Fraction(volume)

    multiplier = Fraction(multiplier).limit_denominator(10)
    new_volume = ""
    if units in unit_list:
        unit = None
        cups = None
        lower_cups = None
        pounds = None
        lower_pounds = None
        if any(x in str(units).lower() for x in ["cup", "cups"]):
            # unit = "cup"
            cups = Fraction(volume)
            if lower_volume is not None:
                lower_cups = Fraction(lower_volume)
        elif any(x in str(units).lower() for x in ["tbsp", "tbsps", "tablespoon", "tablespoons"]):
            # unit = "tbsp"
            cups = Fraction(volume / 16)
            if lower_volume is not None:
                lower_cups = Fraction(lower_volume / 16)
        elif any(x in str(units).lower() for x in ["tsp", "tsps", "teaspoon", "teaspoons"]):
            # unit = "tsp"
            cups = Fraction(volume / 48)
            if lower_volume is not None:
                lower_cups = Fraction(lower_volume / 48)
        elif any(x in str(units).lower() for x in ["fl oz", "fl ozs", "fluid"]):
            # unit = "oz"
            cups = Fraction(volume / 8)
            if lower_volume is not None:
                lower_cups = Fraction(volume / 8)
        elif any(x in str(units).lower() for x in ["oz", "ozs", "ounce", "ounces"]):
            # unit = "oz"
            pounds = Fraction(volume / 16)
            if lower_volume is not None:
                lower_pounds = Fraction(lower_volume / 16)
        elif any(x in str(units).lower() for x in ["pound", "pounds", "lb", "lbs"]):
            # unit = "lb"
            pounds = Fraction(volume)
            if lower_volume is not None:
                lower_pounds = Fraction(lower_volume)

        whole_number = 0
        lower_whole_number = 0
        if cups is not None:
            lower_new_cups = None
            new_cups = Fraction(cups * multiplier)
            if lower_cups is not None:
                lower_new_cups = Fraction(lower_cups * multiplier)
            if new_cups < Fraction(1/16):
                new_cups = new_cups * 48
                if lower_cups is not None:
                    lower_new_cups = lower_new_cups * 48
                unit = "tsp"
            elif new_cups < Fraction(1/8):
                new_cups = new_cups * 16
                if lower_cups is not None:
                    lower_new_cups = lower_new_cups * 16
                unit = "tbsp"
            else:
                unit = "cup"
            while new_cups >= 1:
                whole_number += 1
                new_cups -= 1
            if lower_new_cups is not None:
                while lower_new_cups >= 1:
                    lower_whole_number += 1
                    lower_new_cups -= 1
                if lower_whole_number > 0:
                    new_volume += str(lower_whole_number)
                if lower_new_cups > 0:
                    if lower_whole_number > 0:
                        new_volume += " "
                    new_volume += str(lower_new_cups)
                if lower_whole_number > 0 or lower_new_cups > 0:
                    new_volume += "-"
            if whole_number > 0:
                if unit == "cup":
                    if whole_number > 1:
                        unit = "cups"
                new_volume += str(whole_number) + " "
            if new_cups > 0:
                new_volume += str(new_cups) + " "
            new_volume += unit
        elif pounds is not None:
            lower_new_pounds = None
            new_pounds = Fraction(pounds * multiplier)
            if lower_pounds is not None:
                lower_new_pounds = Fraction(lower_pounds * multiplier)
            whole_ounces = 0
            lower_whole_ounces = 0
            if lower_new_pounds is not None:
                while lower_new_pounds >= 1:
                    lower_whole_number += 1
                    lower_new_pounds -= 1
                if lower_whole_number >= 1:
                    lower_unit = "lbs"
                    new_volume += str(lower_whole_number) + " " + lower_unit + " "
                if lower_new_pounds > 0:
                    lower_new_pounds = lower_new_pounds * 16
                    while lower_new_pounds >= 1:
                        lower_whole_ounces += 1
                        lower_new_pounds -= 1
                    lower_unit = "oz"
                    if lower_whole_ounces > 0:
                        new_volume += str(lower_whole_ounces) + " "
                    if lower_new_pounds > 0:
                        new_volume += str(lower_new_pounds) + " "
                    new_volume += lower_unit
                new_volume += "-"
            while new_pounds >= 1:
                whole_number += 1
                new_pounds -= 1
            if whole_number >= 1:
                unit = "lbs"
                new_volume += str(whole_number) + " " + unit + " "
            if new_pounds > 0:
                new_pounds = new_pounds * 16
                while new_pounds >= 1:
                    whole_ounces += 1
                    new_pounds -= 1
                unit = "oz"
                if whole_ounces > 0:
                    new_volume += str(whole_ounces) + " "
                if new_pounds > 0:
                    new_volume += str(new_pounds) + " "
                new_volume += unit
    else:
        # handle ingredients that use words like whole, half, quarter, etc... or things that don't use a unit of measure
        size_descriptions = ["whole", "half", "third", "quarter"]
        size_values = [Fraction(1), Fraction(1/2), Fraction(1/3), Fraction(1/4)]
        if units in size_descriptions:
            pass
        else:
            if volume is not None:
                whole_number = 0
                new_value = Fraction(volume * multiplier)
                while new_value >= 1:
                    whole_number += 1
                    new_value -= 1
                if whole_number > 0:
                    new_volume += str(whole_number) + " "
                if new_value > 0:
                    new_volume += str(new_value)

    return new_volume


def parse_ingredient(ingredient):
    unit = None
    value = None
    ingredient_remainder = ""
    unit_list = ["cups", "cup", "tablespoons", "tbsp", "tablespoon", "teaspoons", "tsp", "teaspoon", "pounds", "lbs",
                 "pound", "lb", "fl oz", "fluid", "oz", "ozs", "ounce", "ounces", "whole", "half", "third", "quarter"]
    ingredient_listable = str(ingredient).split(' ')
    for item in ingredient_listable:
        if str(item) in unit_list:
            if unit is None:
                unit = unit_list[unit_list.index(item)]
        elif "-" in item:
            if value is None:
                value = item
        elif "/" in item:
            if value is None:
                value = item
            else:
                value += (" " + item)
        elif item.isdigit():
            if value is None:
                value = item
        else:
            ingredient_remainder += str(item)
            if item != ingredient_listable[-1]:
                ingredient_remainder += " "

    return value, unit, ingredient_remainder
