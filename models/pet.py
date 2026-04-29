import math

class Pet:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.health_logs = []

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.name}: {self.weight}kg, {self.age} years old"

    def calculate_daily_calories(self):
        return 70 * math.pow(self.weight, 0.75)

    def add_log(self, entry):
        self.health_logs.append(entry)
        return f"Log added for {self.name}!"

    def get_history(self):
        if not self.health_logs:
            return f"No logs for {self.name} yet"
        
        return "\n".join(self.health_logs)

class Dog(Pet):
    def calculate_daily_calories(self):
        rer = super().calculate_daily_calories()
        return rer * 1.2

class Cat(Pet):
    def calculate_daily_calories(self):
        rer = super().calculate_daily_calories()
        return rer * 1.0