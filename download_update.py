from urllib.request import urlretrieve
from urllib.request import urlopen

def update_check():
    version_main = 1

    list_update = []
    check_version = urlopen("https://raw.githubusercontent.com/LescautManon/Manon/master/update.txt").read()
    check_version = check_version.decode('utf-8')
    for i in check_version:
        if i.isdigit():
            list_update.append(int(i))

    if list_update[0] > version_main:
        return "Вышла новая версия. Для обновления введи 'update'"
    else:
        return ""

##if list_update[0] > version_main:
##    url = 'https://raw.githubusercontent.com/LescautManon/Manon/master/main.py'
##    filename = "main.py"
##    urlretrieve(url, filename)
##    print('OK')
##
##
##    old_version = version_main
##    new_version = version_main + 1
##
##    import re
##    data = open('download.py').read()
##    o = open('download.py','w')
##    o.write(re.sub(f"version_main = {old_version}", f"version_main = {new_version}", data))
##    o.close()
