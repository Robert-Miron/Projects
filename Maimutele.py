import tkinter
from tkinter import *
import math
import numpy as np
from PIL import Image, ImageTk
import random

window = tkinter.Tk()
window.geometry('1330x720')
window.title('Maimutele')
window.resizable(0, 0)
index = 1
ok = 0

def misca(x: list, y: list):
    global index, ok
    field.move(p, x[index] - x[index - 1], y[index] - y[index - 1]) #misca banana cu x si y unitati
    index += 1
    if index < len(x) and y[index] <= 720:
        if (x[index - 1] + 10 == field.coords(m2)[0] - 50 and y[index - 1] + 10 == field.coords(m2)[1] - 60 and ok==0) or (
                x[index - 1] - 10 == field.coords(m2)[0] - 50 and y[index - 1] - 10 == field.coords(m2)[1] - 60 and ok==0) or (
                x[index - 1] == field.coords(m2)[0] - 50 and y[index - 1] == field.coords(m2)[1] - 60 and ok==0):
            print("Ai nimerit!")
            ok = 1
            return 1
        elif ok == 0:
            field.move(p, x[index] - x[index - 1], y[index] - y[index - 1])
            index += 1
            field.after(30, misca(x, y))
    else:
        print('banana este la: ', field.coords(p)[0], field.coords(p)[1])
        return 0


def aruncare():
    global p
    global player
    #In functie de jucator, se stabileste directia vitezei si unghiul
    if player == 1:
        v0 = float(viteza1.get())
        unghi = float(unghi1.get())
        print(unghi)
    else:
        v0 = -float(viteza2.get())
        unghi = 180 - float(unghi2.get())
        #se stabiliesc coordonatele initiale ale bananei care vo fi folosite la determinarea pozitiilor intermediare
    x0 = field.coords(p)[0]
    y0 = field.coords(p)[1]
    print('x0=', x0, 'y0=', y0)
    g = 9.81  # acceleratia gravitationala [m/s^2]
    unghi_rad = unghi * math.pi / 180  # conversia de la grade la radieni
    print(unghi_rad)
    vx = v0 * math.cos(unghi_rad)  # componenta orizontala a vitezei la t=0.
    print('vx=', vx)
    v0y = v0 * math.sin(unghi_rad) # componenta vericala a vitezei la t=0
    print('v0y=', v0y)
    x = []
    y = []
    vy = []
    for i in range(len(tt)):
        vy.append(v0y * math.sin(unghi_rad) - g * tt[i])  # componenta vericala a vitezei la fiecare moment al miscarii
        x.append(x0 + vx * tt[i]) #coordonata x a bananei la fiecare moment al miscarii
        y.append(y0 - v0y * tt[i] + g * tt[i] * tt[i] / 2) #coordonata y a bananei la fiecare moment al miscarii
    print('x=', x)
    print('y=', y)
    print(field.coords(p)[0], field.coords(p)[1])
    if misca(x, y) == 1:
        final = Tk()
        final.pack()
        mesaj = tkinter.Message(final, font=('arial', 12), text="FELICITARI AI CASTIGAT!")
    else:
        if player == 1:
            player = 2
            dreapta2['state'] = 'normal'
            stanga2['state'] = 'normal'
            arunca2['state'] = 'normal'
            dreapta1['state'] = 'disable'
            stanga1['state'] = 'disable'
            arunca1['state'] = 'disable'
            field.delete(p)
            p = field.create_image(field.coords(m2)[0] - 60, field.coords(m2)[1] - 20, image=banana, anchor=CENTER)
        else:
            player = 1
            dreapta2['state'] = 'disable'
            stanga2['state'] = 'disable'
            arunca2['state'] = 'disable'
            dreapta1['state'] = 'normal'
            stanga1['state'] = 'normal'
            arunca1['state'] = 'normal'
            field.delete(p)
            p = field.create_image(field.coords(m1)[0] - 60, field.coords(m1)[1] - 20, image=banana, anchor=CENTER)


