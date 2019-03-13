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

    distance = math.sqrt(((xa - xb) ** 2) + ((ya - yb) ** 2))
    return distance


# =======================

class Action:
    @staticmethod
    def use(target):
        return "USE " + Kitchen.get_coords(target)

    @staticmethod
    def use_coords(p_x, p_y):
        return "USE %d %d" % (int(p_x), int(p_y))


class Chef:
    def __init__(self, name, p_x, p_y, items):
        self.name = name
        self.x = int(p_x)
        self.y = int(p_y)
        self.item = items.split("-")

        # post-refactoring V

        self.action_state = None

        # pre-refactoring V

        self.str_coords = ""
        self.update_str_coords()

        self.target_command = ""

    def update_info(self, p_x, p_y, items):
        self.x = int(p_x)
        self.y = int(p_y)
        self.update_str_coords()
        self.item = items.split("-")

    def update_str_coords(self):
        self.str_coords = "%d %d" % (self.x, self.y)

    def show_items(self):
        print_err(self.name + " : " + " & ".join(self.item))

    def has_all_items(self):
        ready = True
        for it in self.target_command:
            if it not in self.item:
                ready = False

        return ready

    def is_around_coords(self, p_x, p_y):
        p_x = int(p_x)
        p_y = int(p_y)
        if p_x >= self.x - 1 and p_x <= self.x + 1:
            if p_y >= self.y - 1 and p_y <= self.y + 1:
                return True
        return False

    def is_around(self, target, direction=None, empty=None):

        search_range_x = range(-1, 2)
        search_range_y = range(-1, 2)

        if len(target) > 1:
            target = Kitchen.get_initial(target)

        if direction is not None:
            p_x, p_y = Kitchen.get_coords(direction).split(" ")
            p_x = int(p_x)
            p_y = int(p_y)
            if p_x <= self.x:
                search_range_x = range(1, -2, -1)
            if p_y >= self.y:
                search_range_y = range(1, -2, -1)

        for iy in search_range_y:
            for ix in search_range_x:
                look_x = self.x + ix
                look_y = self.y + iy
                if Kitchen.map[look_y][look_x] == target:
                    print_debug("test1")
                    if empty is None:
                        return [look_x, look_y]
                    else:
                        if TableItem.get_item_at_coords(look_x, look_y) is None:
                            return [look_x, look_y]
        return None

    def use_dish(self):
        possiblity1 = "99 99"
        if TableItem.has_item(DISH):
            possiblity1 = TableItem.get_item_coords(DISH)
        possiblity2 = Kitchen.get_coords(DISH)

        if get_distance(self.str_coords, possiblity1) < get_distance(self.str_coords, possiblity2):
            return "USE " + possiblity1
        else:
            return "USE " + possiblity2

    def drop_dish(self):
        search_table = self.is_around("#", empty=True)
        if search_table is not None:
            p_x, p_y = list(map(int, search_table))
            return Action.use_coords(p_x, p_y)
        return None


class Kitchen:
    map = []

    @staticmethod
    def add_line_to_map(line):
        Kitchen.map.append(list(line))

    @staticmethod
    def show_map():
        for line in Kitchen.map:
            print_err("-".join(str(p_x) for p_x in line))

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
    def get_initial(p_item):
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

        if p_item in values:
            return values[p_item]
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

        if TART in self.item or CROISSANT in self.item or CHOPPED_STRAWBERRIES in self.item:
            new_item = []
            if TART in self.item:
                self.item.remove(TART)
                new_item.append(TART)
            if CROISSANT in self.item:
                self.item.remove(CROISSANT)
                new_item.append(CROISSANT)
            if CHOPPED_STRAWBERRIES in self.item:
                self.item.remove(CHOPPED_STRAWBERRIES)
                new_item.append(CHOPPED_STRAWBERRIES)
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
        best_item = None
        award = 0
        for cus in Customer.waiting_list:
            if cus.award > award:
                award = cus.award
                best_item = cus.item
        return best_item


