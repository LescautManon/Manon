import sqlite3
from subprocess import run
from importlib import reload
from platform import system
from time import time
from random import shuffle
from subprocess import Popen
from json import load, dump
from os.path import exists
import download_update
import input_wait


def print_text():
    print("""\
menu: mistakes, pause, clear mistakes, update, exit
translate: time, show stat, pause, exit
mistakes: - (for delete sentence)

Present Simple
1. Subject + verb.
2. I, We, You, They + verb.
3. I, We, You, They + verb.
4. I, We, You, They + verb. He/She/It + verb + s.
5. I, We, You, They + verb.(5.1, 5.2, 5.3).
6. Want.(6).
7. I like + ...
8. Negative form. I, We, You, They + don't + verb.
9. I, We, You, They + don't + verb. He, She, It + doesn't + verb.
10. Need.
11. Test. (11.1, 11.2, 12.1, 12.2, 13.1, 13.2)
12. Questions. I, We, You, They. (14)
13. Questions. He, She, It. (15)
14. Questions. (16)
15. + / - / ?  (17)
16. Special Question. (18.1, 18.2)
17. Special Question. (19.1, 19.2)
18. Special Question. (20)
19. Questions. (21.1, 21.2)
20. Words (25) *
        """)


def screen_cleaning():
    p = Popen(clear, shell=True)
    p.communicate(input=b"\n")


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


def load_sentences():
    if enter == 'mistakes':
        cursor1.execute("SELECT rus FROM albums WHERE num_practice='0' ")
        rus_ = (cursor1.fetchall())
        cursor1.execute("SELECT eng FROM albums WHERE num_practice='0' ")
        eng_ = (cursor1.fetchall())
        return rus_, eng_
    else:
        cursor.execute(f"SELECT rus FROM albums WHERE num_practice='{enter}' ")
        rus_ = (cursor.fetchall())
        cursor.execute(f"SELECT eng FROM albums WHERE num_practice='{enter}' ")
        eng_ = (cursor.fetchall())
        return rus_, eng_


def normalize_list(rus_, eng_):
    for u, i_ in enumerate(rus_):
        rus_[u] = rus_[u][0]
        eng_[u] = eng_[u][0]
    return rus_, eng_


def show_stat():
    tm_ = (time() - tic) + tm_temp
    print("\n", " " * 1, int(tm_ / 60), " min ", round(tm_ % 60), " sec", sep="")
    print(" " * 1, f"{correctly_sentence} correctly / ", end="")
    print(f"{percent_mistakes_temp} mist / {pass_sentence} pass / {percent_mistakes} total")
    print(" " * 2, "percent mistakes:", round(100 / percent_mistakes * percent_mistakes_temp, 1))
    if len(list_mistakes) != 0:
        print()
        print("Mistakes:")
        for i_ in range(0, len(list_mistakes), 4):
            print(list_mistakes[i_], end=". ")
            print(list_mistakes[i_ + 1], end=" ")
            print(list_mistakes[i_ + 2])
            print(list_mistakes[i_ + 3])


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
added_practices = 20
enter = ''
while enter != 'exit':
    screen_cleaning()
    print_text()
    enter = input("Введи номер практики: ")
    screen_cleaning()
    flag = True
    if enter == 'mistakes':
        rus, eng = load_sentences()
        if len(rus) == 0:
            continue
    elif enter == 'pause':
        flag = False
        pause = read_pause()
        if pause == 0:
            continue
        setNum, enter, tm_temp = pause[0], pause[1], pause[2]
        rus, eng = load_sentences()
    elif enter == 'clear mistakes':
        cursor1.execute("DELETE FROM albums")
        cursor1.execute("VACUUM")
        conn.commit()
        continue
    elif enter == 'update':
        screen_cleaning()
        no_updates, no_internet = download_update.update_check()
        if no_internet or no_updates:
            input()
            continue
        update_main, update_download = download_update.update()
        input()
        if update_main:
            try:
                run(["python", "main.py"])
            except:
                Exception
            exit()
        if update_download:
            reload(download_update)
        input()
        continue
    elif enter.isdigit() and added_practices >= int(enter) > 0:
        rus, eng = load_sentences()
    else:
        continue
    if enter == 15:
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
        rus, eng = normalize_list(rus, eng)
        if flag:
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
        # translate = input()
        input_wait.prompt = str(len(setNum)) + ". " + str(rus[num]) + " "
        translate = input_wait.timed_input("")
        print()
        if str(type(translate)) == "<class 'NoneType'>":
            translate = ""
        if translate == "pause":
            pause = list(range(0, 3))
            tm_temp = (time() - tic) + tm_temp
            pause[0], pause[1], pause[2] = setNum, enter, tm_temp
            with open('pause.txt', 'w') as file:
                dump(pause, file)
            break
        if translate == "-" and enter == "mistakes":
            cursor1.execute("DELETE FROM albums WHERE eng = ?", (eng[num],))
            conn1.commit()
            setNum.remove(num)
            continue
        if translate == "time":
            tm = (time() - tic) + tm_temp
            print(" ", int(tm / 60), " min ", round(tm % 60), " sec", sep="")
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
        if not translate[0].istitle() or translate[-1] != ".":
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
