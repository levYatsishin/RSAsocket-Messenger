import socket
import netlib
import threading
from rsalib import generate_keys
import pickle

sock = socket.socket()
server_address = "127.0.0.1"
server_port = 9090
sock.connect((server_address, server_port))
print("Connecting...")


def listen():
    global my_public_key, my_private_key, second_public_key, second_private_key

    while True:
        # must be decrypted with second_private_key

        answer = netlib.receive_encrypted_data(sock, second_private_key)
        print(answer.decode("utf-8"))


def send():
    global my_public_key, my_private_key, second_public_key, second_private_key

    while True:
        # must be encrypted with second_public_key
        message = input()
        netlib.send_encrypted_data(sock, my_public_key, message, string=True)


#   generating and sending my public key
my_public_key, my_private_key = generate_keys(1024)
netlib.send_data(sock, pickle.dumps(my_public_key), string=False)

#   getting the other public key and sending my private(encrypted by other public key)
second_public_key = pickle.loads(netlib.receive_data(sock, string=False))
netlib.send_encrypted_data(sock, second_public_key, pickle.dumps(my_private_key), string=False)

#   getting other private key
second_private_key = pickle.loads(netlib.receive_encrypted_data(sock, my_private_key))


listen_thread = threading.Thread(target=listen)
send_thread = threading.Thread(target=send)
print("Connection was established successfully!")

listen_thread.start()
send_thread.start()