class TableItem:
    list = []

    def __init__(self, p_x, p_y, items):
        self.x = int(p_x)
        self.y = int(p_y)
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
    def get_item_at_coords(p_x, p_y):
        for it in TableItem.list:
            if it.x == int(p_x) and it.y == int(p_y):
                return it.item
        return None

    @staticmethod
    def has_item(p_item):
        for it in TableItem.list:
            # print_debug("Has Item Comp : %s / %s" % (item, it.item))
            if p_item in it.item and len(it.item) == 1:
                return True
        return False

    @staticmethod
    def get_item_coords(p_item):
        for it in TableItem.list:
            if p_item in it.item:
                return [it.x, it.y]
        return "NO ITEM FOUND (%s)" % p_item

    @staticmethod
    def get_all_dishes():
        for it in TableItem.list:
            if DISH in it.item:
                print_debug("GetAll : %s : comp=%s" % (" & ".join(it.item), str(TableItem.dish_is_compatible(it))))

    @staticmethod
    def dish_is_compatible(dish, except_item=None):
        compatible = True

        if DISH not in dish.item:
            compatible = False
        else:
            if except_item is not None and except_item in dish.item:
                compatible = False
            else:
                for it in dish.item:
                    if it not in myChef.target_command:
                        compatible = False

        return compatible

    @staticmethod
    def find_most_compatible_dish(except_item=None):
        nb_items = 0
        return_dish = None
        for it in TableItem.list:
            if TableItem.dish_is_compatible(it, except_item):
                if len(it.item) > nb_items:
                    nb_items = len(it.item)
                    return_dish = it
        return return_dish


# ============== INIT ============================

