class RollingAverageCalculator:
    def __init__(self, window_size):
        if window_size <= 0:
            raise ValueError("Window size must be greater than 0")
        self.window_size = window_size
        self.data = []

    def rolling_average(self, new_number) -> float:
        self.data.append(new_number)
        if len(self.data) > self.window_size:
            self.data.pop(0)
        return sum(self.data) / len(self.data)
