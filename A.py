import secrets
import socket
import time

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

TCP_IP = '127.0.0.1'
TCP_PORT = 5013
TCP_PORT1 = 5035
BUFFER_SIZE = 20

k = 'abcdefghijklmnop'

q = 2

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect((TCP_IP, TCP_PORT1))
message = r.recv(BUFFER_SIZE).decode()

key_encrypted = r.recv(BUFFER_SIZE)

# print(message)

iv = r.recv(BUFFER_SIZE)

# print('IV:', iv)

r.close()

decipher = AES.new(k.encode(), AES.MODE_ECB)
key_decrypted = decipher.decrypt(key_encrypted)
# print('K1 decrypted', key_decrypted)
# print(len(key_decrypted))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen()

conn, addr = s.accept()

with open('data.txt', 'r') as file:
    string = file.read().replace('\n', '')

length = len(string)

string_pad = pad(string.encode(),16)

conn.send(iv)
time.sleep(1)
conn.send(str(len(string_pad)).encode())
time.sleep(1)
conn.send(message.encode())
time.sleep(1)
conn.send(key_encrypted)
nr_bloc = 0

i = 0
j = 16

while i <= len(string_pad)-16 and j <= len(string_pad):
    if message == 'CBC':
        # print('~~~~~CRIPTARE CBC~~~~~')
        nr_bloc += 1
        # print('AM AJUNS LA BLOCUL', nr_bloc)

        if nr_bloc % q == 0:
            r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            r.connect((TCP_IP, TCP_PORT1))
            message = r.recv(BUFFER_SIZE).decode()

            key_encrypted = r.recv(BUFFER_SIZE)

            # print('Noul mesaj de la KM', message)

            iv = r.recv(BUFFER_SIZE)

            # print('Noul iv de la KM', iv)

            r.close()

            decipher = AES.new(k.encode(), AES.MODE_ECB)
            key_decrypted = decipher.decrypt(key_encrypted)

            conn.send(iv)
            time.sleep(1)
            conn.send(key_encrypted)
            time.sleep(1)
            conn.send(message.encode())
            time.sleep(1)

        string_to_be_crypted = ''
        string_to_be_crypted = string_pad[i:j]
        # print('string to be crypted', string_to_be_crypted)
        i += 16
        j += 16

        xor = bytes([a ^ b for a, b in zip(string_to_be_crypted, iv)])

        cipher = AES.new(key_decrypted, AES.MODE_ECB)
        ciphertext = cipher.encrypt(xor)

        iv = ciphertext

        # print('Ciphertext', ciphertext)

        conn.send(ciphertext)

        decipher = AES.new(key_decrypted, AES.MODE_ECB)
        deciphertext = cipher.encrypt(ciphertext)

    else:
        # print('~~~~~CRIPTARE OFB~~~~~')

        nr_bloc += 1
        # print('AM AJUNS LA BLOCUL', nr_bloc)
        if nr_bloc % q == 0:
            r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            r.connect((TCP_IP, TCP_PORT1))
            message = r.recv(BUFFER_SIZE).decode()

            key_encrypted = r.recv(BUFFER_SIZE)

            iv = r.recv(BUFFER_SIZE)

            r.close()

            decipher = AES.new(k.encode(), AES.MODE_ECB)
            key_decrypted = decipher.decrypt(key_encrypted)

            conn.send(iv)
            time.sleep(1)
            conn.send(key_encrypted)
            time.sleep(1)
            conn.send(message.encode())
            time.sleep(1)

        string_to_be_crypted = ''
        string_to_be_crypted = string_pad[i:j]
        # print('string to be crypted', string_to_be_crypted)
        i += 16
        j += 16

        cipher = AES.new(key_decrypted, AES.MODE_ECB)
        encryption = cipher.encrypt(iv)

        iv = encryption

        # print(encryption)

        ciphertext = bytes([a ^ b for a, b in zip(string_to_be_crypted, encryption)])

        # print(ciphertext)

        conn.send(ciphertext)

conn.close()
