import sys
from pyfiglet import Figlet
import random

IsThere = True
figlet = Figlet()

if len(sys.argv) == 1:
    IsThere = True
elif len(sys.argv) == 3 and (sys.argv[1] == "-f" or sys.argv[1] == "--font"):
    IsThere = False
else:
    print("Invalid Usage!")
    sys.exit(1)

if IsThere == False:
    try:
        figlet.setFont(font=sys.argv[2])
    except:
        print("Invalid Usage!")
        sys.exit(1)
    else:
        font = random.choice(figlet.getFonts())

user = input("Input: ")

print(figlet.renderText(user))