def misca_dreapta1(poza):
    j = int((field.coords(poza)[0]) / 133) + 1 #bazat pe coordonata x a maimutei, determin numarul cladirii pe care se afla
    d = 0
    # Daca se afla in propria jumatate si daca nu se schimba cladirea pe care se afla si daca nu depaseste ultima cladire
    # atunci maimuta se va misca cu 10 pixeli la dreapta
    if field.coords(poza)[0] + 10 <= 532 and int((field.coords(poza)[0] + 10) / 133) + 1 == j and j <= 4:
        field.move(poza, 10, 0)
        field.move(p, 10, 0)
    #Daca se schimba cladirea:
    elif field.coords(poza)[0] + 10 <= 532 and int((field.coords(poza)[0] + 10) / 133) + 1 != j and j <= 4:
        #Daca viitoarea cladire are aceeasi inaltime cu cea actuala atunci miscarea se va desfasura normal
        if cladiri[j].height() == cladiri[j - 1].height():
            field.move(poza, 10, 0)
            field.move(p, 10, 0)
        #Daca viitoarea cladire are o inaltime diferita, maimuta, impreuna cu banana pe care o tine in mana se misca
        # corespunzator inaltimii cladirii viitoare
        elif cladiri[j - 1].height() > cladiri[j].height() and j <= 4:
            d = 120 + abs(field.coords(poza)[0] - j * 133)
            field.move(poza, d, abs(cladiri[j - 1].height() - cladiri[j].height()))
            field.move(p, d, abs(cladiri[j - 1].height() - cladiri[j].height()))
        elif cladiri[j - 1].height() < cladiri[j].height() and j <= 4:
            d = 120 + abs(field.coords(poza)[0] - j * 133)
            field.move(poza, d, -abs(cladiri[j - 1].height() - cladiri[j].height()))
            field.move(p, d, -abs(cladiri[j - 1].height() - cladiri[j].height()))


def misca_dreapta2(poza):
    j = int((field.coords(poza)[0]) / 133) + 1 - 2
    d = 0
    if field.coords(poza)[0] + 10 <= 1323.5 and int((field.coords(poza)[0] + 10) / 133) + 1 - 2 == j and j <= 8:
        field.move(poza, 10, 0)
        field.move(p, 10, 0)
    elif field.coords(poza)[0] + 10 <= 1323.5 and int((field.coords(poza)[0] + 10) / 133) + 1 - 2 != j:
        if cladiri[j].height() == cladiri[j - 1].height():
            field.move(poza, 10, 0)
            field.move(p, 10, 0)
        elif cladiri[j - 1].height() > cladiri[j].height():
            d = 120 + abs(field.coords(poza)[0] - (j + 2) * 133)
            field.move(poza, d, abs(cladiri[j - 1].height() - cladiri[j].height()))
            field.move(p, d, abs(cladiri[j - 1].height() - cladiri[j].height()))
        elif cladiri[j - 1].height() < cladiri[j].height():
            d = 120 + abs(field.coords(poza)[0] - (j + 2) * 133)
            field.move(poza, d, - abs(cladiri[j - 1].height() - cladiri[j].height()))
            field.move(p, d, - abs(cladiri[j - 1].height() - cladiri[j].height()))


