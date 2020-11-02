import random
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

TCP_IP = '127.0.0.1'
TCP_PORT1 = 5035
BUFFER_SIZE = 20

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.bind((TCP_IP, TCP_PORT1))

print('Listening')

k = 'abcdefghijklmnop'

while True:
    r.listen()
    conn, addr = r.accept()
    random_number = random.randint(1,2)
    if random_number == 1:
        message = 'CBC'
    elif random_number == 2:
            message = 'OFB'
    print(message)

    conn.send(message.encode())


    k1 = get_random_bytes(16)
    k2 = get_random_bytes(16)

    cipher = AES.new(k.encode(), AES.MODE_ECB)
    k1_encrypted = cipher.encrypt(k1)

    cipher = AES.new(k.encode(), AES.MODE_ECB)
    k2_encrypted = cipher.encrypt(k2)

    if message == 'CBC':
        conn.send(k1_encrypted)
    else:
        conn.send(k2_encrypted)

    iv = get_random_bytes(16)
    conn.send(iv)

conn.close()