import sqlite3
from platform import system
from subprocess import Popen
from os.path import exists
from json import load, dump
from itertools import chain
from random import shuffle
from time import time
from subprocess import run
from importlib import reload
import download_update
import datetime
#import input_wait


def print_Tense():
    print("""
    1. Present Simple
    2. Future Simple    
    """)


def showCommandMenu():
    strmenu = f"""\
menu: 1)mistakes({numberMistakes}), 2)pause({pEx}), 3)del pause, 4)clear mistakes, 5)update, 6)exit(q)
translate: 1)time, 2)show stat, 3)pause, 4)exit(q)
random {random} (for change enter "r+ / r-")
"""
    return strmenu


def print_text():
    print(f"""{showCommandMenu() if commandMenu == 1 else ""}
Present Simple
1. Subject + verb. (1)
2. I, We, You, They + verb. (2)
3. I, We, You, They + verb. (3)
4. I, We, You, They + verb. He/She/It + verb + s. (4)
5. I, We, You, They + verb. (5.1 - 5.3)
5.1 Предложения из теста 5, которые не встречаются в предыдущих практиках.
6. Want. (6)
7. I like + ... (7)
8. Negative form. I, We, You, They + don't + verb. (8)
9. I, We, You, They + don't + verb. He, She, It + doesn't + verb. (9)
10. Need. (10)
11. Test. (11.1 - 13.2)
11.1 Предложения из теста 11, которые не встречаются в предыдущих практиках.
12. Questions. I, We, You, They. (14)
13. Questions. He, She, It. (15)
14. Questions. (16)
15. + / - / ? (17)
16. Special Question. (18.1, 18.2)
17. Special Question. (19.1, 19.2)
18. Special Question. (20)
19. Questions. (21.1, 21.2)
20. Words. (25) *
21. Test. (22.1 - 25.5)
21.1 Предложения из теста 21, которые не встречаются в предыдущих практиках.
22. To be. (26)
23. To be. a/an + very + adjective + noun (one) (27.1, 27.2)
24. To be. so / such (28)
25. Numbers. (29)
26. To be. More difficult. (29.1, 29.2)
27. To be. Negative form. (30.1, 30.2)
28. To be. Questions. (31.1, 31.2)
29. To be. Questions. More difficult. (32.1, 32.2)
30. To be. Special Question. (33)
31. To be. Special Question. More difficult. (34.1, 34.2)
32. Words. Repeat. (38)
33. Test. (35.1 - 38.4)
33.1 Предложения из теста 33, которые не встречаются в предыдущих практиках.
34. Words (46, 47)
35. Test. (48)
36. Test. (39.1 - 48.4)
36.1 Предложения из теста 36, которые не встречаются в предыдущих практиках.
        """)


def print_FutureSimple():
    print(f"""{showCommandMenu() if commandMenu == 1 else ""}
Future Simple
1.
2.
3.
4.
""")


def screen_cleaning():
    p = Popen(clear, shell=True)
    p.communicate(input=b"\n")


def read_pause():
    pause_ = 0
    if exists('pause.txt'):
        with open('pause.txt', 'r') as f:
            return load(f)
    return pause_


def load_sentences(enter, XforLoadPause):
    if enter[-1] == 'm':
        cursor1.execute(f"SELECT rus FROM albums WHERE datetime = '{XforLoadPause}'  ")
        russian_sentences_ = (cursor1.fetchall())
        cursor1.execute(f"SELECT eng FROM albums WHERE datetime = '{XforLoadPause}'  ")
        english_sentences_ = (cursor1.fetchall())
        return russian_sentences_, english_sentences_

    cursor.execute(f"SELECT rus FROM albums WHERE num_practice='{enter}' ")
    russian_sentences_ = (cursor.fetchall())
    cursor.execute(f"SELECT eng FROM albums WHERE num_practice='{enter}' ")
    english_sentences_ = (cursor.fetchall()) 
    return russian_sentences_, english_sentences_


def normalize_list(russian_sentences_, english_sentences_):
    for u, i_ in enumerate(russian_sentences_):
        russian_sentences_[u] = russian_sentences_[u][0]
        english_sentences_[u] = english_sentences_[u][0]
    return russian_sentences_, english_sentences_


def show_stat():
    tm_ = (time() - tic) + tm_temp
    print("\n", f"Practice {enter}", sep="")
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


