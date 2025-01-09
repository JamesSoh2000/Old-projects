import csv
import sys
# Open csv file and DNA sequence, read contents into memory.
# For each STR, compute the longest run of consecutive repeats in the DNA sequence.
# compare the STR counts against each row in the CSV file.

# with open(sys.argv[1], "r" or "a") as File:
#     reader = csv.DictReader(File)
#     for row in reader:
#         # 여기서 row는 {name : Sarah, AGATC : 2, AATG : 3, TATC : 4} 이런식으로 딕셔너리를 줌

# grocery = ['bread', 'milk', 'butter']
# enumerateGrocery = enumerate(grocery)

# # converting to list
# print(list(enumerateGrocery))

# # for loop using enumerate
# for i, letter in enumerate(grocery):
#     print(i, letter)

# # remove leading and trailing whitespaces
# message = '     Learn Python  '
# print('Message:', message.strip())

# # string to a list "sllit function"
# txt = "Hey david"
# txt.split()
# txt2 = "hello, my name is Peter, I am 26 years old"
# x = txt2.split(", ")
# print(x)

# file.read() function


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")
    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1], "r") as File:
        reader = csv.DictReader(File)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    temp = []
    with open(sys.argv[2], "r") as seq:
        reader2 = seq.read()
    temp.append(reader2)
    # length of reader2 is 171 including \n(이건 하나취급받음) 그러므로 170개의 letter이 존재함.
    a = "ABCDAAAA"  # 0123 1234 2345 3456 4567

    # TODO: Find longest match of each STR in DNA sequence

    # Now we have a list of STR
    keys=[]
    for key in database[0].keys():
        if (key != "name"):
            keys.append(key)
    # Now make a dictionary of STR to count the longest_match for each STR
    STR = {}
    for i in range(len(keys)):
        STR[keys[i]] = 0

    # Check for each STR we have.
    for i in range(len(keys)):
        longest = find(reader2.rstrip("\n"), keys[i])
        STR[keys[i]] = longest

    print(STR)


    # TODO: Check database for matching profiles

    for i in range(len(database)):
        count = 0
        for j in range(len(keys)):
            if int(database[i][keys[j]]) == STR[keys[j]]:
                count += 1
            if count == len(keys):
                return print(database[i]["name"])



    return print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run



## This is my own Function for find longest 내가 직접 만듬~
def find(seq, STR):
    len_seq = len(seq)
    len_STR = len(STR)
    count = 0
    end = 0
    longest = 0
    for i in range(len_seq):

        pointer = 0
        while True:
            if seq[pointer:(pointer+len_STR)] == STR:

                for i in range(pointer, len_seq, len_STR):
                    if seq[i:i + len_STR] == STR:
                        count += 1
                        pointer = i + len_STR
                    else:
                        break
                if (longest < count):
                    longest = count
                    count = 0

            else:
                if (pointer >= len_seq - len_STR):
                    break
                pointer += 1
                count = 0
    return longest

main()
