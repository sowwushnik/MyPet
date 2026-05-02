from models.pet import Dog,Cat

def display_menu():
    print("\n --- MyPet: Health Tracker --- \n")
    print("1. Register a Dog")
    print("2. Register a Cat")
    print("3. View Registered Pets")
    print("4. Add Health Log")
    print("5. View Health History")
    print("6. Exit \n")
    return input("Select an option: ")

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


def main():
    pets = []

    while True:
        choice = display_menu()

        if choice == '1' or choice == '2':
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            weight = float(input("Enter your weight(in kg): "))
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
                    print(f" > Daily Nutrition Goal: {p.calculate_daily_calories():.2f} kcal \n")

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
            print("\n --- Exiting --- \n")
            break

        else:
            print("Please enter a valid option")

if __name__ == "__main__":
    main()
