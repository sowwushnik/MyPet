from models.pet import Dog,Cat
import json
import os

def display_menu():
    print("\n --- MyPet: Health Tracker --- \n")
    print("1. Register a Dog")
    print("2. Register a Cat")
    print("3. View Registered Pets")
    print("4. Add Health Log")
    print("5. View Health History")
    print("6. Update Last Checkup")
    print("7. Vaccination")
    print("8. Exit \n")
    return input("Select an option: ")

def load_pets():
    filename = "pets_data.json"

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r") as f:
            data = json.load(f)

        loaded_pets = []
        for item in data:
            pet_type = item.get("type")

            if pet_type == "Dog":
                pet = Dog(item["name"], item["age"], item["weight"], item["breed"], item["temperament"])
            elif pet_type == "Cat":
                pet = Cat(item["name"], item["age"], item["weight"], item["breed"], item["temperament"])
            else:
                continue

            pet.is_vaccinated = item.get("is_vaccinated", False)
            pet.last_checkup = item.get("last_checkup", "Not recorded")
            pet.health_logs = item.get("health_logs", [])

            loaded_pets.append(pet)

        return loaded_pets
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def select_pet(pets_list):
    if not pets_list:
        print("No pets available!")
        return None

    print("\n Select a pet: \n")
    for i, pet in enumerate(pets_list):
        print(f"{i + 1}. {pet.name}")

    try:
        choice = int(input("\nEnter your choice: ")) - 1
        if 0 <= choice < len(pets_list):
            return pets_list[choice]
        else:
            print("Please enter a valid option")
            return None

    except ValueError:
        print("Please enter a valid option")
        return None

def save_pets(pets_list):
    data_to_save = [p.to_dict() for p in pets_list]

    with open("pets_data.json", "w") as f:
        json.dump(data_to_save, f, indent=4)
        print("Pet data saved into pets_data.json!")


def main():
    pets = load_pets()
    print(f"Loaded {len(pets)} pets from database")

    while True:
        choice = display_menu()

        if choice == '1' or choice == '2':
            name = input("Enter pet's name: ")
            age = int(input("Enter pet's age: "))
            weight = float(input("Enter pet's weight(in kg): "))
            breed = input("Enter breed: ")
            temp = input("Enter character (e.g., Playful, Calm): ")

            if choice == '1':
                new_pet = Dog(name, age, weight, breed, temp)
            else:
                new_pet = Cat(name, age, weight, breed, temp)

            pets.append(new_pet)
            print(f"Successfully registered {name}!")

        elif choice == '3':
            print("--- Current Pet Health Profiles --- \n")

            if not pets:
                print("No pets registered!")
            else:
                for p in pets:
                    print(p)
                    print(f" > Status: {p.check_health_status()}")
                    print(f" > Daily Nutrition Goal: {p.calculate_daily_calories():.2f} kcal")
                    print(f" > Care Note: {p.get_health_advice()}")
                    print(f" > Last Checkup: {p.last_checkup}")
                    print(f" > Weight Analysis: {p.get_weight_category()}")
                    print(f" > Vaccination: {p.get_vaccination_status()} \n")

        elif choice == '4':
            chosen_pet = select_pet(pets)
            if chosen_pet:
                note = input(f"What happened with {chosen_pet.name} today? ")
                confirm_msg = chosen_pet.add_log(note)
                print(confirm_msg)

        elif choice == '5':
            chosen_pet = select_pet(pets)
            if chosen_pet:
                print(f"\n--- Health History for {chosen_pet.name} ---")
                history = chosen_pet.get_history()
                print(history)
                print("-----------------")

        elif choice == '6':
            chosen_pet = select_pet(pets)
            if chosen_pet:
                new_date = input("Enter new date: ")
                chosen_pet.last_checkup = new_date
                print(f"Checkup date for {chosen_pet.name} updated!")

        elif choice == '7':
            chosen_pet = select_pet(pets)
            if chosen_pet:
                chosen_pet.is_vaccinated = True
                chosen_pet.add_log("Vaccinated updated to: Fully vaccinated")
                print(f"Great! {chosen_pet.name} is now marked as vaccinated")

        elif choice == '8':
            save_pets(pets)
            print("\n --- Exiting --- \n")
            break

        else:
            print("Please enter a valid option")

if __name__ == "__main__":
    main()
