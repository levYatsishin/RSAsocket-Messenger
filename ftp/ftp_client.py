import socket
import os
import netlib

sock = socket.socket()
server_address = "127.0.0.1"
server_port = 9090
sock.connect((server_address, server_port))

print(netlib.receive_data(sock))
while True:
    data_to_send = input("user> ")
    if data_to_send == "client_ls":
        print(os.popen("ls ftp/client_files").read())
        continue

    elif data_to_send.split()[0] == 'upload':
        m = f"File was successfully transmitted"
        netlib.send_data(sock, data_to_send)
        try:
            if os.path.exists(f"ftp/client_files/{data_to_send.split()[1]}"):
                with open(f"ftp/client_files/{data_to_send.split()[1]}", 'rb') as file:
                    data = file.read()
                    netlib.send_data(sock, data, string=False)
            else:
                m = f"File {data_to_send.split()[1]} does not exist"

        except IndexError:
            m = f"Please enter file name"

        print(m)
        continue

    netlib.send_data(sock, data_to_send)
    server_answer = netlib.receive_data(sock, string=False)

    if data_to_send.split()[0] == 'download':
        try:
            print(server_answer.decode('utf-8'))
        except UnicodeDecodeError:
            with open(f"ftp/client_files/{data_to_send.split()[1]}", 'wb') as file:
                file.write(server_answer)
            print(f"{data_to_send.split()[1]} downloaded")

    elif server_answer.decode('utf-8') == 'disconnect' or server_answer.decode('utf-8') == 'shutdown':
        # close connection

        break

    else:
        print(server_answer.decode('utf-8'))

sock.close()
