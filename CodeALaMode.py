import sys
import math

CHOPPED_STRAWBERRIES = "CHOPPED_STRAWBERRIES"
STRAWBERRIES = "STRAWBERRIES"
NONE = "NONE"
BLUEBERRIES = "BLUEBERRIES"
DISH = "DISH"
ICE_CREAM = "ICE_CREAM"
CHOPPING_BOARD = "CHOPPING_BOARD"
OVEN = "OVEN"
DOUGH = "DOUGH"
CROISSANT = "CROISSANT"
CHOPPED_DOUGH = "CHOPPED_DOUGH"
RAW_TART = "RAW_TART"
TART = "TART"
WINDOW = "WINDOW"


def print_err(string):
    print(string, file=sys.stderr)


def print_debug(string):
    if True:
        print("DEBUG: %s" % string, file=sys.stderr)


def get_distance(a_pos, b_pos):
    xa, ya = list(map(int, a_pos.split(" ")))
    xb, yb = list(map(int, b_pos.split(" ")))

    distance = math.sqrt(((xa-xb)**2) + ((ya-yb)**2))
    return distance

# =======================
class Chef:
    def __init__(self, name, x, y, items):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.str_coords = ""
        self.update_str_coords()

        self.item = items.split("-")

        self.last_dish_coords = "EMPTY"

        self.is_chopping = False
        self.chopped_item = "EMPTY"
        self.chopping_state = "EMPTY"

        self.is_baking = False
        self.baked_item = "EMPTY"
        self.baking_state = "EMPTY"
        self.bake_timer = 0
        self.bake_timer_running = False

        self.is_baking_tart = False
        self.baked_tart_item = "EMPTY"
        self.baking_tart_state = "EMPTY"

        self.target_command = ""

    def update_info(self, x, y, items):
        self.x = int(x)
        self.y = int(y)
        self.update_str_coords()
        self.item = items.split("-")

        if self.bake_timer_running:
            self.bake_timer += 2
            if self.bake_timer > 20:
                self.bake_timer_running = False

    def update_str_coords(self):
        self.str_coords = "%d %d" % (self.x, self.y)

    def set_bake_timer(self):
        self.bake_timer = 0
        self.bake_timer_running = True

    def show_items(self):
        print_err(self.name + " : " + " & ".join(self.item))

    def has_all_items(self, command):
        ready = True
        for it in command:
            if it not in self.item:
                ready = False

        return ready

    def is_around_coords(self, x, y):
        x = int(x)
        y = int(y)
        if x >= self.x-1 and x <= self.x+1:
            if y >= self.y-1 and y <= self.y+1:
                return True
        return False

    def chop_item(self):
        return_action = "ERROR IN CHOP_ITEM"

        if self.chopping_state == "SEARCH_CHOPPED":
            found_chopped = False
            for it in TableItem.list:
                if CHOPPED_STRAWBERRIES in it.item:
                    found_chopped = True
                    return_action = "USE %d %d" % (it.x, it.y)
                    if self.is_around_coords(it.x, it.y):
                        return_action = "USE %d %d" % (it.x, it.y)
                        self.chopping_state = "FINISH"
            if self.is_chopping and not found_chopped:
                if self.is_around("C") == False:
                    self.chopping_state = "SEARCH_BOARD"
                else:
                    self.chopping_state = "DROP_DISH"

        if self.chopping_state == "SEARCH_BOARD":
            return_action = "MOVE " + Kitchen.get_coords(CHOPPING_BOARD)

            if self.is_around("C") != False:
                self.chopping_state = "DROP_DISH"

        if self.chopping_state == "DROP_DISH":
                free_table_coords = self.is_around("#", "C")
                self.last_dish_coords = free_table_coords
                return_action = "USE " + free_table_coords
                if NONE in self.item:
                    self.chopping_state = "SEARCH_ITEM"

        if self.chopping_state == "SEARCH_ITEM":
            if STRAWBERRIES not in self.item:
                return_action =  "USE " + Kitchen.get_coords(STRAWBERRIES)
            else:
                self.chopping_state = "CHOP_ITEM"

        if self.chopping_state == "CHOP_ITEM":
            if CHOPPED_STRAWBERRIES not in self.item:
                return_action = "USE " + Kitchen.get_coords(CHOPPING_BOARD)
            else:
                self.chopping_state = "USE_DISH"

        if self.chopping_state == "USE_DISH":
            last_coords = self.last_dish_coords
            x, y = last_coords.split(" ")
            if DISH not in TableItem.get_item_at_coords(x, y):
                self.chopping_state = "ERROR"

            if DISH not in self.item:
                return_action = "USE " + last_coords
            else:
                return_action = "WAIT; Huh?"
                self.chopping_state = "FINISH"

        if self.chopping_state == "ERROR":
            print_err("ERROR IN CHOPPING MACHINE")
            return_action = "WAIT; Problem!"
            self.chopping_state = "FINISH"

        if self.chopping_state == "FINISH":
            self.last_dish_coords = "EMPTY"
            self.is_chopping = False

        print_err("Choppin State = " + self.chopping_state)
        return return_action

    def bake_item(self):
        return_action = "ERROR IN BAKE_ITEM"

        if self.baking_state == "SEARCH_BAKED":
            found_baked = False
            for it in TableItem.list:
                if CROISSANT in it.item:
                    found_baked = True
                    return_action = "USE %d %d" % (it.x, it.y)
                    if self.is_around_coords(it.x, it.y):
                        return_action = "USE %d %d" % (it.x, it.y)
                        self.baking_state = "FINISH"
            if self.is_baking and not found_baked:
                if self.is_around("O") == False:
                    self.baking_state = "SEARCH_OVEN"
                else:
                    self.baking_state = "DROP_DISH"

        if self.baking_state == "SEARCH_OVEN":
            return_action = "MOVE " + Kitchen.get_coords(OVEN)

            if self.is_around("O") != False:
                self.baking_state = "DROP_DISH"

        if self.baking_state == "DROP_DISH":
            free_table_coords = self.is_around("#", "O")
            self.last_dish_coords = free_table_coords
            return_action = "USE " + free_table_coords
            if NONE in self.item:
                self.baking_state = "SEARCH_ITEM"

        if self.baking_state == "SEARCH_ITEM":
            if DOUGH not in self.item:
                return_action = "USE " + Kitchen.get_coords(DOUGH)
            else:
                self.baking_state = "BAKE_ITEM"

        if self.baking_state == "BAKE_ITEM":
            if CROISSANT not in self.item:
                return_action = "USE " + Kitchen.get_coords(OVEN)
            else:
                self.baking_state = "USE_DISH"

        if self.baking_state == "USE_DISH":
            last_coords = self.last_dish_coords
            x, y = last_coords.split(" ")

            if DISH not in self.item:
                if DISH not in TableItem.get_item_at_coords(x, y):
                    if TableItem.has_item(DISH):
                        return_action = "USE " + TableItem.get_item_coords(DISH)
                    else:
                        return_action = "USE " + Kitchen.get_coords(DISH)
                    # self.baking_state = "ERROR"
                else:
                    return_action = "USE " + last_coords
            else:
                return_action = "WAIT; hmm.."
                self.baking_state = "FINISH"

        if self.baking_state == "ERROR":
            print_err("ERROR IN BAKING MACHINE")
            return_action = "WAIT; Problem!"
            self.baking_state = "FINISH"

        if self.baking_state == "FINISH":
            self.last_dish_coords = "EMPTY"
            self.is_baking = False

        return return_action

    def bake_tart_item(self):
        return_action = "ERROR IN BAKE_tart_ITEM"
        # print_debug("Baking Tart")
        # print_debug("Bake Tart : " + self.baking_tart_state)

        steps = ['SEARCH_OVEN', 'DROP_DISH', 'SEARCH_ITEM', 'CHOP_ITEM', 'ADD_BERRY', 'BAKE_ITEM', 'USE_DISH']
        step = 99
        if self.baking_tart_state in steps:
            step = steps.index(self.baking_tart_state)
        # print_debug("Step : " + str(step))

        if TableItem.has_item(RAW_TART) and NONE in self.item and step < 3:
            return_action = "USE " + TableItem.get_item_coords(RAW_TART)
            return return_action
        if RAW_TART in self.item:
            self.baking_tart_state = "BAKE_ITEM"

        if self.baking_tart_state == "SEARCH_BAKED":
            found_baked = False
            for it in TableItem.list:
                if TART in it.item:
                    found_baked = True
                    return_action = "USE %d %d" % (it.x, it.y)
                    if self.is_around_coords(it.x, it.y):
                        return_action = "USE %d %d" % (it.x, it.y)
                        self.baking_tart_state = "FINISH"
            if self.is_baking_tart and not found_baked:
                if self.is_around("O") == False:
                    self.baking_tart_state = "SEARCH_OVEN"
                else:
                    self.baking_tart_state = "DROP_DISH"

        if self.baking_tart_state == "SEARCH_OVEN":
            return_action = "MOVE " + Kitchen.get_coords(OVEN)

            if self.is_around("O") != False:
                self.baking_tart_state = "DROP_DISH"

        if self.baking_tart_state == "DROP_DISH":
            free_table_coords = self.is_around("#", "O")
            self.last_dish_coords = free_table_coords
            return_action = "USE " + free_table_coords
            if NONE in self.item:
                self.baking_tart_state = "SEARCH_ITEM"

        if self.baking_tart_state == "SEARCH_ITEM":
            if DOUGH not in self.item:
                if TableItem.has_item(DOUGH):
                    return_action = "USE " + TableItem.get_item_coords(DOUGH)
                else:
                    return_action = "USE " + Kitchen.get_coords(DOUGH)
            else:
                self.baking_tart_state = "CHOP_ITEM"

        if self.baking_tart_state == "CHOP_ITEM":
            if CHOPPED_DOUGH not in self.item:
                return_action = "USE " + Kitchen.get_coords(CHOPPING_BOARD)
            else:
                self.baking_tart_state = "ADD_BERRY"

        if self.baking_tart_state == "ADD_BERRY":
            if RAW_TART not in self.item:
                return_action = "USE " + Kitchen.get_coords(BLUEBERRIES)
            else:
                self.baking_tart_state = "BAKE_ITEM"

        if self.baking_tart_state == "BAKE_ITEM":
            if TART not in self.item:
                print_debug("timer : " + str(oven_timer))

                if oven_timer < 8 and self.is_around(OVEN):
                    oven_x, oven_y = list(map(int, Kitchen.get_coords(OVEN).split(" ")))
                    if partnerChef.y > self.y:
                        return_action = "MOVE %d %d" % (self.x, oven_y + 1)
                    else:
                        return_action = "MOVE %d %d" % (self.x, oven_y - 1)

                else:
                    return_action = "USE " + Kitchen.get_coords(OVEN)
            else:
                self.baking_tart_state = "USE_DISH"

        if self.baking_tart_state == "USE_DISH":
            last_coords = self.last_dish_coords
            x, y = last_coords.split(" ")

            if DISH not in self.item:
                return_action = self.use_dish()
                ''' if DISH not in TableItem.get_item_at_coords(x, y):
                     if TableItem.has_item(DISH):
                        return_action = "USE " + TableItem.get_item_coords(DISH)
                     else:
                        return_action = "USE " + Kitchen.get_coords(DISH)
                     self.baking_state = "ERROR"
                else:
                    return_action = "USE " + last_coords'''
            else:
                return_action = "WAIT; hmm.."
                self.baking_tart_state = "FINISH"

        if self.baking_tart_state == "ERROR":
            print_err("ERROR IN BAKING MACHINE")
            return_action = "WAIT; Problem!"
            self.baking_tart_state = "FINISH"

        if self.baking_tart_state == "FINISH":
            self.last_dish_coords = "EMPTY"
            self.is_baking_tart = False

        # print_debug("Bake Tart : " + self.baking_tart_state)
        return return_action

    def is_around(self, target, direction=None):

        search_range_x = range(-1, 2)
        search_range_y = range(-1, 2)

        if direction is not None:
            x, y = Kitchen.get_coords(direction).split(" ")
            x = int(x)
            y = int(y)
            if x <= self.x:
                search_range_x = range(1, -2, -1)
            if y >= self.y:
                search_range_y = range(1, -2, -1)

        for iy in search_range_y:
            for ix in search_range_x:
                look_x = self.x + ix
                look_y = self.y + iy
                if Kitchen.map[look_y][look_x] == target:
                    return "%d %d" % (look_x, look_y)

        return False

    def use_dish(self):
        possiblity1 = "99 99"
        if TableItem.has_item(DISH):
            possiblity1 = TableItem.get_item_coords(DISH)
        possiblity2 = Kitchen.get_coords(DISH)

        if get_distance(self.str_coords, possiblity1) < get_distance(self.str_coords, possiblity2):
            return "USE " + possiblity1
        else:
            return "USE " + possiblity2


