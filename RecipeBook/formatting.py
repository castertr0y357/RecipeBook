from math import floor, modf
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


class Volumes:

    @staticmethod
    def format_volume(amount, units, multiplier):
        multiplier = Fraction(multiplier)
        volume_unit_list = ["cups", "cup", "tablespoons", "tbsp", "tablespoon", "teaspoons", "tsp", "teaspoon",
                            "gallon", "gallons", "gals", "gal", "ounce", "ounces", "oz", "fl oz", "pint", "pints",
                            "quart", "quarts"]
        new_volume = ""
        units = units.lower()
        teaspoons = 0
        cups = 0
        if units in volume_unit_list:
            if units in ["teaspoons", "tsp", "teaspoon", "tsps"]:
                print("units: ", units)
                teaspoons = amount
            elif units in ["tablespoons", "tbsp", "tablespoon", "tbsps"]:
                print("units: ", units)
                teaspoons = amount * 3
            elif units in ["ounce", "ounces", "oz", "fl oz"]:
                print("units: ", units)
                cups = Fraction(amount / 8)
            elif units in ["cups", "cup"]:
                print("units: ", units)
                cups = amount
            elif units in ["pint", "pints", "pt", "pts"]:
                print("units: ", units)
                cups = amount * 2
            elif units in ["quart", "quarts", "qt", "qts"]:
                print("units: ", units)
                cups = amount * 4
            elif units in ["gallon", "gallons", "gals", "gal"]:
                print("units: ", units)
                cups = amount * 16
            else:
                print("Unit " + units + " not identified")
                pass
            # print("teaspoons: ", teaspoons)
            # print("cups: ", cups)

            if teaspoons > 0:
                # print("teaspoons: ", teaspoons)
                new_teaspoons = Fraction(teaspoons * multiplier)

                # print("new teaspoons: ", new_teaspoons)

                if new_teaspoons > 11:
                    new_volume = Volumes.cup_formatting(new_teaspoons, "tsp")
                else:
                    new_volume = Volumes.teaspoon_formatting(new_teaspoons, "tsp")

            elif cups > 0:
                # print("cups: ", cups)
                new_cups = Fraction(cups * multiplier)
                # fraction, integer = modf(new_cups)
                # print("new cups: ", int(integer), Fraction(fraction))

                if new_cups < 1/4:
                    new_volume = Volumes.teaspoon_formatting(new_cups, "cup")
                else:
                    new_volume = Volumes.cup_formatting(new_cups, "cup")

        return new_volume

    @staticmethod
    def fraction_separator(value):
        fraction, integer = modf(value)
        if fraction == 0:
            return int(integer)
        elif integer == 0:
            return Fraction(fraction)
        else:
            return str(int(integer)) + " " + str(Fraction(fraction))

    @staticmethod
    def teaspoon_formatting(amount, unit):
        new_volume = ""
        teaspoons = 0
        tablespoons = 0
        if unit in ["teaspoons", "tsp", "teaspoon", "tsps"]:
            # print("units: ", unit)
            teaspoons = amount
        elif unit in ["tablespoons", "tbsp", "tablespoon", "tbsps"]:
            # print("units: ", unit)
            teaspoons = amount * 3
        elif unit in ["cups", "cup"]:
            # print("units: ", unit)
            teaspoons = amount * 48

        if teaspoons > 1:
            # print("teaspoons: ", teaspoons)
            tablespoons = int(teaspoons / 3)

            # format volumes
            tablespoons = tablespoons % 16
            teaspoons = int(teaspoons % 3)

        # format the volume
        if tablespoons > 0:
            tablespoons = Volumes.fraction_separator(tablespoons)
            new_volume += (str(tablespoons) + " tablespoons ")
        if teaspoons > 0:
            teaspoons = Volumes.fraction_separator(teaspoons)
            new_volume += (str(teaspoons) + " teaspoons ")

        return new_volume

    @staticmethod
    def cup_formatting(amount, unit):
        new_volume = ""
        cups = 0
        gallons = 0
        if unit in ["teaspoons", "tsp", "teaspoon", "tsps"]:
            # print("units: ", unit)
            cups = amount / 48
        elif unit in ["tablespoons", "tbsp", "tablespoon", "tbsps"]:
            # print("units: ", unit)
            cups = amount / 16
        elif unit in ["ounce", "ounces", "oz", "fl oz"]:
            # print("units: ", unit)
            cups = Fraction(amount / 8)
        elif unit in ["cups", "cup"]:
            # print("units: ", unit)
            cups = amount

        if cups > 1:
            gallons = int(cups / 16)

            # format volumes
            cups = cups % 16
        else:
            cups = cups

        if gallons > 0:
            gallons = Volumes.fraction_separator(gallons)
            new_volume += (str(gallons) + " gallons ")
        if cups > 0:
            cups = Volumes.fraction_separator(cups)
            new_volume += (str(cups) + " cups ")

        return new_volume


def format_weight(amount, units, multiplier):
    multiplier = Fraction(multiplier)
    weight_unit_list = ["pounds", "lbs", "pound", "lb", "ounce", "ounces", "oz"]
    new_weight = ""
    units = units.lower()
    ounces = 0
    if units in weight_unit_list:
        if units in ["pounds", "lbs", "pound", "lb"]:
            print("units: ", units)
            ounces = amount * 16
        elif units in ["ounce", "ounces", "oz"]:
            print("units: ", units)
            ounces = amount

        new_ounces = ounces * multiplier

        if new_ounces > 0:
            print(new_ounces)
            pounds = int(new_ounces / 16)

            # format weight
            ounces = new_ounces % 16

            if pounds > 0:
                new_weight += (str(int(pounds)) + " lbs ")
            if ounces > 0:
                new_weight += (str(int(ounces)) + " oz ")
    return new_weight
