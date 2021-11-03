def write_new_login(cur, connection, login, password):
    cur.execute("SELECT login FROM logins WHERE login=?;", (login, ))
    if cur.fetchall():
        return False

    q = "INSERT INTO logins (login, password) VALUES (?, ?);"
    cur.execute(q, (login, password))
    connection.commit()

    return True


def check_login_and_password(cur, login, password):
    q = "SELECT login, password FROM logins WHERE login=? AND password=?;"
    cur.execute(q, (login, password))
    record = cur.fetchone()
    return True if record else False
