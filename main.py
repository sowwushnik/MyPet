from models.pet import Dog,Cat

def display_menu():
    print("\n --- MyPet: Health Tracker --- \n")
    print("1. Register a Dog")
    print("2. Register a Cat")
    print("3. View Registered Pets")
    print("4. Exit")
    return input("Select an option: ")

def main():
    pets = []

    while True:
        choice = display_menu()

        if choice == '1' or choice == '2':
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            weight = float(input("Enter your weight(in kg): "))

            if choice == '1':
                new_pet = Dog(name,age,weight)
            else:
                new_pet = Cat(name,age,weight)

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
            print("--- Exiting --- \n")
            break

        else:
            print("Please enter a valid option")

if __name__ == "__main__":
    main()
