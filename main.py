import sqlite3
import importlib
from platform import system
from time import time
from random import shuffle
from subprocess import Popen
from json import load, dump
from os.path import exists
import download_update


def print_text():
    print(f"""\
use in main menu: mistakes, pause, clear mistakes, all practice, exit
use in translate: time, show stat, pause, exit
use in mistakes: time, show stat, pause, exit, -(for delete sentence)

1. Present Simple. Subject + verb.
2. Present Simple. I, We, You, They + verb.
3. Present Simple. I, We, You, They + verb.
4. Present Simple. I, We, You, They + verb. He/She/It + verb + s.
5. Present Simple. I, We, You, They + verb.(5.1, 5.2, 5.3).
6. Want.(6).
7. I like + ...
8. Present Simple (negative form). I, We, You, They + don't + verb.
9. I, We, You, They + don't + verb. He, She, It + doesn't + verb.
10. Need.
11. Test. (11.1, 11.2, 12.1, 12.2, 13.1, 13.2)
12. Present Simple. Questions. I, We, You, They. (14)
13. Present Simple. Questions. He, She, It. (15)
14. Present Simple. Questions. (16)
15. Present Simple. + / - / ?  (17)
16. Present Simple. Special Question. (18.1, 18.2)
17. Present Simple. Special Question. (19.1, 19.2)
18. Present Simple. Special Question. (20)
19. Present Simple. Questions. (21.1, 21.2)
20. Words (25) *
{state_update}
        """)


def text_cls():
    p = Popen(clear, shell=True)
    p.communicate(input=b"\n")


def clear_mistakes():
    cursor1.execute("DELETE FROM albums")
    cursor1.execute("VACUUM")
    conn.commit()


def read_pause():
    pause_ = 0
    if exists('pause.txt'):
        with open('pause.txt', 'a+') as f:
            f.seek(0)
            try:
                return load(f)
            except ValueError:
                pass
    return pause_


def normalize_list(rus_, eng_):
    for u, i_ in enumerate(rus_):
        rus_[u] = rus_[u][0]
        eng_[u] = eng_[u][0]
    return rus_, eng_


def show_stat():
    tm = (time() - tic) + tm_temp
    print("\n", " " * 1, int(tm / 60), " min ", round(tm % 60), " sec", sep="")
    print(" " * 1, f"{correctly_sentence} correctly / ", end="")
    print(f"{percent_mistakes_temp} mist / {pass_sentence} pass / {percent_mistakes} total")
    print(" " * 2, "percent mistakes:", round(100 / percent_mistakes * percent_mistakes_temp, 1))
    if len(list_mistakes) != 0:
        print()
        print("Mistakes:")
        for i in range(0, len(list_mistakes), 4):
            print(list_mistakes[i], end=". ")
            print(list_mistakes[i + 1], end=" ")
            print(list_mistakes[i + 2])
            print(list_mistakes[i + 3])


state_update = download_update.update_check()
if system() == "Windows":
    clear = "cls"
else:
    clear = "clear"
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
conn1 = sqlite3.connect("mistakes.db", isolation_level=None)
cursor1 = conn1.cursor()
cursor1.execute("SELECT eng FROM albums WHERE num_practice='0' ")
mistakes = (cursor1.fetchall())
for num, i in enumerate(mistakes):
    mistakes[num] = mistakes[num][0]
