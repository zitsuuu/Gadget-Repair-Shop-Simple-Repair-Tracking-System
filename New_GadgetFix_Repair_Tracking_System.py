from datetime import datetime

accounts = []
repairs = []
next_receipt_no = 1

# Default staff account
accounts.append({
    "full_name": "GadgetFix Staff",
    "username": "admin",
    "password": "admin123",
    "role": "Staff"
})

STATUSES = [
    "Waiting for repair",
    "Being repaired",
    "Completed"
]

def pause():
    input("\nPress Enter to continue...")

def find_account(username):
    for account in accounts:
        if account["username"].lower() == username.lower():
            return account
    return None

def register_customer():
    print("\n--- CUSTOMER REGISTRATION ---")

    while True:
        full_name = input("Enter your full name: ").strip()

        if full_name and all(
            part.isalpha() for part in full_name.split()
        ):
            break

        print("Invalid name. Use letters and spaces only.")

    while True:
        username = input("Create a username: ").strip()

        if not username:
            print("Username cannot be empty.")
        elif find_account(username):
            print("Username already exists. Choose another.")
        else:
            break

    while True:
        password = input("Create a password: ")

        if password.strip():
            break

        print("Password cannot be empty.")

    accounts.append({
        "full_name": full_name,
        "username": username,
        "password": password,
        "role": "Customer"
    })

    print("\nRegistration successful!")
    print("You can now log in.")

    pause()

def login():
    print("\n--- GADGETFIX LOGIN ---")

    username = input("Username: ").strip()
    password = input("Password: ")

    account = find_account(username)

    if account and account["password"] == password:
        if account["username"] == "admin" and account["role"] == "Staff":
            print("\nWelcome, Staff!")
            staff_menu()
        elif account["role"] == "Customer":
            print(f"\nWelcome, {account['full_name']}!")
            customer_menu(account)
        else:
            print("\nInvalid account.")
            pause()
    else:
        print("\nInvalid username or password.")
        pause()

def add_repair():
    global next_receipt_no

    print("\n--- ADD REPAIR ---")

    customers = [
        account for account in accounts
        if account["role"] == "Customer"
    ]

    if not customers:
        print("No registered customers found.")
        print("Ask a customer to register first.")
        pause()
        return

    print("\n--- REGISTERED CUSTOMERS ---")

    for index, customer in enumerate(customers, start=1):
        print(
            f"[{index}] {customer['full_name']} "
            f"(@{customer['username']})"
        )

    while True:
        try:
            choice = int(input("Choose customer number: "))

            if 1 <= choice <= len(customers):
                customer = customers[choice - 1]
                break

            print("Invalid customer number.")

        except ValueError:
            print("Enter a whole number.")

    while True:
        gadget = input(
            "Enter gadget brand and model: "
        ).strip()

        if gadget and any(char.isalpha() for char in gadget):
            break

        print("Invalid gadget. Enter a valid brand and model.")

    problems = []
    total_cost = 0

    while True:
        print("\n--- REPAIR PROBLEMS ---")
        print("1. Battery replacement")
        print("2. LCD replacement")
        print("3. Screen repair")
        print("4. Other (type manually)")

        choice = input(
            "Choose repair problem (1-4): "
        ).strip()

        if choice == "1":
            problem = "Battery replacement"

        elif choice == "2":
            problem = "LCD replacement"

        elif choice == "3":
            problem = "Screen repair"

        elif choice == "4":
            while True:
                problem = input(
                    "Enter repair problem: "
                ).strip()

                if problem and any(
                    char.isalpha() for char in problem
                ):
                    break

                print("Invalid problem description.")

        else:
            print("Invalid choice. Choose 1, 2, 3, or 4.")
            continue

        while True:
            try:
                cost = int(
                    input("Enter price for this repair: ₱")
                )

                if cost >= 0:
                    break

                print("Enter zero or a positive number.")

            except ValueError:
                print("Enter a whole-number cost.")

        problems.append((problem, cost))
        total_cost += cost

        print("\nRepair added:", problem)
        print("Price: ₱", cost)

        while True:
            another = input(
                "\nAdd another repair problem? "
                "(1 = Yes, 2 = No): "
            ).strip()

            if another in ["1", "2"]:
                break

            print("Enter 1 or 2.")

        if another == "2":
            break

    problem_text = "\n".join(
        f"{problem} - ₱{cost}"
        for problem, cost in problems
    )

    date_time = datetime.now().strftime(
        "%B %d, %Y - %I:%M %p"
    )

    repair = {
        "receipt_no": next_receipt_no,
        "customer_username": customer["username"],
        "name": customer["full_name"],
        "gadget": gadget,
        "problem": problem_text,
        "cost": total_cost,
        "status": "Waiting for repair",
        "date_time": date_time,
        "completed_time": ""
    }

    repairs.append(repair)

    print("\n--- REPAIR SUMMARY ---")
    print("Customer:", customer["full_name"])
    print("Gadget:", gadget)

    for problem, cost in problems:
        print(f"{problem} - ₱{cost}")

    print("Total Cost: ₱", total_cost)
    print("\nRepair recorded successfully!")
    print("Receipt Number:", next_receipt_no)

    next_receipt_no += 1

    pause()

