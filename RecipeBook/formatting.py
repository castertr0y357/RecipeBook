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


def format_volume(amount, units, multiplier):
    volume_unit_list = ["cups", "cup", "tablespoons", "tbsp", "tablespoon", "teaspoons", "tsp", "teaspoon", "gallon",
                        "gallons", "gals", "gal", "ounce", "ounces", "oz", "fl oz", "pint", "pints", "quart", "quarts"]
    new_volume = ""
    units = units.lower()
    teaspoons = 0
    if units in volume_unit_list:
        if units == "cups" or "cup":
            teaspoons = amount * 64
        elif units == "tablespoons" or "tbsp" or "tablespoon":
            teaspoons = amount * 3
        elif units == "teaspoons" or "tsp" or "teaspoon":
            teaspoons = amount
        elif units == "gallon" or "gallons" or "gals" or "gal":
            teaspoons = amount * 1024
        elif units == "pint" or "pints":
            teaspoons = amount * 128
        elif units == "quart" or "quarts":
            teaspoons = amount * 256
        elif units == "ounce" or "ounces" or "oz" or "fl oz":
            teaspoons = amount * 6

        new_teaspoons = teaspoons * multiplier

        if new_teaspoons > 1:
            tablespoons = int(new_teaspoons / 3)
            cups = int(tablespoons / 16)
            gallons = int(cups / 16)

            # format volumes
            cups = cups % 16
            tablespoons = tablespoons % 16
            teaspoons = new_teaspoons % 3

            if gallons > 0:
                new_volume += (str(gallons) + " gallons ")
            if cups > 0:
                new_volume += (str(cups) + " cups ")
            if tablespoons > 0:
                new_volume += (str(tablespoons) + " tablespoons ")
            if teaspoons > 0:
                new_volume += (str(teaspoons) + " teaspoons ")
        else:
            new_volume = (str(new_teaspoons) + " teaspoons ")
    return new_volume


def format_weight(amount, units, multiplier):
    weight_unit_list = ["pounds", "lbs", "pound", "lb", "ounce", "ounces", "oz"]
    new_weight = ""
    units = units.lower()
    ounces = 0
    if units in weight_unit_list:
        if units == "pounds" or "lbs" or "pound" or "lb":
            ounces = amount * 16
        elif units == "ounce" or "ounces" or "oz":
            ounces = amount

        new_ounces = ounces * multiplier

        if new_ounces > 1:
            pounds = int(ounces / 16)

            # format weight
            ounces = new_ounces % 16

            if pounds > 0:
                if ounces % 12 == 0:
                    new_weight += (str(pounds) + " 3/4 " + " pounds ")
                elif ounces % 8 == 0:
                    new_weight += (str(pounds) + " 1/2 " + " pounds ")
                elif ounces % 4 == 0:
                    new_weight += (str(pounds) + " 1/4 " + " pounds ")
                else:
                    new_weight += (str(pounds) + " pounds ")
            if ounces > 0:
                if ounces % 12 == 0:
                    pass
                elif ounces % 8 == 0:
                    pass
                elif ounces % 4 == 0:
                    pass
                else:
                    new_weight += (str(ounces) + " ounces ")
    return new_weight
