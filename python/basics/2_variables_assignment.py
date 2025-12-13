"""
- You have $50
- You buy an item that is $15
- With a tax of 3%
- print how much money you have left
"""

money = 50
item = 15
tax = .03

money_left = money - item - (item * tax)

print(money_left)

print(50 - 15 - (15 * .03))

'''
String Assignment:

Ask the user how many days until their birthday
and print an approx number of weeks until their birthday

Weeks is = 7 days

decimals within the return is allowed..

We have to do the type casting while collecting user input .. collected user input is string
'''


days = int(input("How many days until your birthday? "))

print(round(days/7, 2))