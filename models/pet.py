import math

class Pet:
    def __init__(self, name, age, weight):
        self.name = name

        if age < 0:
            print(f"Warning: Age for {name} cannot be negative. Setting to 0")
            self.age = 0
        else:
            self.age = age

        if weight <= 0:
            print(f"Warning: Weight for {name} must be positive. Setting to 1kg default")
            self.weight = 1.0
        else:
            self.weight = weight

        self.health_logs = []
        self.last_checkup = "Not recorded"

    def __str__(self):
        return (f"---------------------------\n"
                f"NAME: {self.name}\n"
                f"TYPE: {self.__class__.__name__}\n"
                f"AGE: {self.age} years\n"
                f"WEIGHT: {self.weight} kg\n"
                f"---------------------------")

    def calculate_daily_calories(self):
        return 70 * math.pow(self.weight, 0.75)

    def add_log(self, entry):
        self.health_logs.append(entry)
        return f"Log added for {self.name}!"

    def get_history(self):
        if not self.health_logs:
            return f"No logs for {self.name} yet"
        
        return "\n".join(self.health_logs)

    def get_health_advice(self):
        return "Regular vet visits are recommended once a year"

    def check_health_status(self):
        status = "Healthy / Normal"

        if self.age > 10 and self.weight > 30:
            status = "Senior - Watch for joints and weight"
        elif self.weight < 2:
            status = "Underweight or very small - Ensure high calorie intake"

        return status

class Dog(Pet):
    def __init__(self, name, age, weight, breed, temperament):
        super().__init__(name, age, weight)
        self.breed = breed
        self.temperament = temperament

    def __str__(self):
        return (f"---------------------------\n"
                f"NAME: {self.name}\n"
                f"TYPE: {self.__class__.__name__}\n"
                f"AGE: {self.age} years\n"
                f"WEIGHT: {self.weight} kg\n"
                f"BREED: {self.breed}\n"
                f"CHARACTER: {self.temperament}\n"
                f"---------------------------")

    def calculate_daily_calories(self):
        rer = super().calculate_daily_calories()
        return rer * 1.2

    def get_health_advice(self):
        return f"Advice for {self.breed}: Check paws after walks and visit vet every 6 months"

class Cat(Pet):
    def __init__(self, name, age, weight, breed, temperament):
        super().__init__(name, age, weight)
        self.breed = breed
        self.temperament = temperament

    def __str__(self):
        return (f"---------------------------\n"
                f"NAME: {self.name}\n"
                f"TYPE: {self.__class__.__name__}\n"
                f"AGE: {self.age} years\n"
                f"WEIGHT: {self.weight} kg\n"
                f"BREED: {self.breed}\n"
                f"CHARACTER: {self.temperament}\n"
                f"---------------------------")

    def calculate_daily_calories(self):
        rer = super().calculate_daily_calories()
        return rer * 1.0

    def get_health_advice(self):
        return "Advice: Monitor dental health and ensure fresh water is always available"