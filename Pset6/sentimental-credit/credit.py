# TODO
import sys

def main():


    credit_number = input("Number: ")
    while (credit_number.isdigit() == False):
        credit_number = input("Number: ")

    sumBy2 = 0
    sum = 0
    addsum = 0


    # Multiply every other digit by 2
    for i in range(len(credit_number)):
        # right now, credit_number is a string, so convert it to integer type.
        if (i % 2 == 0):
            sumBy2 += int(credit_number[i]) * 2
        else:
            sum += int(credit_number[i])

    if (addsum % 10 == 0):
        if (len(credit_number) == 15 and credit_number[0] == "3"):
            return print("AMEX")
        elif (len(credit_number) == 16 and credit_number[0] == "5"):
            return print("MASTERCARD")
        elif ((len(credit_number) == 13 or len(credit_number) == 16) and credit_number[0] == "4"):
            return print("VISA")

    return print("INVALID")


main()


