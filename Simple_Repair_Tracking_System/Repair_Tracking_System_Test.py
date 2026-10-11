from datetime import datetime
import sqlite3

repairs = []

conn = sqlite3.connect("gadgetfix.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS repairs (
    receipt_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    gadget TEXT,
    problem TEXT,
    cost INTEGER,
    status TEXT,
    date_time TEXT,
    completed_time TEXT
)
""")

conn.commit()

def add_repair():
    print("\n--- ADD REPAIR ---")

    while True:
        name = input("Enter customer name: ").strip()
        if name and name.replace(" ", "").isalpha():
            break
        print("\nInvalid name. Use letters and spaces only. Try again.\n")

    while True:
        gadget = input("Enter gadget brand and model: ").strip()
        if gadget and any(char.isalpha() for char in gadget):
            break
        print("\nInvalid gadget. Enter a valid brand and model. Try again.\n")

    problems = []
    total_cost = 0

    while True:
        print("\n--- REPAIR PROBLEMS ---")
        print("1. Battery replacement")
        print("2. LCD replacement")
        print("3. Screen repair")
        print("4. Other (type manually)")

        while True:
            choice = input("Choose repair problem (1-4): ").strip()

            if choice in ["1", "2", "3", "4"]:
                break

            print("\nInvalid choice. Please choose 1, 2, 3, or 4.\n")

        if choice == "1":
            problem = "Battery replacement"
        elif choice == "2":
            problem = "LCD replacement"
        elif choice == "3":
            problem = "Screen repair"
        else:
            while True:
                problem = input("Enter repair problem: ").strip()

                if problem and any(char.isalpha() for char in problem):
                    break

                print("\nInvalid problem description. Try again.\n")

        while True:
            try:
                cost = int(input("Enter price for this repair: ₱"))

                if cost >= 0:
                    break

                print("\nInvalid cost. Enter zero or a positive number.\n")

            except ValueError:
                print("\nInvalid cost. Please enter a whole number.\n")

        problems.append((problem, cost))
        total_cost += cost

        print("\nRepair added:", problem)
        print("Price: ₱", cost)

        while True:
            another = input("\nAdd another repair problem? (1 = Yes, 2 = No): ").strip()

            if another in ["1", "2"]:
                break

            print("\nInvalid choice. Enter 1 or 2.\n")

        if another == "2":
            break

    status = "Waiting for repair"
    date_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    completed_time = ""

    # Store all repair problems in one text field for now.
    problem_text = "\n".join(
        f"{problem} - ₱{cost}" for problem, cost in problems
    )

    cursor.execute("""
        INSERT INTO repairs
        (name, gadget, problem, cost, status, date_time, completed_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name, gadget, problem_text, total_cost,
        status, date_time, completed_time
    ))

    conn.commit()

    print("\n--- REPAIR SUMMARY ---")
    print("Customer:", name)
    print("Gadget:", gadget)

    for problem, cost in problems:
        print(f"{problem} - ₱{cost}")

    print("Total Cost: ₱", total_cost)
    print("\nRepair recorded successfully!")
    print("Receipt Number:", cursor.lastrowid)

    input("\nPress Enter to continue...")

def view_repairs():
    print("\n--- VIEW REPAIRS ---")

    cursor.execute("SELECT * FROM repairs")
    repair_list = cursor.fetchall()

    if not repair_list:
        print("No repair records found.")
    else:
        for repair in repair_list:
            print("\n------------------------------")
            print("Receipt Number:", repair[0])
            print("Customer:", repair[1])
            print("Gadget:", repair[2])

            print("Repair Problems:")
            print(repair[3])

            print("Total Cost: ₱", repair[4])
            print("Status:", repair[5])
            print("Date & Time Added:", repair[6])

            if repair[7]:
                print("Completed Date & Time:", repair[7])

            print("------------------------------")

    input("\nPress Enter to continue...")

