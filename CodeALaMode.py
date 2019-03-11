import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

num_all_customers = int(input())
for i in range(num_all_customers):
    # customer_item: the food the customer is waiting for
    # customer_award: the number of points awarded for delivering the food
    customer_item, customer_award = input().split()
    customer_award = int(customer_award)
for i in range(7):
    kitchen_line = input()

# game loop
while True:
    turns_remaining = int(input())
    player_x, player_y, player_item = input().split()
    player_x = int(player_x)
    player_y = int(player_y)
    partner_x, partner_y, partner_item = input().split()
    partner_x = int(partner_x)
    partner_y = int(partner_y)
    num_tables_with_items = int(input())  # the number of tables in the kitchen that currently hold an item
    for i in range(num_tables_with_items):
        table_x, table_y, item = input().split()
        table_x = int(table_x)
        table_y = int(table_y)
    # oven_contents: ignore until wood 1 league
    oven_contents, oven_timer = input().split()
    oven_timer = int(oven_timer)
    num_customers = int(input())  # the number of customers currently waiting for food
    for i in range(num_customers):
        customer_item, customer_award = input().split()
        customer_award = int(customer_award)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # MOVE x y
    # USE x y
    # WAIT
    print("WAIT")