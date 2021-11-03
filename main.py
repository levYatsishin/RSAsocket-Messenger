from rsalib import generate_keys, decrypt_data, encrypt_data


if __name__ == "__main__":
    my_public_key, my_private_key = generate_keys()
    A = f'{"мама"*999}'.encode('utf-8')
    print(b"".join(decrypt_data(encrypt_data(A, my_public_key), my_private_key)) == A)
