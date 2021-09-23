import sqlite3
import code
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# cursor.execute(f"SELECT eng FROM albums WHERE num_practice = 11")
cursor.execute(f"SELECT eng FROM albums")
eng = (cursor.fetchall())

all_words = []
for u, i_ in enumerate(eng):
    eng[u] = eng[u][0]
    eng[u] = eng[u][:-1]
    eng[u] = eng[u].lower()
    all_words.extend(eng[u].split(" "))


# all_words = list(set(all_words))
all_words = sorted(set(all_words), key=lambda d: all_words.index(d))

#убрать точку из слов *убрать :
for num, i in enumerate(all_words):
    if i[-1] == "." or i[-1] == "?":
        all_words[num] = i[:-1]
for num, i in enumerate(all_words):
    if "\'s" in i or "\'d" in i or "\'m" in i:
        all_words[num] = i[:-2]
for num, i in enumerate(all_words):
    if i[-1] == ")":
        all_words[num] = i[:-1]
for num, i in enumerate(all_words):
    if i[0] == "(":
        all_words[num] = i[1:]
for num, i in enumerate(all_words):
    if i[-1] == "s" and i[:-1] in all_words:
        all_words[num] = i[:-1]
try:
    all_words.remove("/")
    # all_words.remove("it's")
except:
    Exception

all_words = sorted(set(all_words), key=lambda d: all_words.index(d))





print(all_words)
print(len(all_words))





#################################################
cursor.execute(f"SELECT rus FROM albums")
rus = (cursor.fetchall())

cursor.execute(f"SELECT eng FROM albums")
eng = (cursor.fetchall())

for u, i_ in enumerate(eng):
    eng[u] = eng[u][0]
    rus[u] = rus[u][0]

# with open('39 - 48.txt', encoding="utf8") as File:
#     data = []
#     for line in File:
#         data.append(line)
# with open('new eng.txt', encoding="utf8") as File:
#     data_new_eng = []
#     for line in File:
#         m = line.split(' ')
#         m.pop(0)
#         data_new_eng.append(' '.join(m))
# with open('new rus.txt', encoding="utf8") as File:
#     data_new_rus = []
#     for line in File:
#         data_new_rus.append(line)

#u = 0
#all_the_practice = []
#for num, i in enumerate(data):
#    if i[:-1] in eng:
        # print(str(num+1) + ".", rus[eng.index(i[:-1])], i, end = "")
        # print(str(num+1) + ".", rus[eng.index(i[:-1])], i, end = "")
        # l = rus[eng.index(i[:-1])] + " " + i[:-1]
        # l = rus[eng.index(i[:-1])]
        # l = i[:-1]
        # all_the_practice.append(l)
        # pass
#    else:
        # pass
        #print(str(num+1) + ". " + data_new_rus[u][:-1] + " " + data_new_eng[u][:-1])
        # l = data_new_rus[u][:-1] + " " + data_new_eng[u][:-1]
        # l = data_new_rus[u][:-1]
        # l = data_new_eng[u][:-1]
        # all_the_practice.append(l)
        # print(str(num+1) + ".", i, end= "")
        # u+=1

#print(u)


#for i in all_the_practice:
#    print(i)




cursor.execute(f"SELECT eng FROM albums WHERE num_practice = 5")
eng1 = (cursor.fetchall())
cursor.execute(f"SELECT rus FROM albums WHERE num_practice = 5")
rus1 = (cursor.fetchall())


for u, i_ in enumerate(eng1):
    eng1[u] = eng1[u][0]
    rus1[u] = rus1[u][0]


all_p_e = []
all_p_r = []
for i in range(1, 5):
    cursor.execute(f"SELECT eng FROM albums WHERE num_practice = {str(i)}")
    xeng = (cursor.fetchall())
    cursor.execute(f"SELECT rus FROM albums WHERE num_practice = {str(i)}")
    xrus = (cursor.fetchall())
    for u, i_ in enumerate(xeng):
        xeng[u] = xeng[u][0]
        xrus[u] = xrus[u][0]
    all_p_e.extend(xeng)
    all_p_r.extend(xrus)


f = 0
c = 0
for num, i in enumerate(eng1):
    if i in all_p_e:
        f+=1
    else:
        c+=1
        # print(i)
        # print(rus1[num])






code.interact(local=locals())
# не забывать что строчка с текстом может содержать несколько предложений на русском и английском.


