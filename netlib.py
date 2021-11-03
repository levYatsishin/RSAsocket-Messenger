import rsalib
import pickle


def receive_bytes(conn, data_size):
    data = b""
    while len(data) < data_size:
        data += conn.recv(data_size - len(data))

    return data


def receive_data(conn, string=True):
    data_size = int.from_bytes(receive_bytes(conn, 4), 'big')
    data = receive_bytes(conn, data_size)
    if string:
        data = data.decode("utf-8")

    return data


def send_data(conn, data, string=True):
    if type(data) == str:
        string = True
    elif type(data) == bytes:
        string = False

    if string:
        data = data.encode('utf-8')

    conn.send(len(data).to_bytes(4, "big"))
    conn.send(data)


def send_encrypted_data(conn, public_key, message, string=True):
    #   encrypts given message and sends it in byte representation
    if type(message) == str:
        string = True
    elif type(message) == bytes:
        string = False

    if string:
        message = message.encode('utf-8')
    message = rsalib.encrypt_data(message, public_key)
    message = pickle.dumps(message)
    send_data(conn, message, string=False)


def receive_encrypted_data(conn, private_key) -> bytes:
    #   return received message in byte representation

    message = receive_data(conn, string=False)
    message = pickle.loads(message)
    message = rsalib.decrypt_data(message, private_key)
    message = b''.join(message)

    return message
