import sqlite3

def create_employee_table():

    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                per_hour REAL NOT NULL CHECK (per_hour > 0),
                hours INTEGER NOT NULL CHECK (hours >= 0),
                perf_points INTEGER
            )
        ''')

        conn.commit()
        print("Employee table created successfully!")

    except sqlite3.OperationalError as e:
        print("Error creating table:", e)

    finally:
        conn.close()

def create_inventory_table():

    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upc TEXT UNIQUE NOT NULL,
                item_desc TEXT NOT NULL,
                price REAL NOT NULL CHECK (price > 0),
                qoh INTEGER NOT NULL CHECK (qoh >= 0)
            )
        ''')

        conn.commit()
        print("Inventory table created successfully!")

    except sqlite3.OperationalError as e:
        print("Error creating table:", e)

    finally:
        conn.close()

def add_inventory():
    print("========================================")
    print("|             ADD INVENTORY            |")
    print("========================================")
    upc = input("Enter the item's UPC:")
    if upc == "":
        inventory_main()
    item_desc = input("Enter a short description of the item:")
    price = float(input("Enter the item's price: "))  # Convert to float
    qoh = int(input("How many on hand?"))  # Convert to integer
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (upc,item_desc,price,qoh) VALUES (?, ?, ?, ?)",
                   (upc,item_desc,price,qoh))
    conn.commit()
    print("Item added successfully!")
    conn.close()
    add_inventory()

def remove_inventory():
        print("========================================")
        print("|           REMOVE INVENTORY           |")
        print("========================================")
        upc = input("Enter the item's UPC:")
        if upc == "":
            inventory_main()
        conn = sqlite3.connect('smart.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE upc = ?", (upc,))
        conn.commit()
        print("Item removed successfully!")
        conn.close()
        add_inventory()

def order_inventory():
    print("========================================")
    print("|            ORDER INVENTORY           |")
    print("========================================")
    upc = input("Enter the item's UPC:")
    quantity = input("How many to order?: ")
    if upc == "":
        inventory_main()
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET qoh = qoh + ? WHERE upc = ?", (quantity, upc))  # Corrected line
    conn.commit()
    print("Quantity updated successfully!")
    conn.close()
    order_inventory()

def view_inventory():
        search_upc = input("Please enter the UPC: ")
        conn = sqlite3.connect('smart.db')
        cursor = conn.cursor()
        if search_upc == "":
            main()
        if search_upc:
            cursor.execute("SELECT * FROM inventory WHERE upc = ?", (search_upc,))
        else:
            cursor.execute("SELECT * FROM inventory")

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No items found in inventory.")
        else:
            print("===========================================================")
            print("|                     VIEW INVENTORY                      |")
            print("===========================================================")
            print("|  ID  |      UPC      |   Description  |  Price  |  QOH  |")
            print("========================================")
            for row in rows:
                print(f"|  {row[0]:<4} | {row[1]:^14} | {row[2]:^14} | ${row[3]:<5} | {row[4]:<5} |")
            print("========================================")

        conn.close()
        inventory_main()


def inventory_main():
    print("========================================")
    print("|         INVENTORY MANAGEMENT         |")
    print("========================================")
    print("|         1.  Add Inventory            |")
    print("|         2.  Remove Inventory         |")
    print("|         3.  Order Inventory          |")
    print("|         4.  View Inventory           |")
    print("|         5.  Back                     |")
    print("========================================")
    choice = input("Please enter your choice here:  ")
    if choice == "1":
        add_inventory()
    elif choice == "2":
        remove_inventory()
    elif choice == "3":
        order_inventory()
    elif choice == "4":
        view_inventory()
    elif choice == "5":
        main()


def add_person():
    print("========================================")
    print("|              ADD PERSON              |")
    print("========================================")
    first_name = input("Enter the employee's first name:")
    if first_name == "":
        people_main()
    last_name = input("Enter the employee's last name:")
    per_hour = float(input("Enter the hourly wage: "))  # Convert to float
    hours = int(input("How many hours?"))
    perf_points = int(input("How many performance points?"))
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (first_name,last_name,per_hour,hours,perf_points) VALUES (?, ?, ?, ?,?)",
                   (first_name, last_name, per_hour, hours,perf_points))
    conn.commit()
    print("Employee added successfully!")
    conn.close()
    add_person()

