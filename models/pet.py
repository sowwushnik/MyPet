import math
from datetime import datetime

class Pet:
    def __init__(self, name, age, weight, **kwargs):  # Добавили **kwargs
        self.name = name
        self.age = max(0, age)
        self.weight = weight if weight > 0 else 1.0

        # Загружаем из kwargs или ставим дефолт
        self.health_logs = kwargs.get("health_logs", [])
        self.last_checkup = kwargs.get("last_checkup", "Not recorded")
        self.is_vaccinated = kwargs.get("is_vaccinated", False)

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
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        full_entry = f"[{timestamp}] {entry}"

        self.health_logs.append(full_entry)
        return f"Log added for {self.name} at {timestamp}!"

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


    def get_weight_category(self):
        return "Unknown"

    def get_vaccination_status(self):
        if self.is_vaccinated:
            return "Fully vaccinated"
        else:
            return "NOT VACCINATED (Action required)"

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "health_logs": self.health_logs,
            "last_checkup": self.last_checkup,
            "is_vaccinated": self.is_vaccinated,
        }

class Dog(Pet):
    def __init__(self, name, age, weight, breed, temperament, **kwargs):
        super().__init__(name, age, weight, **kwargs) # Передаем kwargs наверх
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

    def get_weight_category(self):
        if self.weight < 5:
            return "Toy/Small (Check for fragile bones)"
        elif 5 <= self.weight < 30:
            return "Medium (Ideal for most active breeds"
        else:
            return "Large/Giant (Watch for joint pressure)"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "breed": self.breed,
            "temperament": self.temperament,
        })
        return data

class Cat(Pet):
    def __init__(self, name, age, weight, breed, temperament, **kwargs):
        super().__init__(name, age, weight, **kwargs) # Передаем kwargs наверх
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

    def get_weight_category(self):
        if self.weight < 3.5:
            return "Underweight (Needs more nutrition)"
        elif 3.5 <= self.weight < 5.5:
            return "Ideal Weight (Perfect condition)"
        else:
            return "Overweight (Risk of diabetes, consult vet)"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "breed": self.breed,
            "temperament": self.temperament,
        })
        return data