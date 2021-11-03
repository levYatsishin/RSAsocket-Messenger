import socket
import netlib
import threading
from rsalib import generate_keys
import pickle

sock = socket.socket()
server_address = "127.0.0.1"
server_port = 9090
sock.connect((server_address, server_port))
print("Establishing connection with server...")


def connect_with_server():
    #   handshake with the server

    #   generating and sending my public key
    my_public_key_, my_private_key_ = generate_keys(1024)
    netlib.send_data(sock, pickle.dumps(my_public_key_), string=False)

    #   getting the servers public key and sending my private(encrypted by servers public key)
    servers_public_key = pickle.loads(netlib.receive_data(sock, string=False))
    netlib.send_encrypted_data(sock, servers_public_key, pickle.dumps(my_private_key_), string=False)

    #   getting servers private key
    servers_private_key = pickle.loads(netlib.receive_encrypted_data(sock, my_private_key_))

    return my_public_key_, my_private_key_, servers_public_key, servers_private_key


def log_in(encrypt_key, decrypt_key):
    login = input("Login: ")
    password = input("Password: ")
    message = pickle.dumps((login, password))

    netlib.send_encrypted_data(sock, encrypt_key, message)
    answer = netlib.receive_encrypted_data(sock, decrypt_key).decode('utf-8')
    print(answer)


#   connecting with server and getting rsa keys
my_public_key, my_private_key, server_public_key, server_private_key = connect_with_server()
log_in(my_public_key, server_private_key)
