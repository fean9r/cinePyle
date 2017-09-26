from enum import Enum


class WEEK_DAYS(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class Hour(object):
    """.
    """

    def __init__(self):
        self.events = []


class Date(object):
    """.
    """

    def __init__(self):
        self.events = []


class Event(object):
    """.
    """

    def __init__(self, name, start, all_day=True, all_day):
        self.name = name
        self.start = start
        self.duration = all_day
        self.all_day = all_day



class Agenda(object):
    """.
    """

    def __init__(self):
        self.events = []

    def add_busy_hours(self, name, start, stop, validity):
        self.events.append("")

    def add_event(self, ):