def numMist():
    date = showMistakes()
    global numberMistakes
    numberMistakes = len(date)


def pauseExists():
    pauseExists = read_pause()
    if pauseExists != 0:
        pauseExists = True
    global pEx
    if pauseExists == True:
        pEx = "exists"
    else:
        pEx = "none"


def showMistakes():
    cursor1.execute("SELECT datetime, num_practice FROM albums")
    date = (cursor1.fetchall())
    date = sorted(set(date), key=lambda d: date.index(d))
    practice = []
    for u, i_ in enumerate(date):
        practice.append(date[u][1])
        date[u] = date[u][0]
    for num, i in enumerate(date):
        print(str(num + 1)  + '.', 'Practice', str(practice[num]) + '.', i)
    print()
    return date


def loadMistakes(date, x):
    global XforLoadPause
    XforLoadPause = date[x]
    cursor1.execute(f"SELECT rus FROM albums WHERE datetime = '{date[x]}'  ")
    russian_sentences_ = (cursor1.fetchall())
    cursor1.execute(f"SELECT eng FROM albums WHERE datetime = '{date[x]}'  ")
    english_sentences_ = (cursor1.fetchall())
    return russian_sentences_, english_sentences_


def mistakesForPause(now):
    cursor1.execute(f"SELECT eng FROM albums WHERE datetime = '{now}'  ")
    english_sentences_ = (cursor1.fetchall())
    mistakes = english_sentences_
    for num, i in enumerate(mistakes):
        mistakes[num] = mistakes[num][0]
    return mistakes


if system() == "Windows":
    clear = "cls"
else:
    clear = "clear"
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
conn1 = sqlite3.connect("new_mistakes.db", isolation_level=None)
cursor1 = conn1.cursor()
commandMenu = 0
random = "off"
added_practices = 36
num_added_practices = [str(x) for x in range(1, added_practices+1)]
for_push_NAP = [5.1, 11.1, 21.1, 33.1, 36.1]
for i in for_push_NAP:
    num_added_practices.append(str(i))
