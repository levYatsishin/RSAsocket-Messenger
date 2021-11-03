import random
import time
random.seed(time.time())


def gcd(a, b):
    if b != 0:
        return gcd(b, a % b)
    else:
        return a


def extended_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, g = extended_gcd(b, a % b)
        return y, x - y * (a // b), g


def modular_pow(a, k, n):
    res = 1
    for _ in range(int(k)):
        res = (res * (a % n)) % n
    return res


def fast_modular_pow(a, k, n):
    res = 1
    while k != 0:
        if k % 2 == 1:
            res = (res * a) % n
            k -= 1
        else:
            a = (a * a) % n
            k //= 2
    return res


def generate_e(phi):
    e = random.randint(3, phi)
    while gcd(e, phi) != 1:
        e = random.randint(3, phi)
    return e


def generate_d(e, phi):
    d, _, _ = extended_gcd(e, phi)
    while d < 0:
        d += phi
    return d


def prime_test(p):
    if p % 2 == 0 and p != 2:
        return False
    for i in range(3, int(p ** 0.5), 2):
        if p % i == 0:
            return False
    return True


def fermat_prime_test(p, tests=20):
    for _ in range(tests):
        a = random.randint(2, p - 1)

        if fast_modular_pow(a, p-1, p) != 1:
            return False

    return True


def generate_prime(a, b):
    number = random.randint(a, b)
    while not fermat_prime_test(number):
        number = random.randint(a, b)

    return number


def generate_keys(key_size=1024):
    low_b, high_b = 2**(int(key_size / 2)-1), 2**(int(key_size / 2))

    p, q = generate_prime(low_b, high_b), generate_prime(low_b, high_b)
    while p == q:
        p, q = generate_prime(low_b, high_b), generate_prime(low_b, high_b)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_e(phi)
    d = generate_d(e, phi)
    return (e, n), (d, n)


def encrypt_number(a, public_key):
    return fast_modular_pow(a, public_key[0], public_key[1])


def decrypt_number(c, private_key):
    return fast_modular_pow(c, private_key[0], private_key[1])


def to_bytes(number):
    binary = bin(number)
    result = int(binary, 2).to_bytes((len(binary) + 5) // 8, byteorder='big')

    return result


def from_bytes(data):
    result = int.from_bytes(data, "big")
    return result


def split_bytes(data: bytes, max_length=127):
    return [data[i:i+max_length] for i in range(0, len(data), max_length)]


def encrypt_data(data, public_key):
    data = split_bytes(data)
    data = list(map(lambda a: from_bytes(a), data))
    data = list(map(lambda a: encrypt_number(a, public_key), data))
    data = list(map(lambda a: to_bytes(a), data))
    return data


def decrypt_data(data, private_key):
    data = list(map(lambda a: from_bytes(a), data))
    data = list(map(lambda a: decrypt_number(a, private_key), data))
    data = list(map(lambda a: to_bytes(a), data))

    return data

