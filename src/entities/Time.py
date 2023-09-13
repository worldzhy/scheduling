from entities.Constant import Constant

class Time:
    # Initializes time
    def __init__(self, id: str, value: int):
        # Returns time ID
        self.id = id
        # Returns time value
        self.value = value
        # Start time
        self.clock_start = self._convert_to_time(value)
        # End time
        self.clock_end = ''

    def _convert_to_time(self, value: int):
        if 0 <= value <= 203:
            hours = 5 + value // 12
            minutes = (value % 12) * 5
            period = "AM" if hours < 12 else "PM"
            if hours == 12:
                period = "PM"
            if hours > 12:
                hours -= 12
            return f"{hours:02d}:{minutes:02d} {period}"
        else:
            return "Invalid input"
        
    def add_clock_end(self, duration: int):
        self.clock_end = self._convert_to_time(self.value + duration // Constant.RESOLUTION_IN_MINUTES)