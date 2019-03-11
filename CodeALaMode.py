import sys
import math


# =======================
class Chef:
    def __init__(self, x, y, item):
        self.x = int(x)
        self.y = int(y)
        self.item = item

    def update_info(self, x, y, item):
        self.x = int(x)
        self.y = int(y)
        self.item = item


class Kitchen:
    # .: case de sol
    # D: le lave-vaisselle
    # W: la fenêtre de clients
    # B: la corbeille de myrtilles
    # I: la corbeille de crème glacée

    map = []

    @staticmethod
    def add_line_to_map(line):
        Kitchen.map.append(list(line))

    @staticmethod
    def show_map():
        for line in Kitchen.map:
            print("-".join(str(x) for x in line), file=sys.stderr)

    @staticmethod
    def get_coords(target):
        for index, line in enumerate(Kitchen.map):
            if target in line:
                coords = "%d %d" % (line.index(target), index)
                return coords
        return "COORDS_NOT_FOUND"


class Customer:
    nb_customers = 0
    full_list = []
    waiting_list = []

    def __init__(self, item, award):
        self.item = item  # customer_item: the food the customer is waiting for
        self.award = award  # customer_award: the number of points awarded for delivering the food
        self.id = Customer.nb_customers
        Customer.nb_customers += 1

    @staticmethod
    def show_all_customers():
        for cus in Customer.full_list:
            print("(%d) item:%s / award:%d" % (cus.id, cus.item, cus.award), file=sys.stderr)
            # (1) item:DISH-BLUEBERRIES-ICE_CREAM / award:650

    @staticmethod
    def show_waiting_customers():
        for cus in Customer.waiting_list:
            print("(%d) item:%s / award:%d" % (cus.id, cus.item, cus.award), file=sys.stderr)
            # (1) item:DISH-BLUEBERRIES-ICE_CREAM / award:650


# ============== INIT ============================

num_all_customers = int(input())
for i in range(num_all_customers):
    customer_item, customer_award = input().split()
    customer_award = int(customer_award)
    newCustomer = Customer(customer_item, customer_award)
    Customer.full_list.append(newCustomer)

# Customer.show_all_customers()

for i in range(7):
    Kitchen.add_line_to_map(input())

# Kitchen.show_map()

myChef = Chef(99, 99, "")
partnerChef = Chef(99, 99, "")

# game loop
while True:
    turns_remaining = int(input())

    player_x, player_y, player_item = input().split()
    myChef.update_info(player_x, player_y, player_item)
    partner_x, partner_y, partner_item = input().split()
    partnerChef.update_info(partner_x, partner_x, partner_y)

    num_tables_with_items = int(input())  # the number of tables in the kitchen that currently hold an item
    for i in range(num_tables_with_items):
        table_input = input()
        print("%d: %s" % i, table_input, file=sys.stderr)
        table_x, table_y, item = table_input.split()
        table_x = int(table_x)
        table_y = int(table_y)

    # oven_contents: ignore until wood 1 league
    oven_contents, oven_timer = input().split()
    oven_timer = int(oven_timer)

    num_customers = int(input())  # the number of customers currently waiting for food
    Customer.waiting_list = []
    for i in range(num_customers):
        customer_item, customer_award = input().split()
        customer_award = int(customer_award)
        newCustomer = Customer(customer_item,customer_award)
        Customer.waiting_list.append(newCustomer)

    Customer.show_waiting_customers()

    next_action = "WAIT"

    # ====== LOGIC ==============================

    if myChef.item == "NONE":
        next_action = "USE " + Kitchen.get_coords("D")
    elif myChef.item == "DISH":
        next_action = "USE " + Kitchen.get_coords("I")
    elif myChef.item == "DISH-ICE_CREAM":
        next_action = "USE " + Kitchen.get_coords("B")
    elif myChef.item == "DISH-ICE_CREAM-BLUEBERRIES":
        next_action = "USE " + Kitchen.get_coords("W")



    # ========= ACTION ===========================
    print(next_action)

