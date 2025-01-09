# TODO

text = input("Text: ")
L = 0
S = 0
word = 0
sentence = 0
letter = 0
end = ["!", "?", "."]
for i in range(len(text)):
    if text[i] == " ":
        word += 1
    elif text[i] in end:
        sentence += 1
        word += 1
    elif text[i] == "'":
        print("Whatt")
    elif text[i].isalpha:
        letter += 1


print(word, sentence, letter)
a = "'"
print(a.isalpha())