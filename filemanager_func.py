import os
import shutil
import zipfile
#'''
from perep_func import sent, reciver
#размер папки
def size(path):

    result = 0
    for directory, subdirectory, files in os.walk(path):
        if files:
            for file in files:
                path = directory + '\\'+file
                result += os.path.getsize(path)
    return result
#текущая рабочая директория
def current(dop):
    pathh = os.getcwd()+'\\'+dop[:-1]
    msg= (pathh+'\n')
    pathh = pathh.split('\\')
    return(msg+pathh[len(pathh)-1]+'\n', False)#'''


#'''
def sent(name, conn, key, user, max_size, dop):
    length = int(poluch(conn, key))#conn.recv(1024).decode()
    text = poluch(conn, key, razm=length)#conn.recv(int(length)).decode()
    with open(dop+name) as file:
        file.write(text)
    if max_size and size(user) > max_size:
        exterminate(name, dop)
        return 'Недостаточно места', False
    return 'получен файл '+name, 'file '+name+' was accepted'


def recv(name, conn, key, dop):
    with open(dop+name) as file:
        text = file.read()
    otprav(conn, str(len(text)), key)
    otprav(conn, text, key)
    return 'отправлен файл '+name,  'file '+name+' was sent'

def zip_in(file_name, user, max_size, dop):
    try:
        if zipfile.is_zipfile(dop+file_name):
            return('Он уже зазипован', False)
        else:
            z = zipfile.ZipFile(dop+file_name.split('.')[0]+'.zip', 'w')
            z.write(dop+file_name)
            z.close()
            if max_size and size(user) > max_size:
                exterminate(file_name, dop)
            return(file_name+' файл успешно зазипован', file_name+' was zipped')
    except FileNotFoundError:
            return('Не получилось найти файл', False)

def unzip(file_name, userr, max_size, dop):
    try:
        if zipfile.is_zipfile(dop+file_name):
            z = zipfile.ZipFile(dop+file_name, 'r')
            z.extractall()
            if max_size and size(userr) > max_size:
                    zazipovat(file_name, dop)
                    return 'Недостаточно места', False
            return(file_name+' файл успешно раззипован', file_name+' was dezipped')
        else:
            return('Не, это не зип', False)
    except FileNotFoundError:
            return('Не получилось найти файл', False)

#удалить директорию
def kill_it(dir_name, dop):#zashity ot duraka
    os.rmdir(dop+dir_name)
    return('Директория '+dir_name+' удалена', dir_name+' was delet')
#создать
def mkdir(dir_name, user, max_size, addit):
    if not os.path.isdir(addit+dir_name):
        os.umask(0)
        os.mkdir(addit+dir_name,0o777)
        if max_size and size(user) > max_size:
                kill_it(dir_name, dop)
                return 'Недостаточно места', False
        return('Директория с именем '+dir_name+' создана', 'dir'+dir_name+' was created')
    else:
        return('Нельзя сотворить две директории с одинаковыми именами!', False)

#содержимое файла
def open(file):
    list = os.listdir(file)
    msg=''
    for i in (list):
        msg+=str(i)+' '
    return(msg+'\n', False)

#создание файла
def touch(file_name, user, max_size, addit):
    if not os.path.isfile(addit+file_name):
        text_file = open(addit+file_name, 'w+')
        text_file.write('')
        os.startfile(addit+file_name)
        if max_size and size(user) > max_size:
            exterminate(file_name, dop)
            return 'Недостаточно места', False
        return('Сделаем!', 'file '+file_name+' was created')
    else:
        return('Здесь нельзя строить!', False)
#'''
def open_file(file_name, dop):
    msg=''
    try:
        with open(dop+file_name, 'r', encoding='utf-8') as file:
            msg+=(file)#*
    except FileNotFoundError:
            return('Не получилось найти файл', False)
    return(msg, False)#'''

def rename(old_Fname, new_Fname, dop):
    try:
        os.rename(dop+old_Fname, dop+new_Fname)
    except PermissionError:
        return(f'Не достаточно прав для переименования {old_Fname}', False)
    except:
        return(f'Файл {old_Fname} не найден', False)
    else:
        return(f'Файл {old_Fname} был переименован в {new_Fname}')

def remove(file_name, dop):
    os.remove(dop+file_name)
    return(f'Файл {file_name} был удалён!')

def moveto(file_name, dir_name, dop):
    try:
        os.replace(dop+file_name, dop+dir_name+'/'+file_name)
    except FileNotFoundError:
        try:
            os.replace(dop+file_name, dop[:dop.find('/')]+dir_name+'/'+file_name)
        except FileNotFoundError:
            return('Не получилось найти файл', False)
    return(f'Файл {file_name} был перемещён в директорию {dir_name}')

def copy_file(file_name, second_file, user, max_size, dop):
    try:
        shutil.copyfile(dop+file_name, dop+second_file)
    except FileNotFoundError:
            return('Не получилось найти файл', False)
    if max_size and size(user) > max_size:
            exterminate(second_file, dop)
            return 'Недостаточно места', False
    return('Файл '+file_name+' скопирован', 'file '+file_name+' like '+second_file)

def copy_folder(file_name, dir_name, userr, max_size, dop):
    if os.path.isdir(dop+dir_name):
        try:
            if max_size and size(userr)+os.path.getsize(dop+file_name) > max_size:
                return 'Недостаточно места', False
        except FileNotFoundError:
            return('Не получилось найти файл', False)
        try:
            shutil.copy(dop+file_name, dop+dir_name)
        except FileNotFoundError:
            try:
                shutil.copy(dop+file_name, dop[:dop.find('/')]+dir_name)
            except FileNotFoundError:
                return('Не получилось найти файл', False)
        return(f'Файл {file_name} был скопирован в директорию {dir_name}')
    else:
        return('Не получилось найти директорию', False)
def analise(cell, home, put,dop):

    put = put[:-2].split('\\')
    cell = cell.split('\\')
    if  len(put)<len(home):

        return(False)
    #el
    if cell[0] != home[0] and (cell[-1][-1] == ":"):
        return(False)
    else:#'''
        #cel = 
        k=0
        for i in home:
            #print(i, cel[k])
            if i != put[k]:
                return(False)
            k +=1
    dop=dop.split('\\')
    for i in cell:
        if i in home and (i in dop)==False:
            return(False)
    return(True)#'''
