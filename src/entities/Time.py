from .Constant import Constant

class Time:
    def __init__(self, id: str, value: int):
        # returns time ID
        self.id = id
        # returns time value
        self.value = value
        # start time
        self.clock_start = self._convert_to_time(value)
        # end time
        self.clock_end = ''

    # given time index, returns time in string
    def _convert_to_time(self, time_index: int) -> str:
        if 0 <= time_index <= 203:
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
        
    # adds clock end time
    def add_clock_end(self, duration: int):
        self.clock_end = self._convert_to_time(self.value + duration // Constant.RESOLUTION_IN_MINUTES)