enter = ''
exitEnterMenu = ['exit', 'q', ' 6']
returnMistakes = False
while not enter in exitEnterMenu:
    XforLoadPause = ''
    numMist()
    pauseExists()
    if returnMistakes:
        enter = "mistakes"
    else:
        screen_cleaning()
        print_text()
        enter = input("Введи номер практики или команду: ")
    screen_cleaning()
    pause_is_not_used = True
    if enter == 'mistakes' or enter == " 1":
        con = False
        while True:
            screen_cleaning()
            date = showMistakes()
            if len(date) == 0:
                con = True
                break
            enter = input("Введи номер: ")
            if enter == "q":
                enter = ''
                con = True
                returnMistakes = False
                break
            if enter == "":
                continue
            if enter.isdigit() and len(date) >= int(enter) > 0:
                russian_sentences, english_sentences = loadMistakes(date, int(enter) - 1)
                enter = str(enter) + "m"
                returnMistakes = True
                break
            else:
                continue
        if con:
            continue
        screen_cleaning()
    elif enter == 'pause' or enter == " 2":
        enter = 'pause'
        pause_is_not_used = False
        pause = read_pause()
        if pause == 0:
            continue
        setNum, enter, tm_temp, now, XforLoadPause = pause[0], pause[1], pause[2], pause[3], pause[4]
        russian_sentences, english_sentences = load_sentences(enter, XforLoadPause)
        mistakes = mistakesForPause(now)
    elif enter == 'clear mistakes' or enter == " 4":
        enter = 'clear mistakes'
        #проверка: записана ли пауза в ошибках?
        pause = read_pause()
        if pause != 0:
            XforLoadPause = pause[4]
        answer = False
        if XforLoadPause != None and XforLoadPause != '':
            while True:
                print('Пауза записана в ошибках. Очищение журнала ошибок приведет к удалению паузы. Продолжить? Y/n')
                answer = input()
                if answer == 'y' or answer == 'Y' or answer == "":
                    if system() == "Windows":
                        p = Popen("del pause.txt", shell=True)
                        p.communicate(input=b"\n")
                    else:
                        p = Popen("rm pause.txt", shell=True)
                        p.communicate(input=b"\n")
                    cursor1.execute("DELETE FROM albums")
                    cursor1.execute("VACUUM")
                    conn.commit()
                    break
                elif answer == 'n' or answer == 'N':
                    break
                else:
                    screen_cleaning()
                    continue
        if answer == "n" or answer == "N" or answer == 'y' or answer == 'Y' or answer == "":
            continue
        cursor1.execute("DELETE FROM albums")
        cursor1.execute("VACUUM")
        conn.commit()
        continue
    elif enter == 'update' or enter == " 5":
        enter == 'update'
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
    elif enter == 'r-':
        random = "off"
        continue
    elif enter == 'r+':
        random = "on"
        continue
    elif enter == 'del pause' or enter == ' 3':
        XforLoadPause = ''
        if system() == "Windows":
            p = Popen("del pause.txt", shell=True)
            p.communicate(input=b"\n")
            continue
        else:
            p = Popen("rm pause.txt", shell=True)
            p.communicate(input=b"\n")
            continue
    elif enter == '?':
        if commandMenu == 0:
            commandMenu = 1
        else:
            commandMenu = 0
        continue
    elif enter.replace(".", "", 1).isdigit() and enter in num_added_practices:
        russian_sentences, english_sentences = load_sentences(enter, XforLoadPause = 0)
    else:
        continue
    if enter == '15' and pause_is_not_used:
        if random == "off":
            setNum = [x for x in range(0, len(russian_sentences))]
        if random == "on":
            setNum = [[x for x in range(i, i+3)] for i in range(0, len(russian_sentences), 3)]
            shuffle(setNum)
            setNum = list(chain(*setNum))        
        tm_temp = 0
    else:
        if pause_is_not_used:
            setNum = [i for i in range(0, len(russian_sentences))]
            if random == "on":
                shuffle(setNum)
            tm_temp = 0      
    russian_sentences, english_sentences = normalize_list(russian_sentences, english_sentences)
    tic = time()
    list_mistakes = []
    percent_mistakes_temp = 0
    correctly_sentence = 0
    pass_sentence = 0
    percent_mistakes = len(setNum)
    if pause_is_not_used:
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y %H:%M:%S")
        mistakes = []
    while setNum:
        num = setNum[0]
        print(len(setNum), end=". ")
        print(russian_sentences[num], end=" ")
        #translate = input()
        input_wait.prompt = str(len(setNum)) + ". " + str(russian_sentences[num]) + " "
        translate = input_wait.timed_input("")
        print()
        if str(type(translate)) == "<class 'NoneType'>":
             translate = ""
        if translate == "?":
            print('1)time, 2)show stat, 3)pause, 4)exit(q)')
            continue
        if translate == "pause" or translate == " 3":
            pause = list(range(0, 5))
            tm_temp = (time() - tic) + tm_temp
            pause[0], pause[1], pause[2], pause[3], pause[4] = setNum, enter, tm_temp, now, XforLoadPause
            with open('pause.txt', 'w') as file:
                dump(pause, file)
            break
        if translate == "time" or translate == " 1":
            tm = (time() - tic) + tm_temp
            print(" ", int(tm / 60), " min ", round(tm % 60), " sec", sep="")
            continue
        if translate == "":
            print(english_sentences[num])
            pass_sentence += 1
            setNum.remove(num)
            continue
        if translate == "show stat" or translate == " 2":
            show_stat()
            print()
            continue
        if translate == "exit" or translate == "q" or translate == " 4":
            break
        if not translate[0].istitle() or translate[-1] != ".":
            if not translate[0].istitle():
                translate = translate[0].upper() + translate[1:]
            if translate[-1] != "." and english_sentences[num][-1] == ".":
                translate = translate + "."
            if translate[-1] != "?" and english_sentences[num][-1] == "?":
                translate = translate + "?"
        if translate == english_sentences[num]:
            correctly_sentence += 1
        if translate != english_sentences[num]:
            print(english_sentences[num])
            if english_sentences[num] not in mistakes and len(translate) != 0:
                temp = tuple([tuple([now]) + tuple([enter]) + tuple([russian_sentences[num]]) + tuple([english_sentences[num]])])
                cursor1.executemany("INSERT INTO albums VALUES (?,?,?,?)", temp)
                conn1.commit()
            list_mistakes.append(len(setNum))
            list_mistakes.append(russian_sentences[num])
            list_mistakes.append(translate)
            list_mistakes.append(english_sentences[num])
            percent_mistakes_temp += 1
        setNum.remove(num)
    if len(setNum) == 0:
        show_stat()
        input()
