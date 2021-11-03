import socket
import time

import netlib
import os

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, address = sock.accept()

netlib.send_data(conn, "Commands:"
                       "\n1. [client/server]_ls - list server/client files"
                       "\n2. download <file name> - download file from server"
                       "\n3. upload <path to file> - upload file to server"
                       "\n4. disconnect - disconnect from server"
                       "\n5. shutdown - kill server and disconnect"
                       "\n6. help - to access this list")
while True:
    client_answer = netlib.receive_data(conn)

    if client_answer == 'shutdown':
        # close connection
        netlib.send_data(conn, "disconnect")
        time.sleep(1)
        break

    elif client_answer == "disconnect":
        netlib.send_data(conn, "disconnect")
        conn, address = sock.accept()
        netlib.send_data(conn, "Commands:"
                               "\n1. ls - list server files"
                               "\n2. download <file name> - download file from server"
                               "\n3. upload <path to file> - upload file to server"
                               "\n4. disconnect - disconnect from server"
                               "\n5. shutdown - kill server")

    elif client_answer == 'server_ls':
        list_of_files = os.popen("ls ftp/server_files").read()
        netlib.send_data(conn, list_of_files)

    elif client_answer.split()[0] == 'download':
        try:
            if client_answer.split()[1]:
                with open(f"ftp/server_files/{client_answer.split()[1]}", 'rb') as file:
                    data = file.read()
            else:
                data = f"Please enter file name"
        except FileNotFoundError:
            data = f"File {client_answer.split()[1]} does not exist"

        except IndexError:
            data = f"Please enter file name"
        if type(data) is bytes:
            netlib.send_data(conn, data, string=False)
        else:
            netlib.send_data(conn, data)

    elif client_answer.split()[0] == 'upload':
        data = netlib.receive_data(conn, string=False)
        try:
            if data.decode('utf-8') == 'error':
                continue
        except UnicodeDecodeError:
            with open(f"ftp/server_files/{client_answer.split()[1]}", 'wb') as file:
                file.write(data)

    elif client_answer == 'help':
        netlib.send_data(conn, "Commands:"
                               "\n1. [client/server]_ls - list server/client files"
                               "\n2. download <file name> - download file from server"
                               "\n3. upload <path to file> - upload file to server"
                               "\n4. disconnect - disconnect from server"
                               "\n5. shutdown - kill server and disconnect"
                               "\n6. help - to access this list")
    else:
        netlib.send_data(conn, "Unknown command")


conn.close()
