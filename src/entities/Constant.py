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
    # weekday list
    WEEKDAY_LIST = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # coach tier list
    COACH_TIER_LIST = ['New', 'Standard', 'Senior', 'Pro', 'Master']
    # time list
    TIMESLOT_LIST = ['05:00:00', '05:30:00', '06:00:00', '06:30:00', '07:00:00', '07:30:00', '08:00:00', '08:30:00', '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00', '18:00:00', '18:30:00', '19:00:00', '19:30:00', '20:00:00', '20:30:00', '21:00:00', '21:30:00', '22:00:00']
    # paths
    PATH_FOLDER_RAW = 'data/raw/'
    PATH_FOLDER_PROCESSED = 'data/processed/'
    # csv filenames
    PATH_CSV_CLASS = PATH_FOLDER_PROCESSED + 'class.csv'
    PATH_CSV_CLASS_DESC = PATH_FOLDER_PROCESSED + 'class_description.csv'
    PATH_CSV_DEMAND = PATH_FOLDER_PROCESSED + 'demand.csv'
    PATH_CSV_LOCATION = PATH_FOLDER_PROCESSED + 'location.csv'
    PATH_CSV_STUDIO = PATH_FOLDER_PROCESSED + 'studio.csv'
