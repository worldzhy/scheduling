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
    PATH_FOLDER_RAW = 'data/raw/'
    PATH_FOLDER_PROCESSED = 'data/processed/'
    # csv filenames
    PATH_CSV_CLASS = PATH_FOLDER_PROCESSED + 'class.csv'
    PATH_CSV_CLASS_DESC = PATH_FOLDER_PROCESSED + 'class_description.csv'
    PATH_CSV_DEMAND = PATH_FOLDER_PROCESSED + 'demand.csv'
    PATH_CSV_LOCATION = PATH_FOLDER_PROCESSED + 'location.csv'
    PATH_CSV_STUDIO = PATH_FOLDER_PROCESSED + 'studio.csv'