def remove_person():
    print("========================================")
    print("|              REMOVE PERSON           |")
    print("========================================")
    id = input("Enter the employee's id:")
    if id == "":
        people_main()
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
    conn.commit()
    print("Employee removed successfully!")
    conn.close()
    people_main()

def edit_person():
    print("========================================")
    print("|             EDIT PERSON             |")
    print("========================================")
    id = input("Enter the employee's ID:")
    first_name = input("Enter the employee's first name:")
    if first_name == "":
        people_main()
    last_name = input("Enter the employee's last name:")
    per_hour = float(input("Enter the hourly wage: "))  # Convert to float
    hours = int(input("How many hours?"))
    perf_points = int(input("How many performance points?"))
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET first_name=?, last_name=?, per_hour=?, hours=?, perf_points=? WHERE id=?",
                   (first_name, last_name, per_hour, hours, perf_points, id,))
    conn.commit()
    print("Employee edited successfully!")
    conn.close()
    people_main()

def coach_person():
    print("========================================")
    print("|             COACH PERSON             |")
    print("========================================")
    id = input("Enter the employee's ID:")
    perf_points = input("How many points (1 - attendance,2 - behavior)?: ")
    if id == "":
        people_main()
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET perf_points = perf_points + ? WHERE id = ?", (perf_points, id))  # Corrected line
    conn.commit()
    print("Points updated successfully!")
    conn.close()
    people_main()

def people_main():
    print("========================================")
    print("|           PEOPLE MANAGEMENT          |")
    print("========================================")
    print("|         1.  Add Person               |")
    print("|         2.  Remove Person            |")
    print("|         3.  Edit Person(DNP)         |")
    print("|         4.  Coach Person             |")
    print("|         5.  Back                     |")
    print("========================================")
    choice = input("Please enter your choice here:  ")
    if choice == "1":
        add_person()
    elif choice == "2":
        remove_person()
    elif choice == "3":
        edit_person()
    elif choice == "4":
        coach_person()
    elif choice == "5":
        main()

def edit_price():
    print("========================================")
    print("|             PRICE CHANGES            |")
    print("========================================")
    upc = input("Enter the item's UPC:")
    price = input("What is the new price?: ")
    if upc == "":
        prices_main()
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET price = ? WHERE upc = ?", (price, upc))  # Corrected line
    conn.commit()
    print("Price updated successfully!")
    conn.close()
    prices_main()

def view_price():
    search_upc = input("Please enter the UPC: ")
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    if search_upc == "":
        main()
    if search_upc:
        cursor.execute("SELECT * FROM inventory WHERE upc = ?", (search_upc,))
    else:
        cursor.execute("SELECT * FROM inventory")

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No items found in inventory.")
    else:
        print("===========================================================")
        print("|                      VIEW PRICING                       |")
        print("===========================================================")
        print("|  ID  |      UPC      |   Description  |  Price  |  QOH  |")
        print("========================================")
        for row in rows:
            print(f"|  {row[0]:<4} | {row[1]:^14} | {row[2]:^14} | ${row[3]:<5} | {row[4]:<5} |")
        print("========================================")

    conn.close()
    prices_main()

def prices_main():
    print("========================================")
    print("|           PRICING MANAGEMENT         |")
    print("========================================")
    print("|         1.  Edit Pricing             |")
    print("|         2.  View Pricing             |")
    print("|         3.  Back                     |")
    print("========================================")
    choice = input("Please enter your choice here:  ")
    if choice == "1":
        edit_price()
    elif choice == "2":
        view_price()
    elif choice == "3":
        main()

def sales_main():
    print("========================================")
    print("|            SALES MANAGEMENT          |")
    print("========================================")
def main():
    print("========================================")
    print("|        SMART SYSTEM INTERFACE        |")
    print("========================================")
    print("|           1.  Inventory              |")
    print("|           2.  People                 |")
    print("|           3.  Prices                 |")
    print("|           4.  Sales                  |")
    print("|           5.  Exit                   |")
    print("========================================")
    print("| IF DB NOT INTITIALIZED, ENSURE TO DO |")
    print("========================================")
    choice = input("Please enter your choice here:  ")
    if choice == "1":
        inventory_main()
    elif choice == "2":
        people_main()
    elif choice == "3":
        prices_main()
    elif choice == "4":
        sales_main()
    elif choice == "5":
        print("Goodbye!")
        quit()
    elif choice == "i":
        create_inventory_table()
        main()
    elif choice == "e":
        create_employee_table()

if __name__ == "__main__":
    main()
