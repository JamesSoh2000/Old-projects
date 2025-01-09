groceryList = {}
while True:
    try:
        item = input("").upper()

        if item in (groceryList.keys()):
            groceryList[item] += 1

        else:
            groceryList[item] = 1

    except EOFError:
        print("")
        for key in groceryList.keys():
            print(groceryList[key], key)
        break