a = ''
while a != 'exit':
    text_cls()
    print_text()
    a = input("Введи номер практики: ")
    text_cls()
    value_a = ['mistakes', 'pause', 'all practice', 'clear mistakes', 'update']
    if a not in value_a and not a.isdigit():
        continue
    elif a.isdigit():
        a = int(a)
        if a < 1 or a > 20:
            continue
    flag = True
    if a == 'pause':
        flag = False
        pause = read_pause()
        if pause == 0:
            continue
        setNum, rus, eng, a, tm_temp = pause[0], pause[1], pause[2], pause[3], pause[4]
    if flag:
        if a == 'mistakes':
            cursor1.execute("SELECT rus FROM albums WHERE num_practice='0' ")
            rus = (cursor1.fetchall())
            cursor1.execute("SELECT eng FROM albums WHERE num_practice='0' ")
            eng = (cursor1.fetchall())
            if len(rus) == 0:
                continue
        elif a == 'all practice':
            cursor.execute("SELECT rus FROM albums")
            rus = (cursor.fetchall())
            cursor.execute("SELECT eng FROM albums")
            eng = (cursor.fetchall())
        elif a == 'clear mistakes':
            clear_mistakes()
            continue
        elif a == 'update':
            importlib.reload(download_update)
            state_update = download_update.update_check()
            text_cls()
            download_update.update_check()
            download_update.update()
            importlib.reload(download_update)
            state_update = download_update.update_check()
            input()
            continue
        elif True:
            cursor.execute(f"SELECT rus FROM albums WHERE num_practice='{a}' ")
            rus = (cursor.fetchall())
            cursor.execute(f"SELECT eng FROM albums WHERE num_practice='{a}' ")
            eng = (cursor.fetchall())
        rus, eng = normalize_list(rus, eng)
        if a == 15:
            setNum = [i for i in range(0, len(rus))]
            am = [[0] * 3 for i in range(int(len(setNum) / 3))]
            m = 0
            k = 0
            t = 0
            while m < len(setNum) / 3:
                if k < 3:
                    am[m][k] = setNum[t]
                    k += 1
                    t += 1
                else:
                    k = 0
                    m += 1
            shuffle(am)
            setNum = []
            for i in am:
                setNum.extend(i)
        else:
            setNum = [i for i in range(0, len(rus))]
            shuffle(setNum)
            tm_temp = 0
    tic = time()
    list_mistakes = []
    percent_mistakes_temp = 0
    correctly_sentence = 0
    pass_sentence = 0
    percent_mistakes = len(setNum)
    while setNum:
        num = setNum[0]
        print(len(setNum), end=". ")
        print(rus[num], end=" ")
        translate = input()
        if translate == "pause":
            pause = list(range(0, 5))
            tm_temp = (time() - tic) + tm_temp
            pause[0], pause[1], pause[2], pause[3], pause[4] = setNum, rus, eng, a, tm_temp
            with open('pause.txt', 'w') as file:
                dump(pause, file)
            break
        if translate == "-" and a == "mistakes":
            cursor1.execute("DELETE FROM albums WHERE eng = ?", (eng[num],))
            conn1.commit()
            setNum.remove(num)
            continue
        if translate == "time":
            tm = (time() - tic) + tm_temp
            print(" " * (len(rus[num]) + len(str(len(setNum))) + 2), int(tm / 60), " min ", round(tm % 60), " sec", sep="")
            continue
        if translate == "":
            print(eng[num])
            pass_sentence += 1
            setNum.remove(num)
            continue
        if translate == "show stat":
            show_stat()
            print()
            continue
        if translate == "exit":
            break
        if translate != "" and (not translate[0].istitle() or translate[-1] != "."):
            if not translate[0].istitle():
                translate = translate[0].upper() + translate[1:]
            if translate[-1] != "." and eng[num][-1] == ".":
                translate = translate + "."
            if translate[-1] != "?" and eng[num][-1] == "?":
                translate = translate + "?"
        if translate == eng[num]:
            correctly_sentence += 1
        if translate != eng[num]:
            print(eng[num])
            if eng[num] not in mistakes and len(translate) != 0:
                temp = tuple([tuple([0]) + tuple([rus[num]]) + tuple([eng[num]])])
                cursor1.executemany("INSERT INTO albums VALUES (?,?,?)", temp)
                conn1.commit()
            list_mistakes.append(len(setNum))
            list_mistakes.append(rus[num])
            list_mistakes.append(translate)
            list_mistakes.append(eng[num])
            percent_mistakes_temp += 1
        setNum.remove(num)
    if len(setNum) == 0:
        show_stat()
        input()
