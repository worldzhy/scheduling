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
    # program list
    PROGRAM_LIST = ['30minexpress', 'advanced', 'armsabs', 'beginner', 'bunsabs', 'bunsguns', 'training', 'foundations', 'fullbody']
    # month list
    MONTH_LIST = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # paths
    PATH_RAW = 'data/raw/'
    PATH_PROCESSED = 'data/processed/'
    # csv filenames
    CSV_CLASS = PATH_PROCESSED + 'class.csv'
    CSV_CLASS_DESC = PATH_PROCESSED + 'class_description.csv'
    CSV_DEMAND = PATH_PROCESSED + 'demand.csv'
    CSV_LOCATION = PATH_PROCESSED + 'location.csv'
    CSV_STUDIO = PATH_PROCESSED + 'studio.csv'
