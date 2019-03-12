import sys
import math

CHOPPED_STRAWBERRIES = "CHOPPED_STRAWBERRIES"
STRAWBERRIES = "STRAWBERRIES"
NONE = "NONE"
BLUEBERRIES = "BLUEBERRIES"
DISH = "DISH"
ICE_CREAM = "ICE_CREAM"
CHOPPING_BOARD = "CHOPPING_BOARD"


def print_err(string):
    print(string, file=sys.stderr)


# =======================
class Chef:
    def __init__(self, name, x, y, item):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.item = item.split("-")
        self.is_chopping = False
        self.chopped_item = "EMPTY"
        self.last_dish_coords = "EMPTY"
        self.chopping_state = "EMPTY"

    def update_info(self, x, y, item):
        self.x = int(x)
        self.y = int(y)
        self.item = item.split("-")

    def show_items(self):
        print_err(self.name + " : " + " & ".join(self.item))

    def is_around_coords(self, x, y):
        x = int(x)
        y = int(y)
        if x >= self.x-1 and x <= self.x+1:
            if y >= self.y-1 and y <= self.y+1:
                return True
        return False

    def chop_item(self, item):
        if item == CHOPPED_STRAWBERRIES:
            '''
            1) poser son assiettes pres de la planche
            2) prendre des fraises
            3) couper les fraises
            4) poser sur l'assiette
            5) prendre l'assiette
            '''

            return_action = "ERROR IN CHOP_ITEM"
            print_err("Choppin State = " + self.chopping_state)

            if self.chopping_state == "SEARCH_CHOPPED":
                found_chopped = False
                for it in TableItem.list:
                    if it.item == CHOPPED_STRAWBERRIES:
                        found_chopped = True
                        return_action = "USE %d %d" % (it.x, it.y)
                        if self.is_around_coords(it.x, it.y):
                            self.is_chopping = False
                            self.chopping_state = "EMPTY"
                if self.is_chopping and not found_chopped:
                    if self.is_around("C") != False:
                        self.chopping_state = "SEARCH_BOARD"
                    else:
                        self.chopping_state = "DROP_DISH"

            if self.chopping_state == "SEARCH_BOARD":
                return_action = "MOVE " + Kitchen.get_coords("C")

                if self.is_around("C") != False:
                    self.chopping_state = "DROP_DISH"

            if self.chopping_state == "DROP_DISH":
                    free_table_coords = self.is_around("#")
                    self.last_dish_coords = free_table_coords
                    return_action = "USE " + free_table_coords
                    if NONE in self.item:
                        self.chopping_state = "SEARCH_ITEM"

            if self.chopping_state == "SEARCH_ITEM":
                if STRAWBERRIES not in self.item:
                    return_action =  "USE " + Kitchen.get_coords("S")
                else:
                    self.chopping_state = "CHOP_ITEM"

            if self.chopping_state == "CHOP_ITEM":
                if CHOPPED_STRAWBERRIES not in self.item:
                    return_action = "USE " + Kitchen.get_coords("C")
                else:
                    self.chopping_state = "USE_DISH"

            if self.chopping_state == "USE_DISH":
                last_coords = self.last_dish_coords
                #x, y = last_coords.split(" ")

                if DISH not in self.item:
                    return_action = "USE " + last_coords
                else:
                    last_coords = "EMPTY"
                    self.is_chopping = False
                    return_action = "WAIT"

            print_err("Choppin State = " + self.chopping_state)
            return return_action

    def is_around(self, target):
        for iy in range(-1, 2):
            for ix in range(-1, 2):
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
        if item == DISH:
            return "D"
        if item == ICE_CREAM:
            return "I"
        if item == BLUEBERRIES:
            return "B"
        if item == STRAWBERRIES:
            return "S"
        if item == CHOPPING_BOARD:
            return "C"
        if item == CHOPPED_STRAWBERRIES:
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

    @staticmethod
    def get_best_order_item():
        best_item = ''
        award=0
        for cus in Customer.waiting_list:
            if cus.award > award:
                award = cus.award
                best_item = cus.item
        return best_item


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
show_active_order = True


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
can_steal = False

# game loop
while True:
    print_err("== Is chopping ? %s" % str(myChef.is_chopping))

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

    if not myChef.is_chopping:
        if NONE in myChef.item:
            for ti in TableItem.list:
                if DISH in ti.item:
                    can_steal = True
                    next_action = "USE %d %d" % (ti.x, ti.y)
            if next_action == "WAIT":
                can_steal = False

        # if can_steal and NONE not in myChef.item:
        #    next_action = "USE " + Kitchen.get_coords("D")


    if not can_steal or "NONE" not in myChef.item:

        if myChef.is_chopping:
            next_action = myChef.chop_item(myChef.chopped_item)
        elif "NONE" in myChef.item:
            next_action = "USE " + Kitchen.get_coords("D")
        else:
            if show_active_order:
                print_err("My Active Order: %s" % ("-".join(Customer.waiting_list[2].item)))
            for cus_item in Customer.waiting_list[2].item:
                if cus_item not in myChef.item:
                    if "CHOPPED" in cus_item.split("_") and not myChef.is_chopping:
                        myChef.is_chopping = True
                        myChef.chopping_state = "SEARCH_CHOPPED"
                        myChef.chopped_item = cus_item
                        next_action = myChef.chop_item(cus_item)
                        break
                    else:
                        next_action = "USE " + Kitchen.get_coords(Kitchen.get_initial(cus_item))
                        break
            if next_action == "WAIT":
                next_action = "USE " + Kitchen.get_coords("W")
    else:
        if "NONE" not in myChef.item:
            next_action = "USE " + Kitchen.get_coords("W")

    # ========= ACTION ===========================
    print(next_action)