def print_repair_list(repair_list):
    if not repair_list:
        print("No repair records found.")
        return

    for repair in repair_list:
        print("\n------------------------------")
        print("Receipt Number:", repair["receipt_no"])
        print("Customer:", repair["name"])
        print("Gadget:", repair["gadget"])
        print("Repair Problems:")
        print(repair["problem"])
        print("Total Cost: ₱", repair["cost"])
        print("Status:", repair["status"])
        print("Date & Time Added:", repair["date_time"])

        if repair["completed_time"]:
            print(
                "Completed Date & Time:",
                repair["completed_time"]
            )

        print("------------------------------")

def view_repairs():
    print("\n--- VIEW ALL REPAIRS ---")

    if not repairs:
        print("No repair records found.")
        pause()
        return

    page_size = 10
    page = 0

    while True:
        total_pages = (len(repairs) + page_size - 1) // page_size
        start_index = page * page_size
        page_repairs = repairs[start_index:start_index + page_size]

        print(f"\nPage {page + 1} of {total_pages} | Total repairs: {len(repairs)}")
        headers = [
            ("Receipt No.", 12), ("Customer", 22),
            ("Gadget", 20), ("Status", 22)
        ]
        line = "+" + "+".join("-" * (width + 2) for _, width in headers) + "+"
        print(line)
        print("|" + "|".join(
            f" {title:<{width}} " for title, width in headers
        ) + "|")
        print(line)

        for repair in page_repairs:
            values = [
                repair["receipt_no"],
                repair["name"],
                repair["gadget"],
                repair["status"]
            ]
            print("|" + "|".join(
                f" {str(value)[:width]:<{width}} "
                for value, (_, width) in zip(values, headers)
            ) + "|")

        print(line)
        print("Enter a receipt number to view full details.")
        print("N = Next page | P = Previous page | Q = Back to staff menu")
        choice = input("Choose an option: ").strip().lower()

        if choice == "n":
            if start_index + page_size < len(repairs):
                page += 1
            else:
                print("You are already on the last page.")
        elif choice == "p":
            if page > 0:
                page -= 1
            else:
                print("You are already on the first page.")
        elif choice == "q":
            break
        else:
            try:
                receipt_no = int(choice)
                repair = find_repair_by_receipt(receipt_no)

                # Only allow selecting a receipt visible on the current page.
                if repair is None or repair not in page_repairs:
                    print("\nThat receipt number is not on this page.")
                    continue

                print("\n========== FULL REPAIR INFORMATION ==========")
                print("Receipt Number:", repair["receipt_no"])
                print("Customer:", repair["name"])
                print("Gadget:", repair["gadget"])
                print("\nRepair Problems:")
                print(repair["problem"])
                print("Total Cost: ₱", repair["cost"])
                print("Status:", repair["status"])
                print("Date & Time Added:", repair["date_time"])

                if repair["completed_time"]:
                    print("Completed Date & Time:", repair["completed_time"])

                print("=============================================")
                pause()
            except ValueError:
                print("Invalid choice. Enter a receipt number, N, P, or Q.")

def customer_view_repairs(account):
    print("\n--- MY REPAIR RECORDS ---")

    my_repairs = [
        repair for repair in repairs
        if repair["customer_username"].lower()
        == account["username"].lower()
    ]

    print_repair_list(my_repairs)

    pause()

def find_repair_by_receipt(receipt_no):
    for repair in repairs:
        if repair["receipt_no"] == receipt_no:
            return repair

    return None