class Kitchen:
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
        real_target = target
        if len(target) > 1:
            real_target = Kitchen.get_initial(target)

        for index, line in enumerate(Kitchen.map):
            if real_target in line:
                coords = "%d %d" % (line.index(real_target), index)
                return coords
        return "COORDS_NOT_FOUND (%s / %s)" % (target, real_target)

    @staticmethod
    def get_initial(item):
        values = {
            DISH: "D",
            ICE_CREAM: "I",
            BLUEBERRIES: "B",
            STRAWBERRIES: "S",
            CHOPPING_BOARD: "C",
            OVEN: "O",
            DOUGH: "H",
            WINDOW: "W"
        }

        if item in values:
            return values[item]
        else:
            return "NO INITIAL FOUND"


class Customer:
    nb_customers = 0
    full_list = []
    waiting_list = []

    def __init__(self, items, award):
        self.item = items.split("-")  # customer_item: the food the customer is waiting for
        self.award = award  # customer_award: the number of points awarded for delivering the food
        self.id = Customer.nb_customers
        Customer.nb_customers += 1

        if TART in self.item or CROISSANT in self.item or STRAWBERRIES in self.item:
            new_item = []
            if TART in self.item:
                self.item.remove(TART)
                new_item.append(TART)
            if CROISSANT in self.item:
                self.item.remove(CROISSANT)
                new_item.append(CROISSANT)
            if STRAWBERRIES in self.item:
                self.item.remove(STRAWBERRIES)
                new_item.append(STRAWBERRIES)
            for it in self.item:
                new_item.append(it)
            self.item = new_item

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
        award = 0
        for cus in Customer.waiting_list:
            if cus.award > award:
                award = cus.award
                best_item = cus.item
        return best_item


