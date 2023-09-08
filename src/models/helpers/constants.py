class Constant:
        # Time granularity
        RESOLUTION_IN_MINUTES = 5
        # Number of working time in minutes (17 hours from 5AM to 10PM)
        DAY_MINUTES = 17 * 60
        # Number of slots per day
        SLOTS_PER_DAY_NUM = DAY_MINUTES / RESOLUTION_IN_MINUTES
        # Number of days to consider
        DAYS_NUM = 30
