import socket
import netlib
import socket
import netlib
import threading
from rsalib import generate_keys
import pickle

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, address = sock.accept()


def listen():
    global my_public_key, my_private_key, second_public_key, second_private_key

    while True:
        # must be decrypted with second_private_key

        answer = netlib.receive_encrypted_data(conn, second_private_key)
        if answer.decode("utf-8") == 'end':
            listen_thread._is_running = False
            send_thread._is_running = False
            # end the programme

        print(answer.decode("utf-8"))


def send():
    global my_public_key, my_private_key, second_public_key, second_private_key

    while True:
        # must be encrypted with my_public_key

        message = input()
        if message == 'end':
            netlib.send_encrypted_data(conn, my_public_key, message)
            # end the programme

        netlib.send_encrypted_data(conn, my_public_key, message)


#   getting the other public key and sending mine
second_public_key = pickle.loads(netlib.receive_data(conn, string=False))
my_public_key, my_private_key = generate_keys(1024)
netlib.send_data(conn, pickle.dumps(my_public_key), string=False)

#   getting other private key and sending mine
second_private_key = pickle.loads(netlib.receive_encrypted_data(conn, my_private_key))
netlib.send_encrypted_data(conn, second_public_key, pickle.dumps(my_private_key), string=False)

listen_thread = threading.Thread(target=listen)
send_thread = threading.Thread(target=send)
print("Connection was established successfully!")

listen_thread.start()
send_thread.start()