class TableItem:
    list = []

    def __init__(self, x, y, items):
        self.x = int(x)
        self.y = int(y)
        self.item = items.split("-")

    @staticmethod
    def show_all_items():
        for index, it in enumerate(TableItem.list):
            print_err("%d - %s %s %s" % (index, it.x, it.y, it.item))

    def item_is_ordered(self, customers):
        for cus in customers:
            if cus.item[1] in self.item and cus.item[2] in self.item:
                coords = "%d %d" % (self.x, self.y)
                return coords

    @staticmethod
    def get_item_at_coords(x, y):
        for it in TableItem.list:
            if it.x == int(x) and it.y == int(y):
                return it.item
        return "Nothing"

    @staticmethod
    def has_item(item):
        for it in TableItem.list:
            # print_debug("Has Item Comp : %s / %s" % (item, it.item))
            if item in it.item:
                return True
        return False

    @staticmethod
    def get_item_coords(item):
        for it in TableItem.list:
            if item in it.item:
                return "%d %d" % (it.x, it.y)
        return "NO ITEM FOUND (%s)" % item

    @staticmethod
    def get_all_dishes():
        list = []
        for it in TableItem.list:
            if DISH in it.item:
                print_debug("GetAll : %s : comp=%s" % (" & ".join(it.item), str(TableItem.dish_is_compatible(it))))

    @staticmethod
    def dish_is_compatible(dish):
        compatible = True

        for it in dish.item:
            if it not in myChef.target_command:
                compatible = False

        return compatible


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
    turns_remaining = int(input())

    player_x, player_y, player_item = input().split()
    myChef.update_info(player_x, player_y, player_item)
    partner_x, partner_y, partner_item = input().split()
    partnerChef.update_info(partner_x, partner_y, partner_item)

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
        newCustomer = Customer(customer_item, customer_award)
        Customer.waiting_list.append(newCustomer)

    if show_waiting:
        print_err("Waiting:")
        Customer.show_waiting_customers()

    next_action = "WAIT"

    # ====== LOGIC ==============================

    myChef.show_items()
    # target_command = Customer.waiting_list[2].item
    myChef.target_command = Customer.get_best_order_item()

    TableItem.get_all_dishes()

    if show_active_order:
        print_err("My Active Order: %s" % ("-".join(myChef.target_command)))

    if not myChef.is_chopping and not myChef.is_baking and not myChef.is_baking_tart:
        if NONE in myChef.item:
            for ti in TableItem.list:
                if DISH in ti.item:
                    can_steal = True
                    next_action = "USE %d %d" % (ti.x, ti.y)
        else:
            can_steal = False

    if not can_steal:
        if myChef.is_baking_tart:
            next_action = myChef.bake_tart_item()
        elif myChef.is_baking:
            next_action = myChef.bake_item()
        elif myChef.is_chopping:
            next_action = myChef.chop_item()
        elif NONE in myChef.item:
            next_action = "USE " + Kitchen.get_coords(DISH)
        else:
            for cus_item in myChef.target_command:
                if cus_item not in myChef.item:
                    if TART in cus_item and not myChef.is_baking_tart:
                        myChef.is_baking_tart = True
                        myChef.baking_tart_state = "SEARCH_BAKED"
                        myChef.baked_tart_item = cus_item
                        next_action = myChef.bake_tart_item()
                        break
                    elif CROISSANT in cus_item and not myChef.is_baking:
                        myChef.is_baking = True
                        myChef.baking_state = "SEARCH_BAKED"
                        myChef.baked_item = cus_item
                        next_action = myChef.bake_item()
                        break
                    elif "CHOPPED" in cus_item.split("_") and not myChef.is_chopping:
                        myChef.is_chopping = True
                        myChef.chopping_state = "SEARCH_CHOPPED"
                        myChef.chopped_item = cus_item
                        next_action = myChef.chop_item()
                        break
                    else:
                        next_action = "USE " + Kitchen.get_coords(cus_item)
                        break
            if next_action == "WAIT":
                next_action = "USE " + Kitchen.get_coords(WINDOW)

    if myChef.has_all_items(myChef.target_command):
        if not partnerChef.is_around("W") and partnerChef.y > 2 and not myChef.is_around("W"):
            if partnerChef.x < 5:
                next_action = "MOVE 4 5"
            elif partnerChef.x > 5:
                next_action = "MOVE 6 5"
        else:
            next_action = "USE " + Kitchen.get_coords(WINDOW)

    # ========= ACTION ===========================
    print(next_action)
