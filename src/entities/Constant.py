import math

class Constant:
    # Time granularity
    RESOLUTION_IN_MINUTES = 5
    # Number of working time in minutes (17 hours from 5AM to 10PM)
    DAY_MINUTES = 17 * 60
    # Number of slots per day
    SLOTS_PER_DAY_NUM = DAY_MINUTES // RESOLUTION_IN_MINUTES
    # Number of days to consider
    DAYS_NUM = 30
    # Lowest program duration in minutes
    MIN_PROGRAM_DURATION = 30 + 10
    # Highest program duration in minutes
    MAX_PROGRAM_DURATION = 65 + 10
    # Maximum number of programs per day
    MAX_MONTH_PROGRAM_COUNT = math.floor((DAY_MINUTES / MIN_PROGRAM_DURATION) * DAYS_NUM)
    # Fitness adjustment constant
    FITNESS_ADJ = (MAX_PROGRAM_DURATION // RESOLUTION_IN_MINUTES) * MAX_MONTH_PROGRAM_COUNT