def choose_repair(prompt):
    if not repairs:
        print("No repair records found.")
        return None

    for repair in repairs:
        print(
            f"\nReceipt No: {repair['receipt_no']} | "
            f"Customer: {repair['name']} | "
            f"Gadget: {repair['gadget']} | "
            f"Status: {repair['status']}"
        )

    while True:
        try:
            receipt_no = int(input(prompt))

            if receipt_no <= 0:
                print("Receipt number must be greater than zero.")
                continue

            repair = find_repair_by_receipt(receipt_no)

            if repair is not None:
                return repair

            print("Receipt number not found. Try again.")

        except ValueError:
            print("Enter a whole-number receipt number.")

def update_status():
    print("\n--- UPDATE REPAIR STATUS ---")

    repair = choose_repair(
        "Enter receipt number to update: "
    )

    if repair is None:
        pause()
        return

    print("\n1. Waiting for repair")
    print("2. Being repaired")
    print("3. Completed")

    while True:
        choice = input("Select new status: ").strip()

        if choice in ["1", "2", "3"]:
            repair["status"] = STATUSES[int(choice) - 1]
            break

        print("Invalid choice. Select 1, 2, or 3.")

    if repair["status"] == "Completed":
        repair["completed_time"] = datetime.now().strftime(
            "%B %d, %Y - %I:%M %p"
        )

    else:
        repair["completed_time"] = ""

    print("\nRepair status updated successfully!")

    pause()

def generate_receipt(repair=None):
    print("\n--- GENERATE RECEIPT ---")

    if repair is None:
        repair = choose_repair("Enter receipt number: ")

    if repair is None:
        pause()
        return

    print("\n========== GADGETFIX RECEIPT ==========")
    print("Receipt Number:", repair["receipt_no"])
    print("Customer Name:", repair["name"])
    print("Gadget:", repair["gadget"])
    print("---------------------------------------")
    print("Repair Problems:")
    print(repair["problem"])
    print("---------------------------------------")
    print("Total Repair Cost: ₱", repair["cost"])
    print("Status:", repair["status"])
    print("Date & Time Added:", repair["date_time"])

    if repair["completed_time"]:
        print(
            "Completed Date & Time:",
            repair["completed_time"]
        )

    print("=======================================")

    pause()

def customer_receipt(account):
    print("\n--- VIEW MY RECEIPT ---")

    my_repairs = [
        repair for repair in repairs
        if repair["customer_username"].lower()
        == account["username"].lower()
    ]

    if not my_repairs:
        print("You have no repair records yet.")
        pause()
        return

    for repair in my_repairs:
        print(
            f"Receipt No: {repair['receipt_no']} | "
            f"Gadget: {repair['gadget']} | "
            f"Status: {repair['status']}"
        )

    while True:
        try:
            receipt_no = int(
                input("Enter your receipt number: ")
            )

            repair = find_repair_by_receipt(receipt_no)

            if (
                repair is not None
                and repair["customer_username"].lower()
                == account["username"].lower()
            ):
                generate_receipt(repair)
                return

            print(
                "That receipt was not found under your account."
            )

        except ValueError:
            print("Enter a whole-number receipt number.")

def remove_repair():
    print("\n--- REMOVE REPAIR ---")

    repair = choose_repair(
        "Enter receipt number to remove: "
    )

    if repair is None:
        pause()
        return

    print("\nAre you sure you want to remove this repair?")
    print("1. Yes, remove it")
    print("2. No, cancel")

    while True:
        confirm = input("Enter your choice: ").strip()

        if confirm == "1":
            repairs.remove(repair)
            print("\nRepair removed successfully!")
            break

        elif confirm == "2":
            print("\nRemoval cancelled.")
            break

        else:
            print("Select 1 or 2.")

    pause()

def customer_menu(account):
    while True:
        print("\n============================")
        print("       CUSTOMER MENU")
        print("============================")
        print("[1] View My Repair Records")
        print("[2] View My Receipt")
        print("[3] Log Out")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            customer_view_repairs(account)

        elif choice == "2":
            customer_receipt(account)

        elif choice == "3":
            print("Logged out.")
            break

        else:
            print("Invalid choice. Please try again.")

def staff_menu():
    while True:
        print("\n============================")
        print("         STAFF MENU")
        print("============================")
        print("[1] Add Repair")
        print("[2] View All Repairs")
        print("[3] Update Repair Status")
        print("[4] Generate Receipt")
        print("[5] Remove Repair")
        print("[6] Log Out")

        choice = input("Enter your choice: ").strip()

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
            print("Staff logged out.")
            break

        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("\n============================")
        print("          GADGETFIX")
        print("============================")
        print("[1] Register Customer")
        print("[2] Login")
        print("[3] Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_customer()

        elif choice == "2":
            login()

        elif choice == "3":
            print("\nThank you for using GadgetFix!")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
