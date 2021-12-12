#функции для обмена сообщениями
#шифрование
def shifr(text, k):
    return ''.join(map(chr, [(x + k) % 65535 for x in map(ord, text)]))


def deshifr(text, k):
    return ''.join(map(chr, [(x - k) % 65535 for x in map(ord, text)]))
#более сложный вариант
'''
from binascii import hexlify, unhexlify
from itertools import cycle
def shifr(shifrovka, key):
    cipher = xor_str(shifrovka, key)
    return (hexlify(cipher.encode())).decode()

def deshifr(shifrovka, key):
    shifrovka = (unhexlify(shifrovka.encode())).decode()
    return xor_str(shifrovka, key)


def xor_str(a, b):
    return ''.join([chr(ord(x)^ord(y)) for x, y in zip(a, cycle(b))])#'''
def calc_key(key_g, key_ab, key_p):
    return key_g ** key_ab % key_p
'''
def Number_To_Fraze(key, divisor):
    keyl=[]
    lenn=0
    while key !=0:
        keyl.append(key%divisor)
        key=key//divisor
        lenn+=1
        print(''.join([chr(keyl[i]) for i in range(lenn)]))
    return ''.join([chr(keyl[i]) for i in range(lenn)])#'''
#отправление сообщений
def sent(drkto, msg, key):

    drkto.send(shifr(msg,key).encode('utf-8'))#+'\n'
#получение
def reciver(kto, key, razm=2048):#key_full_s - client

            return deshifr(kto.recv(razm).decode('utf-8'),key)