show_waiting = False
show_table_items = False
show_active_order = True
show_oven = False

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
    oven_contents = oven_contents.split("-")

    num_customers = int(input())  # the number of customers currently waiting for food
    Customer.waiting_list = []
    for i in range(num_customers):
        customer_item, customer_award = input().split()
        customer_award = int(customer_award)
        newCustomer = Customer(customer_item, customer_award)
        Customer.waiting_list.append(newCustomer)

    # ====== INFO MESSAGES ==============================

    if show_waiting:
        print_err("Waiting:")
        Customer.show_waiting_customers()

    if show_oven:
        print_err("Oven (%d):" % oven_timer)
        print_err(oven_contents)

    if show_table_items:
        TableItem.get_all_dishes()

    myChef.show_items()

    # ====== LOGIC ==============================

    next_action = "WAIT"

    print_debug("active order =")

    myChef.target_command = ''
    print_debug(myChef.target_command)

    for ord in Customer.waiting_list:
        test_comp = TableItem.find_most_compatible_dish()
        if test_comp is '':
            myChef.target_command = ''

    print_debug(myChef.target_command)
    myChef.target_command = Customer.get_best_order_item()
    print_debug(myChef.target_command)
    print_debug("====")
    # myChef.target_command = Customer.get_best_order_item()



    if show_active_order:
        print_err("My Active Order: %s" % ("-".join(myChef.target_command)))

    if not myChef.has_all_items():

        comp_dish = TableItem.find_most_compatible_dish()
        can_drop = myChef.drop_dish()
        print_debug("My Dish comp? %s" % str(TableItem.dish_is_compatible(myChef)))

        if myChef.action_state is None:
            print_err("Action : NONE")

            if NONE in myChef.item:
                print_debug("Part None")

                if comp_dish is not None:
                    next_action = Action.use_coords(comp_dish.x, comp_dish.y)
                else:
                    next_action = Action.use(DISH)

            elif not TableItem.dish_is_compatible(myChef) and can_drop:
                print_err("Action : Not compatible! Dropping dish...")
                next_action = can_drop

            elif DISH in myChef.item and comp_dish is not None and len(comp_dish.item) > len(myChef.item):
                print_debug("Part Compatible dish")

                print_debug("comp len : %d" % len(comp_dish.item))
                print_debug("chef len : %d" % len(myChef.item))
                if can_drop is not None:
                    next_action = can_drop
            else:
                print_debug("Part Other")
                processed_foods = [TART, CROISSANT, CHOPPED_STRAWBERRIES]

                for order_part in myChef.target_command:
                    # print_debug("Order : " + order_part)

                    if order_part not in myChef.item:

                        if order_part not in processed_foods:
                            print_debug("%s : Standard food" % order_part)
                            next_action = Action.use(order_part)
                        else:
                            print_debug("%s : Processed" % order_part)
                            if TableItem.has_item(order_part):
                                x, y = list(map(int, TableItem.get_item_coords(order_part)))
                                if DISH in TableItem.get_item_at_coords(x, y):
                                    if can_drop is not None:
                                        next_action = can_drop
                                else:
                                    next_action = Action.use_coords(x, y)
                            else:
                                # ============ PROCESS =========================
                                myChef.action_state = "process_" + order_part
                                # ==============================================
        else:
            print_err("Action : %s!" % myChef.action_state)

            if myChef.action_state == "process_" + TART:
                # ================ PROCESSING TART ==================
                process_comp_dish = TableItem.find_most_compatible_dish(TART)

                if DISH in myChef.item and TART not in myChef.item and can_drop is not None:
                    next_action = can_drop
                elif DOUGH in myChef.item:
                    next_action = Action.use(CHOPPING_BOARD)
                elif CHOPPED_DOUGH in myChef.item:
                    next_action = Action.use(BLUEBERRIES)
                elif RAW_TART in myChef.item or RAW_TART in oven_contents or TART in oven_contents:
                    next_action = Action.use(OVEN)
                elif TART in myChef.item:
                    if process_comp_dish is not None:
                        next_action = Action.use_coords(process_comp_dish.x, process_comp_dish.y)
                        if myChef.is_around_coords(process_comp_dish.x, process_comp_dish.y):
                            myChef.action_state = None
                    else:
                        next_action = Action.use(DISH)
                        if myChef.is_around(DISH) != None:
                            myChef.action_state = None
                else:
                    next_action = Action.use(DOUGH)

            elif myChef.action_state == "process_" + CROISSANT:
                # ================ PROCESSING CROISSANT ==================
                process_comp_dish = TableItem.find_most_compatible_dish(CROISSANT)

                if DISH in myChef.item and CROISSANT not in myChef.item and can_drop is not None:
                    next_action = can_drop
                elif DOUGH in myChef.item or DOUGH in oven_contents or CROISSANT in oven_contents:
                    next_action = Action.use(OVEN)
                elif CROISSANT in myChef.item:
                    if process_comp_dish is not None:
                        next_action = Action.use_coords(process_comp_dish.x, process_comp_dish.y)
                        if myChef.is_around_coords(process_comp_dish.x, process_comp_dish.y):
                            myChef.action_state = None
                    else:
                        next_action = Action.use(DISH)
                        print_debug("is around " + str(myChef.is_around(DISH)))
                        if myChef.is_around(DISH) != None:
                            myChef.action_state = None
                else:
                    next_action = Action.use(DOUGH)

            elif myChef.action_state == "process_" + CHOPPED_STRAWBERRIES:
                # ============ PROCESSING CHOPPED STRAWBERRIES ===============
                process_comp_dish = TableItem.find_most_compatible_dish(CHOPPED_STRAWBERRIES)

                if DISH in myChef.item and CHOPPED_STRAWBERRIES not in myChef.item and can_drop is not None:
                    next_action = can_drop
                elif STRAWBERRIES in myChef.item:
                    next_action = Action.use(CHOPPING_BOARD)
                elif CHOPPED_STRAWBERRIES in myChef.item:
                    if process_comp_dish is not None:
                        next_action = Action.use_coords(process_comp_dish.x, process_comp_dish.y)
                        if myChef.is_around_coords(process_comp_dish.x, process_comp_dish.y):
                            myChef.action_state = None
                    else:
                        next_action = Action.use(DISH)
                        if myChef.is_around(DISH) != None:
                            myChef.action_state = None
                else:
                    next_action = Action.use(STRAWBERRIES)

            else:
                next_action = "ERROR IN PROCESSING CHOICE"

    else:
        next_action = Action.use(WINDOW)

    # ========= ACTION ===========================
    print(next_action)
