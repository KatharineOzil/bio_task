# coding=utf-8
import getpass
import conn
from models import User, Admin


def login():
    print 'User Login'
    print '-' * 30
    name = raw_input('Enter your name: ')
    password = getpass.getpass('Enter your password: ')

    row = conn.c.execute('SELECT id, username, is_admin, password FROM user WHERE username=?', (name, ))
    user = row.fetchone()
    if not user:
        return False
    uid, name, is_admin, password_of_user = user
    if password == password_of_user:
        if not is_admin:
            user_instance = User(uid=uid, name=name)
        else:
            user_instance = Admin(uid=uid, name=name)
        return user_instance
    else:
        return False


def main():
    while 1:
        user = login()
        if not user:
            print 'Username and password not match.\n'
            continue
        else:
            print 'User \'%s\' login in.\n' % user.name
            user.choice_management()


if __name__ == '__main__':
    main()
