import socket
import netlib
import threading
from rsalib import generate_keys
import pickle
import sqlite3
import sqllib

sock = socket.socket()
sock.bind(('', 9090))
sock.listen()

#   list with all connections and private/public keys
connections = []


def process_new_connections():
    sqlite_connection = sqlite3.connect('database.sqlite')
    cursor = sqlite_connection.cursor()
    global connections
    #   connects users to the server

    while True:
        conn, address = sock.accept()

        #   getting the other public key and sending mine
        clients_public_key = pickle.loads(netlib.receive_data(conn, string=False))
        my_public_key, my_private_key = generate_keys(1024)
        netlib.send_data(conn, pickle.dumps(my_public_key), string=False)

        #   getting other private key and sending mine
        clients_private_key = pickle.loads(netlib.receive_encrypted_data(conn, my_private_key))
        netlib.send_encrypted_data(conn, clients_public_key, pickle.dumps(my_private_key), string=False)

        #   saving connection + servers&clients public&private keys
        connections.append((conn, (my_public_key, my_private_key), (clients_public_key, clients_private_key)))

        login_password = pickle.loads(netlib.receive_encrypted_data(conn, clients_private_key))
        login, password = login_password[0], login_password[1]

        if not sqllib.check_login_and_password(cursor, login, password):
            netlib.send_encrypted_data(conn, my_public_key, f"Login or password is incorrect")
        else:
            netlib.send_encrypted_data(conn, my_public_key, f"Successfully logged in as {login}")


new_connections = threading.Thread(target=process_new_connections)

new_connections.start()
