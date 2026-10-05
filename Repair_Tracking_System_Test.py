from datetime import datetime

repairs = []


def add_repair():
    print("\n--- ADD REPAIR ---")

    name = input("Customer name: ")
    gadget = input("Gadget type: ")
    problem = input("Device problem: ")

    while True:
        try:
            cost = int(input("Repair cost: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    status = "Waiting for repair"

    date_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")

    repair = [name, gadget, problem, cost, status, date_time, ""]
    repairs.append(repair)

    print("\nRepair recorded successfully!")

    input("\nPress Enter to go back...")


def view_repairs(repair_list):
    print("\n--- VIEW REPAIRS ---")

    if len(repair_list) == 0:
        print("No repair records found.")

    else:
        for i, repair in enumerate(repair_list, 1):
            print("\nRepair #", i)
            print("Customer:", repair[0])
            print("Gadget:", repair[1])
            print("Problem:", repair[2])
            print("Cost: ₱", repair[3])
            print("Status:", repair[4])
            print("Date & Time Added:", repair[5])

            if repair[4] == "Completed":
                print("Completed Date & Time:", repair[6])

        input("\nPress Enter to go back...")

        return repair_list


def update_status():
    print("\n--- UPDATE REPAIR STATUS ---")

    if len(repairs) == 0:
        print("No repair records found.")
        input("\nPress Enter to go back...")
        return

    else:
        for i, repair in enumerate(repairs, 1):
            print(i, "-", repair[0], "-", repair[1], "-", repair[4])

    while True:
        try:
            number = int(input("Enter repair number: "))

            if 1 <= number <= len(repairs):
                break
            else:
                print("Invalid repair number.")

        except ValueError:
            print("Please enter a valid number.")

    print("\n[1] Waiting for repair")
    print("[2] Being repaired")
    print("[3] Completed")

    while True:
        status_choice = input("Enter new status: ")

        if status_choice == "1":
            repairs[number - 1][4] = "Waiting for repair"
            break

        elif status_choice == "2":
            repairs[number - 1][4] = "Being repaired"
            break

        elif status_choice == "3":
            repairs[number - 1][4] = "Completed"
            repairs[number - 1][6] = datetime.now().strftime(
                "%B %d, %Y - %I:%M %p"
            )
            break

        else:
            print("Invalid status choice.")

    print("\nRepair status updated successfully!")
    print("\n--- UPDATED REPAIR ---")
    print("Customer:", repairs[number - 1][0])
    print("Gadget:", repairs[number - 1][1])
    print("Problem:", repairs[number - 1][2])
    print("Cost: ₱", repairs[number - 1][3])
    print("Status:", repairs[number - 1][4])
    print("Date & Time Added:", repairs[number - 1][5])

    if repairs[number - 1][4] == "Completed":
        print("Completed Date & Time:", repairs[number - 1][6])

    input("\nPress Enter to go back...")


def generate_receipt():
    print("\n--- GENERATE RECEIPT ---")

    if len(repairs) == 0:
        print("No repair records found.")
        input("\nPress Enter to go back...")
        return

    for i, repair in enumerate(repairs, 1):
        print(i, "-", repair[0], "-", repair[1], "-", repair[4])

    while True:
        try:
            number = int(input("\nEnter repair number: "))

            if 1 <= number <= len(repairs):
                break
            else:
                print("Invalid repair number.")

        except ValueError:
            print("Please enter a valid number.")

    repair = repairs[number - 1]

    print("\n================================")
    print("       GADGET REPAIR SHOP")
    print("          REPAIR RECEIPT")
    print("================================")
    print("Customer:", repair[0])
    print("Gadget:", repair[1])
    print("Problem:", repair[2])
    print("Repair Cost: ₱", repair[3])
    print("Status:", repair[4])
    print("Date & Time Added:", repair[5])

    if repair[4] == "Completed":
        print("Completed Date & Time:", repair[6])

    print("================================")
    print("Thank you for choosing us!")
    print("================================")

    input("\nPress Enter to go back...")


while True:
    print("\n============================")
    print("     GADGET REPAIR SHOP")
    print("============================")
    print("[1] Add Repair")
    print("[2] View Repairs")
    print("[3] Update Repair Status")
    print("[4] Generate Receipt")
    print("[5] Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_repair()

    elif choice == "2":
        view_repairs(repairs)

    elif choice == "3":
        update_status()

    elif choice == "4":
        generate_receipt()

    elif choice == "5":
        print("\nThank you for using GadgetFix!")
        break

    else:
        print("\nInvalid choice. Please try again.")