def misca_stanga1(poza):
    if (field.coords(poza)[0] - 120) / 133 == int((field.coords(poza)[0] - 120)):
        j = (field.coords(poza)[0] - 120) / 133
    else:
        j = int((field.coords(poza)[0] - 120) / 133) + 1
    d = 0
    if field.coords(poza)[0] - 120 - 10 >= 0 and int((field.coords(poza)[0] - 120 - 10) / 133) + 1 == j and j >= 2:
        field.move(poza, -10, 0)
        field.move(p, -10, 0)
    elif field.coords(poza)[0] - 120 - 10 >= 0 and int((field.coords(poza)[0] - 120 - 10) / 133) + 1 != j and j >= 2:
        if cladiri[j - 2].height() == cladiri[j - 1].height():
            field.move(poza, -10, 0)
            field.move(p, -10, 0)
            j = int((field.coords(poza)[0] - 120) / 133) + 1
        elif cladiri[j - 2].height() < cladiri[j - 1].height():
            d = abs(134 - abs(field.coords(poza)[0] - j * 133))
            field.move(poza, -d, abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
            field.move(p, -d, abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
            j = int((field.coords(poza)[0] - 120) / 133) + 1
        elif cladiri[j - 2].height() > cladiri[j - 1].height():
            d = abs(134 - abs(field.coords(poza)[0] - j * 133))
            field.move(poza, -d, -abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
            field.move(p, -d, -abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
            j = int((field.coords(poza)[0] - 120) / 133) + 1
    elif field.coords(poza)[0] - 120 - 10 >= 0 and int((field.coords(poza)[0] - 120 - 10) / 133) + 1 == j and j == 1:
        field.move(poza, -10, 0)
        field.move(p, -10, 0)


def misca_stanga2(poza):
    if (field.coords(poza)[0] - 120) / 133 == int((field.coords(poza)[0] - 120)):
        j = (field.coords(poza)[0] - 120) / 133 - 2
    else:
        j = int((field.coords(poza)[0] - 120) / 133) + 1 - 2
    d = 0
    if field.coords(poza)[0] - 120 - 10 >= 768 and int(
            (field.coords(poza)[0] - 120 - 10) / 133) + 1 - 2 == j and j >= 6:
        field.move(poza, -10, 0)
        field.move(p, -10, 0)
    elif field.coords(poza)[0] - 120 - 10 >= 768 and int(
            (field.coords(poza)[0] - 120 - 10) / 133) + 1 - 2 != j and j >= 6:
        if cladiri[j - 2].height() == cladiri[j - 1].height():
            field.move(poza, -10, 0)
            field.move(p, -10, 0)
        elif cladiri[j - 2].height() < cladiri[j - 1].height():
            d = abs(120 - abs(field.coords(poza)[0] - j * 133))
            field.move(poza, -d, abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
            field.move(p, -d, abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
        elif cladiri[j - 2].height() > cladiri[j - 1].height():
            d = abs(120 - abs(field.coords(poza)[0] - j * 133))
            field.move(poza, -d, -abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
            field.move(p, -d, -abs(cladiri[j - 1].height() - cladiri[j - 2].height()))
    elif field.coords(poza)[0] - 120 - 10 >= 768 and int(
            (field.coords(poza)[0] - 120 - 10) / 133) + 1 - 2 == j and j == 5:
        field.move(poza, -10, 0)
        field.move(p, -10, 0)


pos1_text = StringVar()
pos2_text = StringVar()
unghi1_text = StringVar()
unghi2_text = StringVar()
viteza1_text = StringVar()
viteza2_text = StringVar()
# t reprezinta timpul. Este un nparray cu elemente egal distribuite intre 0 si 20.5 cu pasul de 0.5
t = np.arange(start=0, stop=20.5, step=0.5)
# tt este o lista care contine elementele din t
tt = t.tolist()
print(tt)

#Construirea peisajului: norii si caldirile, care sunt dispuse aleator
field = Canvas(window, width=1330, height=600, bg='#ADD8E6')
field.pack()
norisori = ImageTk.PhotoImage(Image.open('norisori.png'))
field.create_image(0, 0, image=norisori, anchor=NW)
cladire_mica = Image.open('Cladire_mica.png')
cladire_mare = Image.open('Cladire_inalta.png')
xq = 0
a = 0
k = 0
cladiri = []
c = []
for i in range(10):
    if i != 4 and i != 5:
        a = random.randint(1, 2)
        if a == 1:
            cladiri.append(ImageTk.PhotoImage(cladire_mica))
            c.append(field.create_image(xq, 552, image=cladiri[k], anchor=W))
        else:
            cladiri.append(ImageTk.PhotoImage(cladire_mare))
            c.append(field.create_image(xq, 456, image=cladiri[k], anchor=W))
        k += 1
    xq += 133

#Plasarea maimutelor pe cladirile din extremitati, coordonatele depinzand de tipul acestor cladiri
poza1 = Image.open('Maimutica1.png')
poza1 = poza1.resize((120, 100))
maimu1 = ImageTk.PhotoImage(poza1)
m1 = field.create_image(66.5 + 120 / 2, field.coords(c[0])[1] - (cladiri[0].height() / 2), image=maimu1, anchor=SE)
poza2 = Image.open('Maimuta2.png')
poza2 = poza2.resize((120, 100))
maimu2 = ImageTk.PhotoImage(poza2)
m2 = field.create_image(1263.5 + 120 / 2, field.coords(c[-1])[1] - (cladiri[-1].height() / 2), image=maimu2, anchor=SE)

#Spatiul cu date de la utilizator
input_frame = tkinter.Frame(window, width=1330, height=120)

player1_label = tkinter.Label(input_frame, text='Player1')
player1_label.grid(row=0, column=0, columnspan=7)
player2_label = tkinter.Label(input_frame, text='Player2')
player2_label.grid(row=0, column=7, columnspan=7)

player = random.randint(1, 2)
banan = Image.open('banana.png')
banan = banan.resize((50, 50))
banana = ImageTk.PhotoImage(banan)
if player == 1:
    p = field.create_image(field.coords(m1)[0] - 60, field.coords(m1)[1] - 20, image=banana, anchor=CENTER)
else:
    p = field.create_image(field.coords(m2)[0] - 60, field.coords(m2)[1] - 20, image=banana, anchor=CENTER)

#Fiecare buton apeleaza functia miscarii corespunzatoare. Toate contin text scris cu font arial si dimensiune 12
stanga1 = tkinter.Button(input_frame, text='<', command=lambda: misca_stanga1(m1), font=('arial', 12), justify=CENTER)
stanga1.grid(row=1, column=4)
pos1_label = tkinter.Label(input_frame, text='Pozitia maimutei 1')
pos1_label.grid(row=1, column=5)
dreapta1 = tkinter.Button(input_frame, text='>', command=lambda: misca_dreapta1(m1), font=('arial', 12),
                          justify=CENTER)
dreapta1.grid(row=1, column=6)
stanga2 = tkinter.Button(input_frame, text='<', command=lambda: misca_stanga2(m2), font=('arial', 12), justify=CENTER)
stanga2.grid(row=1, column=7)
pos1_label = tkinter.Label(input_frame, text='Pozitia maimutei 2')
pos1_label.grid(row=1, column=8)
dreapta2 = tkinter.Button(input_frame, text='>', command=lambda: misca_dreapta2(m2), font=('arial', 12), justify=CENTER)
dreapta2.grid(row=1, column=9)

unghi1 = tkinter.Entry(input_frame, font=('arial', 12), textvariable=unghi1_text, width=3, bg='#eee', bd=2,
                       justify=CENTER)
unghi1.grid(row=2, column=6)
unghi1_label = tkinter.Label(input_frame, text='Unghiul la care sa fie aruncata banana ')
unghi1_label.grid(row=2, column=5)
unghi2 = tkinter.Entry(input_frame, font=('arial', 12), textvariable=unghi2_text, width=3, bg='#eee', bd=2,
                       justify=CENTER)
unghi2.grid(row=2, column=9)
unghi2_label = tkinter.Label(input_frame, text='Unghiul la care sa fie aruncata banana ')
unghi2_label.grid(row=2, column=8)

viteza1 = tkinter.Entry(input_frame, font=('arial', 12), textvariable=viteza1_text, width=3, bg='#eee', bd=2,
                        justify=CENTER)
viteza1.grid(row=3, column=6)
viteza1_label = tkinter.Label(input_frame, text='Puterea cu care sa fie aruncata banana ')
viteza1_label.grid(row=3, column=5)
viteza2 = tkinter.Entry(input_frame, font=('arial', 12), textvariable=viteza2_text, width=3, bg='#eee', bd=2,
                        justify=CENTER)
viteza2.grid(row=3, column=9)
viteza2_label = tkinter.Label(input_frame, text='Puterea cu care sa fie aruncata banana ')
viteza2_label.grid(row=3, column=8)

arunca1 = tkinter.Button(input_frame, text='ARUNCA!', command=lambda: aruncare(), font=('arial', 12), justify=CENTER)
arunca1.grid(row=1, column=0, rowspan=4, columnspan=4)
arunca2 = tkinter.Button(input_frame, text='ARUNCA!', command=lambda: aruncare(), font=('arial', 12), justify=CENTER)
arunca2.grid(row=1, column=10, rowspan=4, columnspan=4)

# In functie de tura, butoanele se activeaza si se dezactiveaza
if player == 1:
    dreapta2['state'] = 'disable'
    stanga2['state'] = 'disable'
    dreapta1['state'] = 'normal'
    stanga1['state'] = 'normal'
else:
    dreapta2['state'] = 'normal'
    stanga2['state'] = 'normal'
    dreapta1['state'] = 'disable'
    stanga1['state'] = 'disable'

input_frame.pack()
window.mainloop()
