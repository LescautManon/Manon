from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.error import URLError

version_main = 10
version_database = 2
version_download_update = 3
version_input_wait = 1
list_update = []


def update_check():
    no_updates = True
    no_internet = False
    try:
        check_version = urlopen("https://raw.githubusercontent.com/LescautManon/Manon/master/update.txt").read()
    except URLError:
        no_internet = True
        print("Возможно, нет подключения к интернету")
        return no_updates, no_internet
    check_version = check_version.decode('utf-8')
    check_version = check_version.split("\n")
    for i in check_version:
        if i.isdigit():
            list_update.append(int(i))
    if (list_update[0] > version_main
        or list_update[1] > version_database
            or list_update[2] > version_download_update
                or list_update[3] > version_input_wait):
        no_updates = False
        return no_updates, no_internet
    else:
        no_updates = True
        print("Обновлений нет")
        return no_updates, no_internet


def update():
    update_main = False
    update_download = False
    counter_updates = 0
    if len(list_update) == 0:
        print("Возможно, нет подключения к интернету")
        return update_main, update_download
    else:
        import re
    if list_update[0] > version_main:
        url = 'https://raw.githubusercontent.com/LescautManon/Manon/master/main.py'
        filename = "main.py"
        urlretrieve(url, filename)
        print('update main.py OK')
        old_version = version_main
        new_version = list_update[0]
        data = open('download_update.py').read()
        o = open('download_update.py', 'w')
        o.write(re.sub(f"version_main = {old_version}", f"version_main = {new_version}", data))
        o.close()
        counter_updates += 1
        update_main = True
    if list_update[1] > version_database:
        url = 'https://github.com/LescautManon/Manon/raw/master/mydatabase.db'
        filename = "mydatabase.db"
        urlretrieve(url, filename)
        print('update mydatabase.db OK')
        old_version = version_database
        new_version = list_update[1]
        data = open('download_update.py').read()
        o = open('download_update.py', 'w')
        o.write(re.sub(f"version_database = {old_version}", f"version_database = {new_version}", data))
        o.close()
        counter_updates += 1
    if list_update[2] > version_download_update:
        url = 'https://raw.githubusercontent.com/LescautManon/Manon/master/download_update.py'
        filename = "download_update.py"
        urlretrieve(url, filename)
        print('update download_update.py OK')
        old_version = version_download_update
        new_version = list_update[2]
        data = open('download_update.py').read()
        o = open('download_update.py', 'w')
        o.write(re.sub(f"version_download_update = {old_version}", f"version_download_update = {new_version}", data))
        o.close()
        counter_updates += 1
        update_download = True
    if list_update[3] > version_input_wait:
        url = 'https://raw.githubusercontent.com/LescautManon/Manon/master/input_wait.py'
        filename = "input_wait.py"
        urlretrieve(url, filename)
        print('update input_wait.py OK')
        old_version = version_input_wait
        new_version = list_update[3]
        data = open('download_update.py').read()
        o = open('download_update.py', 'w')
        o.write(re.sub(f"version_input_wait = {old_version}", f"version_input_wait = {new_version}", data))
        o.close()
        counter_updates += 1
        update_download = True
    if counter_updates == 0:
        print("Обновлений нет")
        return update_main, update_download
    else:
        print("Обновление завершено")
        return update_main, update_download
