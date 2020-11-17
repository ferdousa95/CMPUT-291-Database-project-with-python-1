import sqlite3
from Database import Database
from datetime import date
import sys

"""The first screen of your system should provide options for both registered and unregistered users to login. 
Registered users should be able to login using a valid user id and password, 
respectively denoted with uid and pwd in table users. 
Unregistered users should be able to sign up by providing a unique uid and additionally
a name, a city, and a password. Passwords are not encrypted in this project. 
The field crdate should be set by your system to the current date. After a successful login or signup, 
users should be able to perform the subsequent operations (possibly chosen from a menu) as discussed next."""
# class Initialization:
#     def __init__(self):
#         self.db = sqlite3.connect('D:/Pycharm Projects/Databases/reddit.sqlite')
#         self.cursor = db.cursor()
db = Database()

def user_login():
    # Get login details from user
    loggingin = True
    while loggingin:
        registered_user = input('Welcome to Tidder! Do you have an account? (Y/N)').lower()
        if registered_user == 'Y' or registered_user == 'yes' or registered_user[0] == 'y':

            user = input('User: ').lower()
            password = input('Password: ')

            # Execute sql statement and grab all records where the "uid" and
            # "pwd" are the same as "user" and "password"
            db.c.execute('SELECT name FROM users WHERE uid = ? AND pwd = ?', (user, password))
            username = db.c.fetchall()

            # If nothing was found then c.fetchall() would be an empty list, which
            # evaluates to False
            if username:
                print('Welcome, ' + username[0][0] + '!')
                loggingin = False #bug where after logging in u log in again
            else:
                print('Login failed, please try again')
        elif registered_user == 'N' or registered_user == 'no' or registered_user[0] == 'n':
            registered_user = input('Would you like to make an account? (Y/N)').lower()
            if registered_user == 'Y' or registered_user == 'yes' or registered_user[0] == 'y':
                usercheck = 'n'
                user = 'default'
                """
                MAKING A BLOCK TO MAKE SURE YOU FIX THE WHILE LOOP UNDERNEATH
                NEEDS TO ALSO CHECK USERNAME IS ONLY 4 CHARACTERS
                """
                while usercheck[0] != 'y':
                    user = input('Please enter a username. Must be 4 characters. >')
                    usercheck = input('Is ' + user + ' correct? (Y/N)').lower()
                else:
                    namecheck = 'n'
                    while not namecheck[0] == 'y':
                        name = input('Please enter your full name. >')
                        namecheck = input('Is ' + name + ' correct? (Y/N)').lower()
                    else:
                        citycheck = 'n'
                        while not citycheck[0] == 'y':
                            city = input('Please enter your city. >')
                            citycheck = input('Is ' + city + ' correct? (Y/N)').lower()
                        password = None
                        password2 = 1
                        while password != password2:
                            password = input('Please enter your password. >')
                            password2 = input('Enter your password again. >')
                        else:
                            today = date.today()
                            db.c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (user, name, password, city, today))
                            db.commit()
                            print('Congradulations! You have made a Tidder account.')
                            check = input('Would you like to login? (Y/N)')
                            if check == 'Y' or check == 'yes' or check[0] == 'y':
                                user = input('User: ').lower()
                                password = input('Password: ')

                                # Execute sql statement and grab all records where the "uid" and
                                # "pwd" are the same as "user" and "password"
                                try:
                                    db.c.execute('SELECT name FROM users WHERE uid = ? AND pwd = ?', (user, password))
                                except Exception as e:
                                    print(Exception)
                                username = db.c.fetchall()

                                # If nothing was found then c.fetchall() would be an empty list, which
                                # evaluates to False
                                if username:
                                    print('Welcome, ' + username[0][0] + '!')
                                    loggingin = False
                                else:
                                    print('Login failed, please try again')
                            else:
                                print('Okay then why did you make an account?? Peace tho')
            else:
                print("Okay then why did you open this program??")
        else:
            print('Ending the program.')
            loggingin = False
    return user


def checkPrivilege(userid):
    pass
