from urllib.request import urlretrieve
from urllib.request import urlopen

version_main = 1
version_database = 0
list_update = []
def update_check():
    check_version = urlopen("https://raw.githubusercontent.com/LescautManon/Manon/master/update.txt").read()
    check_version = check_version.decode('utf-8')
    for i in check_version:
        if i.isdigit():
            list_update.append(int(i))
    if list_update[0] > version_main \
    or list_update[1] > version_database:
        return "Вышла новая версия. Для обновления введи 'update'"
    else:
        return ""
    
def update():
    counter_updates = 0
    if list_update[0] > version_main:
        url = 'https://raw.githubusercontent.com/LescautManon/Manon/master/main.py'
        filename = "main.py"
        urlretrieve(url, filename)
        print('update main.py OK')
        old_version = version_main
        new_version = version_main + 1
        import re
        data = open('download_update.py').read()
        o = open('download_update.py','w')
        o.write(re.sub(f"version_main = {old_version}", f"version_main = {new_version}", data))
        o.close()
        counter_updates += 1


    if list_update[1] > version_database:
        url = 'https://github.com/LescautManon/Manon/raw/master/mydatabase.db'
        filename = "mydatabase.db"
        urlretrieve(url, filename)
        print('update mydatabase.db OK')
        old_version = version_database
        new_version = version_database + 1
        import re
        data = open('download_update.py').read()
        o = open('download_update.py','w')
        o.write(re.sub(f"version_database = {old_version}", f"version_database = {new_version}", data))
        o.close()
        counter_updates += 1

    if counter_updates == 0:
        print("Обновлений нет")
    else:
        print("Обновление завершено")
