height = int(input("Height: "))
count = 1
for i in range(height):
    print(" " * (height - (i+1)), end='')
    print("#" * (i+1), end='')
    print("  ", end='')
    print("#" * (i+1), end='')
    print(" " * (height - (i+1)), end='')
    print("")


# def main():

#     return recursive(height)



# def recursive(height):

#     if height == 1:
#         return print(() * "#" + "  " + (height+3) * "#")
