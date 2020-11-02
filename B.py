import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

TCP_IP = '127.0.0.1'
TCP_PORT = 5013
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

k = 'abcdefghijklmnop'

q = 2

iv = s.recv(BUFFER_SIZE)

length = s.recv(BUFFER_SIZE)

nr_blocuri = int(int(length)/16)
# print('NR BLOCURI', nr_blocuri)

message = s.recv(BUFFER_SIZE).decode()
# print(message)

key_encrypted = s.recv(BUFFER_SIZE)
# print(key_encrypted)
# print(type(key_encrypted))

decipher = AES.new(k.encode(), AES.MODE_ECB)
key = decipher.decrypt(key_encrypted)
# print('K2 decrypted', key)
# print(len(key))


i = 0
ct = 0
nr_bloc_curent = 0

string_received_from_a = ''

while i < int(length):
    if message == 'CBC':
        i += 16
        ct += 1
        nr_bloc_curent += 1

        if nr_bloc_curent % q ==0:
            # print('Blocul este din q')
            iv = s.recv(BUFFER_SIZE)
            key_encrypted = s.recv(BUFFER_SIZE)
            message = s.recv(BUFFER_SIZE).decode()
            decipher = AES.new(k.encode(), AES.MODE_ECB)
            key = decipher.decrypt(key_encrypted)

        ciphertext = s.recv(BUFFER_SIZE)

        # print('~~~~~DECRIPTARE CBC~~~~~')

        decipher = AES.new(key, AES.MODE_ECB)
        deciphertext = decipher.decrypt(ciphertext)

        xor = bytes([a ^ b for a, b in zip(deciphertext, iv)])
        iv = ciphertext
        # print('xor', xor)
        if ct == nr_blocuri:
            # print(unpad(xor, 16).decode())
            string_received_from_a += unpad(xor, 16).decode()
        else:
            # print(xor.decode())
            string_received_from_a += xor.decode()
    else:
        i += 16
        ct += 1
        nr_bloc_curent += 1

        if nr_bloc_curent % q == 0:
            # print('Blocul este din q')
            iv = s.recv(BUFFER_SIZE)
            key_encrypted = s.recv(BUFFER_SIZE)
            message = s.recv(BUFFER_SIZE).decode()
            decipher = AES.new(k.encode(), AES.MODE_ECB)
            key = decipher.decrypt(key_encrypted)

        ciphertext = s.recv(BUFFER_SIZE)

        # print('~~~~~DECRIPTARE OFB~~~~~')

        decipher = AES.new(key, AES.MODE_ECB)
        deciphertext = decipher.encrypt(iv)

        iv = deciphertext

        # print('deciphertext', deciphertext)
        # print(len(deciphertext))

        xor = bytes([a ^ b for a, b in zip(deciphertext, ciphertext)])
        if ct == nr_blocuri:
            # print(unpad(xor, 16).decode())
            string_received_from_a += unpad(xor, 16).decode()
        else:
            # print(xor.decode())
            string_received_from_a+= xor.decode()

print('String received from A:',string_received_from_a)

s.close()


