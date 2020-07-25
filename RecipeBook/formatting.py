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
    if units == "cups" or "cup":
        cups = volume
    return new_volume
