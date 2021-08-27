import random

a = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
box = [-1, -2, -3, -4, -5, -6, -7, -8, -9]
for i in range(3):
    print(" | | ")
print(" ")
ok = random.randint(0, 1)
ok1 = 0
ok2 = 1
while not (box[0] == box[1] == box[2] or box[3] == box[4] == box[5] or box[6] == box[7] == box[8] or box[0] == box[4] ==
           box[8] or box[2] == box[4] == box[6] or box[0] == box[3] == box[6] or box[1] == box[4] == box[7] or box[2] ==
           box[5] == box[8]):
    ok2 = 1
    if ok == 1:
        player = input("Unde vrei sa pui?: ")
        player = int(player)
        box[player - 1] = 1
        a[player - 1] = "X"
        ok = 0
    elif ok == 0:
        ok1 = 0
        if box[4] < 0:
            a[4] = "0"
            box[4] = 0
            ok = 1
        else:
            for i in range(0, 9, 2):
                if box[i] < 0:
                    a[i] = "0"
                    box[i] = 0
                    ok1 = 1
                    ok = 1
                    break
            if ok1 == 0:
                for i in range(0, 9):
                    if box[i] < 0:
                        a[i] = "0"
                        box[i] = 0
                        ok1 = 1
                        break
                    ok = 1
        print(" ")
    for i in range(0, 9):
        if box[i] < 0:
            ok2 = 0
    for i in range(0, 7, 3):
        print("{0}|{1}|{2}".format(a[i], a[i + 1], a[i + 2]))
    print(" ")
    if ok2 == 1:
        break
