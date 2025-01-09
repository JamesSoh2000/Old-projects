
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

while True:
    try:
        date = input("Date: ")

        if ("/" in date):
            time = date.split("/")
        elif (date.split(" ")[0] in months):
            time = date.split(" ")
            time[0] = months.index(time[0]) + 1

            time[1] = time[1][0:1]

        # 내가 넣은 숫자가 12월보다 높거나(ex.13월) 31일보다 높은 일자를 넣으면 break를 하지못해서 다시 루프로 돌아감.
        if (int(time[0]) < 13) and (int(time[1]) < 32):
            break

    except:
        # if there is an error like passing string, ValueError이 생길텐데 그런것들을 무시하고 전부 pass 시켜 루프로 돌아가게함.
        pass

if int(time[2]) > 9 and int(time[1]) > 9:
    print(f'{time[2]}-{time[0]}-{time[1]}')
else:
    print(f'{time[2]}-0{time[0]}-0{time[1]}')

