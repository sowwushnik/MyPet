import json
import os
from config import PET_CLASSES

class PetStorage:
    def __init__(self, filename = "pets_data.json"):
        self.filename = filename

    def load_pets(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding = "utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                pet_type = item.pop("type", "Dog")
                cls = PET_CLASSES.get(pet_type, PET_CLASSES["Dog"])
                loaded.append(cls(**item))
            return loaded
        except Exception as e:
            print(f"Error loading pet data: {e}")
            return []

    def save_pets(self, pets):
        try:
            data = [p.to_dict() for p in pets]
            with open(self.filename, "w", encoding = "utf-8") as f:
                json.dump(data, f, indent = 4, ensure_ascii = False)
        except Exception as e:
            print(f"Error saving pet data: {e}")



