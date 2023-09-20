import math

class Constant:
    # time granularity
    RESOLUTION_IN_MINUTES = 5
    # number of working time in minutes (17 hours from 5AM to 10PM)
    DAY_MINUTES = 17 * 60
    # number of slots per day
    SLOTS_PER_DAY_NUM = DAY_MINUTES // RESOLUTION_IN_MINUTES
    # number of days to consider
    DAYS_NUM = 30
    # lowest program duration in minutes
    MIN_PROGRAM_DURATION = 30 + 10
    # highest program duration in minutes
    MAX_PROGRAM_DURATION = 65 + 10
    # maximum number of programs on a month
    MAX_MONTH_PROGRAM_COUNT = math.floor((DAY_MINUTES / MIN_PROGRAM_DURATION) * DAYS_NUM)
    # maximum number of programs on a day
    MAX_DAY_PROGRAM_COUNT = math.floor(DAY_MINUTES / MIN_PROGRAM_DURATION)
    # fitness adjustment constant
    FITNESS_ADJ = (MAX_PROGRAM_DURATION // RESOLUTION_IN_MINUTES) * MAX_MONTH_PROGRAM_COUNT
