from simple_term_menu import TerminalMenu
import os
import uuid


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu(options):
    shop_menu = TerminalMenu(options)
    option = shop_menu.show()
    return option


class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.item_id = str(uuid.uuid4())

    def update_price(self, price: float):
        self.price = price


class CountedItem:
    def __init__(self, item: Item, stock: int):
        self.item = item
        self.stock = stock


class StockList:
    def __init__(self):
        self.items: list[CountedItem] = []

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def get_by_id(self, item_id: str):
        for index, counted_item in enumerate(self.items):
            if counted_item.item.item_id == item_id:
                return index
        return None

    def update_stock(self, index: int, stock: int):
        self.items[index].stock = stock

    def remove_item(self, index: int):
        self.items.pop(index)

    def add_item(self, counted_item: CountedItem):
        self.items.append(counted_item)


items = StockList()
items.add_item(CountedItem(Item("Test item", 50), 10))
items.add_item(CountedItem(Item("Blue t-shirt", 15), 25))
items.add_item(CountedItem(Item("Water bottle", 10), 12))

cart: list[CountedItem] = []

sales_summary = {
    "total_items": 0,
    "total_revenue": 0.0,
    "sold": {},
}


def format_price(value: float):
    return f"${value:.2f}"


def shop():
    clear_console()
    print("Shop")
    while True:
        if len(items) == 0:
            print("No items to show!")

        display_items = []
        for item in items:
            in_cart = cart.count(item)
            label = f"{item.item.name} - {format_price(item.item.price)}"
            if item.stock == 0:
                label += " (Out of stock)"
            else:
                label += f" (In cart: {in_cart}/{item.stock})"
            display_items.append(label)

        display_items.append("View Cart")
        display_items.append("Exit Shop")
        option = show_menu(display_items)

        if option == len(display_items) - 2:
            manage_cart()
            clear_console()
            print("Shop")
            continue

        if option == len(display_items) - 1:
            return

        selected_item = items[option]
        if selected_item.stock <= cart.count(selected_item):
            input("No more stock available for that item!")
            continue

        cart.append(selected_item)


def get_grouped_cart_items():
    grouped_items: list[CountedItem] = []
    for item in cart:
        if item not in grouped_items:
            grouped_items.append(item)
    return grouped_items


def manage_cart():
    clear_console()
    print("Cart Manager")
    while True:
        grouped_items = get_grouped_cart_items()

        cart_items = []
        for item in grouped_items:
            count = cart.count(item)
            cart_items.append(f"{item.item.name} (Quantity {count})")
        cart_items.append("Exit Cart Manager")

        option = show_menu(cart_items)

        if option == len(cart_items) - 1:
            return

        manage_cart_item(grouped_items[option])
        clear_console()
        print("Cart Manager")


def manage_cart_item(item: CountedItem):
    while True:
        clear_console()
        quantity = cart.count(item)
        print(item.item.name)
        print(f"Quantity: {quantity}")

        item_options = ["Set Quantity", "Remove item", "Exit"]
        option = show_menu(item_options)

        match option:
            case 0:
                try:
                    new_quantity = int(input("Enter the new quantity for the item: "))
                except ValueError:
                    input("Quantity must be a number!")
                    continue

                if new_quantity <= 0:
                    input("Quantity must be larger than zero!")
                    continue

                if new_quantity > item.stock:
                    input("Quantity exceeds items in stock!")
                    continue

                while quantity < new_quantity:
                    cart.append(item)
                    quantity += 1

                while quantity > new_quantity:
                    cart.remove(item)
                    quantity -= 1

            case 1:
                for _ in range(quantity):
                    cart.remove(item)
                return

            case 2:
                return


def checkout():
    global cart

    clear_console()
    print("Checkout")
    subtotal = 0
    for item in cart:
        subtotal += item.item.price
        print(f"{format_price(item.item.price)} - {item.item.name}")
        item.stock -= 1
        sales_summary["total_items"] += 1
        sales_summary["total_revenue"] += item.item.price

        sold_item = sales_summary["sold"].setdefault( #Setting defualt values for sold item if it doesn't exist, then returning it
            item.item.item_id,
            {"name": item.item.name, "quantity": 0, "revenue": 0.0},
        )
        sold_item["quantity"] += 1
        sold_item["revenue"] += item.item.price

    tax = subtotal * 0.08
    total = subtotal + tax

    cart = []

    print(f"\nSubtotal: {format_price(subtotal)}")
    print(f"Tax: {format_price(tax)}")
    print(f"Total: {format_price(total)}")

    input("\nPress Enter to return to the main menu.")


def view_sales_summary():
    clear_console()
    print("Sales Summary")
    print(f"Total items sold: {sales_summary['total_items']}")
    print(f"Total revenue: {format_price(sales_summary['total_revenue'])}")

    if len(sales_summary["sold"]) == 0:
        print("No sales yet.")
    else:
        for sold in sales_summary["sold"].values():
            print(f"{sold['name']}: {sold['quantity']} sold, {format_price(sold['revenue'])}")

    input("\nPress Enter to return to the Manager menu.")


def manage_stock():
    while True:
        clear_console()
        print("Manage Stock")

        stock_options = []
        for item in items:
            stock_options.append(f"{item.item.name} - {item.stock} in stock")
        stock_options.append("Exit Stock Manager")

        option = show_menu(stock_options)
        if option == len(stock_options) - 1:
            return

        update_stock_item(option)


def update_stock_item(index: int):
    counted_item = items[index]
    clear_console()
    print(f"Update stock for {counted_item.item.name}")
    print(f"Current stock: {counted_item.stock}")

    try:
        new_stock = int(input("Enter new stock quantity: "))
    except ValueError:
        input("Stock must be a whole number!")
        return

    if new_stock < 0:
        input("Stock cannot be negative!")
        return

    items.update_stock(index, new_stock)
    input("Stock updated.")


def add_item():
    clear_console()
    print("Add New Item")

    name = input("Enter item name: ").strip()
    if name == "":
        input("Item name cannot be blank!")
        return

    try:
        price = float(input("Enter item price: "))
    except ValueError:
        input("Price must be a number!")
        return

    if price < 0:
        input("Price cannot be negative!")
        return

    try:
        stock = int(input("Enter item stock quantity: "))
    except ValueError:
        input("Stock must be a whole number!")
        return

    if stock < 0:
        input("Stock cannot be negative!")
        return

    items.add_item(CountedItem(Item(name, price), stock))
    input("Item added to inventory.")


def manager():
    clear_console()
    print("Manager")
    username = input("Username: ")
    password = input("Password: ")
    if username != "admin" or password != "1234":
        input("Invalid credentials!")
        return

    options = ["Sales Summary", "Manage Stock", "Add Item", "Exit"]

    while True:
        clear_console()
        print("Manager")
        option = show_menu(options)

        match option:
            case 0:
                view_sales_summary()
            case 1:
                manage_stock()
            case 2:
                add_item()

        if option == len(options) - 1:
            return

while True:
    clear_console()
    print("Task 3 - Store Management System")
    options = ["Shop", "Checkout", "Manager", "Exit"]
    option = show_menu(options)

    match option:
        case 0:
            shop()
        case 1:
            checkout()
        case 2:
            manager()
        case 3:
            clear_console()
            break