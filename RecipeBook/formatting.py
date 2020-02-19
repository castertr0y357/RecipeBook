from math import floor


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
