foodList = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}
total = 0

while True:
    try:
        item = input("Pick a food: ").title()

        if item in (foodList.keys()):
            total += foodList[item]

        result = '{:.2f}'.format(total)
        print(f"Total: ${result}")

    except EOFError:
        break

print("\n")