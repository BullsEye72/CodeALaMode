import sys
import math


def print_err(string):
    print(string, file=sys.stderr)


# =======================
class Chef:
    def __init__(self, name, x, y, item):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.item = item.split("-")

    def update_info(self, x, y, item):
        self.x = int(x)
        self.y = int(y)
        self.item = item.split("-")

    def show_items(self):
        print_err(self.name + " : " + " & ".join(self.item))

    def chop_item(self, item):
        if item == "CHOPPED_STRAWBERRIES":
            if "STRAWBERRIES" not in self.item:
                return "USE " + Kitchen.get_coords("S")
            else:

                if self.is_around("C") == False:
                   is_near_board = False
                else:
                    is_near_board = True

                if "NONE" not in self.item:
                    if not is_near_board:
                        return "MOVE " + Kitchen.get_coords("C")
                    else:
                        return "USE " + self.is_around("#")

    def is_around(self, target):
        for iy in range(-1, 1):
            for ix in range(-1, 1):
                look_x = self.x + ix
                look_y = self.y + iy
                if Kitchen.map[look_y][look_x] == target:
                    return "%d %d" % (look_x, look_y)

        return False

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
            print_err("-".join(str(x) for x in line))

    @staticmethod
    def get_coords(target):
        for index, line in enumerate(Kitchen.map):
            if target in line:
                coords = "%d %d" % (line.index(target), index)
                return coords
        return "COORDS_NOT_FOUND"

    @staticmethod
    def get_initial(item):
        if item == "DISH":
            return "D"
        if item == "ICE_CREAM":
            return "I"
        if item == "BLUEBERRIES":
            return "B"
        if item == "STRAWBERRIES":
            return "S"
        if item == "CHOPPING_BOARD":
            return "C"
        if item == "CHOPPED_STRAWBERRIES":
            return None

class Customer:
    nb_customers = 0
    full_list = []
    waiting_list = []

    def __init__(self, item, award):
        self.item = item.split("-")  # customer_item: the food the customer is waiting for
        self.award = award  # customer_award: the number of points awarded for delivering the food
        self.id = Customer.nb_customers
        Customer.nb_customers += 1

    @staticmethod
    def show_all_customers():
        for cus in Customer.full_list:
            print_err("(%d) item:%s / award:%d" % (cus.id, "-".join(cus.item), cus.award))
            # (1) item:DISH-BLUEBERRIES-ICE_CREAM / award:650

    @staticmethod
    def show_waiting_customers():
        for cus in Customer.waiting_list:
            print_err("(%d) item:%s / award:%d" % (cus.id, "-".join(cus.item), cus.award))
            # (1) item:DISH-BLUEBERRIES-ICE_CREAM / award:650


class TableItem:
    list = []

    def __init__(self, x, y, item):
        self.x = int(x)
        self.y = int(y)
        self.item = item

    @staticmethod
    def show_all_items():
        for i, it in enumerate(TableItem.list):
            print_err("%d - %s %s %s" % (i, it.x, it.y, it.item))

    def item_is_ordered(self, customers):
        coords = None

        for cus in customers:
            if cus.item[1] in self.item and cus.item[2] in self.item:
                coords = "%d %d" % (self.x, self.y)
                return coords


# ============== INIT ============================

show_waiting = False
show_table_items = False


num_all_customers = int(input())
for i in range(num_all_customers):
    customer_item, customer_award = input().split()
    customer_award = int(customer_award)
    newCustomer = Customer(customer_item, customer_award)
    Customer.full_list.append(newCustomer)

# Customer.show_all_customers()

for i in range(7):
    Kitchen.add_line_to_map(input())

Kitchen.show_map()

myChef = Chef("My Chef", 99, 99, "")
partnerChef = Chef("My Partner", 99, 99, "")

# game loop
while True:
    turns_remaining = int(input())

    player_x, player_y, player_item = input().split()
    myChef.update_info(player_x, player_y, player_item)
    partner_x, partner_y, partner_item = input().split()
    partnerChef.update_info(partner_x, partner_x, partner_y)

    num_tables_with_items = int(input())  # the number of tables in the kitchen that currently hold an item
    TableItem.list = []
    for i in range(num_tables_with_items):
        table_x, table_y, item = input().split()
        newItem = TableItem(table_x, table_y, item)
        TableItem.list.append(newItem)

    if show_table_items:
        print_err("Items:")
        TableItem.show_all_items()

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

    if show_waiting:
        print_err("Waiting:")
        Customer.show_waiting_customers()

    next_action = "WAIT"

    # ====== LOGIC ==============================

    myChef.show_items()

    can_steal = False
    for ti in TableItem.list:
        # print_err(ti.item_is_ordered(Customer.waiting_list))
        get_stealable_coord = ti.item_is_ordered(Customer.waiting_list)
        if get_stealable_coord != None:
            next_action = "USE " + get_stealable_coord
            can_steal = True

    if not can_steal or "NONE" not in myChef.item:

        if "NONE" in myChef.item:
            next_action = "USE " + Kitchen.get_coords("D")
        else:
            for cus_item in Customer.waiting_list[2].item:
                print_err("2:"+cus_item)
                if cus_item not in myChef.item:
                    if "CHOPPED" in cus_item.split("_"):
                        next_action = myChef.chop_item(cus_item)
                        print_err("3_chop:" + next_action)
                    else:
                        print_err("3:" + Kitchen.get_coords(Kitchen.get_initial(cus_item[0])))
                        next_action = "USE " + Kitchen.get_coords(Kitchen.get_initial(cus_item[0]))

    else:
        if "NONE" in myChef.item:
            pass
        else:
            next_action = "USE " + Kitchen.get_coords("W")



    # ========= ACTION ===========================
    print(next_action)

