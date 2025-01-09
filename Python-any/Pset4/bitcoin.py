import sys
import requests


if len(sys.argv) != 2:
    sys.exit("Missing command-line argument")
elif sys.argv[1].isnumeric() == False:
    sys.exit("Command-line argument is not a number")

try:

    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = r.json()

    rate = data["bpi"]["USD"]["rate"].replace(",", "")
    # print(rate)
    amount = float(rate) * float(sys.argv[1])
    print(f"${amount:,.4f}")

except requests.RequestException:
    print("The requests didn't go well!")
    sys.exit(1)