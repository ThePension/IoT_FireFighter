
class Measure:
    def __init__(self, temperature = 0, humidity = 0, pressure = 0, fireRating = 0):
        self.name = "Measure"
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.fireRating = fireRating

    def __str__(self):
        return self.name + ": " + str(self.value)

    def __repr__(self):
        return self.name + ": " + str(self.value)