def update_status():
    print("\n--- UPDATE REPAIR STATUS ---")

    cursor.execute("SELECT * FROM repairs")
    repair_list = cursor.fetchall()

    if not repair_list:
        print("No repair records found.")
        input("\nPress Enter to continue...")
        return

    for repair in repair_list:
        print(
            f"\nReceipt No: {repair[0]} | "
            f"Customer: {repair[1]} | "
            f"Gadget: {repair[2]} | "
            f"Status: {repair[5]}"
        )

    while True:
        try:
            receipt_no = int(input("\nEnter receipt number to update: "))

            if receipt_no <= 0:
                print("Receipt number must be greater than zero.")
                continue

            cursor.execute(
                "SELECT * FROM repairs WHERE receipt_no = ?",
                (receipt_no,)
            )
            repair = cursor.fetchone()

            if repair is not None:
                break

            print("Receipt number not found. Please try again.")

        except ValueError:
            print("Invalid input. Enter a whole-number receipt number.")

    while True:
        print("\n1. Waiting for repair")
        print("2. Being repaired")
        print("3. Completed")

        choice = input("Select new status: ").strip()

        if choice == "1":
            new_status = "Waiting for repair"
            break
        elif choice == "2":
            new_status = "Being repaired"
            break
        elif choice == "3":
            new_status = "Completed"
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    if new_status == "Completed":
        completed_time = datetime.now().strftime(
            "%B %d, %Y - %I:%M %p"
        )
    else:
        completed_time = ""

    cursor.execute("""
        UPDATE repairs
        SET status = ?, completed_time = ?
        WHERE receipt_no = ?
    """, (new_status, completed_time, receipt_no))

    conn.commit()

    print("\nRepair status updated successfully!")
    input("\nPress Enter to continue...")

def remove_repair():
    print("\n--- REMOVE REPAIR ---")

    cursor.execute("SELECT * FROM repairs")
    repair_list = cursor.fetchall()

    if not repair_list:
        print("No repair records found.")
        input("\nPress Enter to continue...")
        return

    for repair in repair_list:
        print(
            f"\nReceipt No: {repair[0]} | "
            f"Customer: {repair[1]} | "
            f"Gadget: {repair[2]} | "
            f"Status: {repair[5]}"
        )

    while True:
        try:
            receipt_no = int(
                input("\nEnter receipt number to remove: ")
            )

            if receipt_no <= 0:
                print("Receipt number must be greater than zero.")
                continue

            cursor.execute(
                "SELECT * FROM repairs WHERE receipt_no = ?",
                (receipt_no,)
            )
            repair = cursor.fetchone()

            if repair is None:
                print("Receipt number not found. Please try again.")
                continue
            break

        except ValueError:
            print("Invalid input. Enter a whole-number receipt number.")

    print("\nAre you sure you want to remove this repair?")
    print("1. Yes, remove it")
    print("2. No, cancel")

    while True:
        confirm = input("Enter your choice: ").strip()

        if confirm == "1":
            cursor.execute(
                "DELETE FROM repairs WHERE receipt_no = ?",
                (receipt_no,)
            )
            conn.commit()
            print("\nRepair removed successfully!")
            break

        elif confirm == "2":
            print("\nRemoval cancelled.")
            break

        else:
            print("Invalid choice. Please select 1 or 2.")

    input("\nPress Enter to continue...")

def generate_receipt():
    print("\n--- GENERATE RECEIPT ---")

    cursor.execute("SELECT receipt_no FROM repairs")
    repair_list = cursor.fetchall()

    if not repair_list:
        print("No repair records found.")
        input("\nPress Enter to continue...")
        return

    while True:
        try:
            receipt_no = int(input("Enter receipt number: "))

            if receipt_no <= 0:
                print("Receipt number must be greater than zero.")
                continue

            cursor.execute(
                "SELECT * FROM repairs WHERE receipt_no = ?",
                (receipt_no,)
            )
            repair = cursor.fetchone()

            if repair is not None:
                break

            print("Receipt number not found. Please try again.")

        except ValueError:
            print("Invalid input. Enter a whole-number receipt number.")

    print("\n========== GADGETFIX RECEIPT ==========")
    print("Receipt Number:", repair[0])
    print("Customer Name:", repair[1])
    print("Gadget:", repair[2])
    print("---------------------------------------")
    print("Repair Problems:")
    print(repair[3])
    print("---------------------------------------")
    print("Total Repair Cost: ₱", repair[4])
    print("Status:", repair[5])
    print("Date & Time Added:", repair[6])

    if repair[7]:
        print("Completed Date & Time:", repair[7])

    print("=======================================")
    input("\nPress Enter to continue...")

while True:
    print("\n============================")
    print("     GADGET REPAIR SHOP")
    print("============================")
    print("[1] Add Repair")
    print("[2] View Repairs")
    print("[3] Update Repair Status")
    print("[4] Generate Receipt")
    print("[5] Remove Repair")
    print("[6] Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_repair()

    elif choice == "2":
        view_repairs()

    elif choice == "3":
        update_status()

    elif choice == "4":
        generate_receipt()

    elif choice == "5":

        remove_repair()
    elif choice == "6":
        print("\nThank you for using GadgetFix!")
        break
    else:
        print("\nInvalid choice. Please try again.")