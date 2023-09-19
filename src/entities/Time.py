from .Constant import Constant

class Time:
    def __init__(self, id: str, num_start: int):
        # returns time ID
        self.id: str = id
        # returns start time in numeric format
        self.num_start: int = num_start
        # returns end time in numeric format
        self.num_end: int = -1
        # returns start time in clock format
        self.clock_start: str = self._convert_to_time(num_start)
        # returns end time in numeric format
        self.clock_end: str = ''

    # given time index, returns time in string
    def _convert_to_time(self, time_index: int) -> str:
        if 0 <= time_index <= Constant.SLOTS_PER_DAY_NUM - 1:
            hours = 5 + time_index // 12
            minutes = (time_index % 12) * 5
            period = "AM" if hours < 12 else "PM"
            if hours == 12:
                period = "PM"
            if hours > 12:
                hours -= 12
            return f"{hours:02d}:{minutes:02d} {period}"
        else:
            return "Invalid input"
        
    # adds end time
    def add_clock_end(self, duration: int):
        self.num_end = self.num_start + (duration // Constant.RESOLUTION_IN_MINUTES)
        self.clock_end = self._convert_to_time(self.num_end)
