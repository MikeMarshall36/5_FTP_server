from perep_func import deshifr, shifr, calc_key
import socket
from threading import Thread
from random import randint
from contextlib import closing
from time import sleep
#Обмен необходимыми данными для генерации ключа (доп алгоритмов шифрования)
def gener(key_prim, key_publ_m):
    sleep(0.2)
    sock.send(str(key_publ_m).encode('utf-8'))
    key_publ_s = int(sock.recv(1024))
    key_part_m = calc_key(key_publ_m, key_prim, key_publ_s) 
    sleep(0.2)
    sock.send(str(key_part_m).encode('utf-8'))
    key_part_s = int(sock.recv(1024))
    return calc_key(key_part_s, key_prim, key_publ_s)
#Получение сообщений с сервера (вызывается в отдельном потоке)
def poluch():
    global flag
    while flag:
        try:
            inp=deshifr(sock.recv(2048).decode('utf-8'),key_full_s)
            if inp=='exit':
                print('server out')
                flag = False
            else:
                print('server:', inp)
        except OSError:
            flag = False
#Поиск свободного порта
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
'''
def send_file(name):
    with open(name) as file:
        text = file.read()
    sock.send(shifr(str(len(text)), key_full_s).encode('utf-8'))
    sock.send(shifr(text, key_full_s).encode('utf-8'))
def recv_file(name):
    length = deshifr(sock.recv(1024).decode('utf-8'),key_full_s)
    text = deshifr(sock.recv(int(length)).decode('utf-8'),key_full_s)
    with open(name) as file:
        file.write(text) 
#'''
flag = True
sock = socket.socket()
pr = find_free_port()
print('Your port: ', pr)
try:
    sock.bind(('', pr))
except OSError:
    print('Addr error')
    flag=False
if flag:
    sock.setblocking(1)
    nomser = 53480
    host='localhost'
    try:
        sock.connect((host, nomser))
        print('connection with server')
    except ConnectionRefusedError:
        print('Server not online')
        flag=False
if flag:
    key_full_s = int(gener(randint(128, 1024), randint(128, 1024)))
    stream = Thread(target= poluch)
    stream.start()
    while flag:
        msg=input('input your message: ')
        if msg == 'exitt':
            flag=False
        try:
            '''
            if msg[:7]=='copyCS ' or msg[:7]=='copySC ':
                msg=msg.split(' ')
                flag=False
                if msg[:7] == 'copyCS ':
                    send_file(msg[7:])
                elif msg[:7] == 'copySC ':
                    recv_file(msg[7:])
                stream = Thread(target= poluch)
                stream.start()
                flag=True
            else:#'''
            sock.send(shifr(msg, key_full_s).encode('utf-8'))
        except ConnectionResetError:
            flag=False
sock.close()
