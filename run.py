#!/usr/bin/python3
import random, sqlite3, sys
import os.path
from os import path

data = {}


def database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS card(
                  id integer primary key,
                  number text not null,
                  pin text not null ,
                  balance integer default 0
                  )""")
        return cursor, conn
    except NameError:
        print(NameError)


def create_account(cursor, conn):
    """
    Create an account with:
        card number generate with Luhna Alghoritm,
        PIN number
    :return:
    """
    while True:
        card_number = ""
        ai = ""
        for n in range(0, 9):
            n += 1
            r = random.randint(0, 9)
            ai += str(r)
            elementary_card_number = "400000" + ai

        counter = 1
        for n in elementary_card_number:
            if not counter % 2 == 0:
                n = int(n) * 2
            card_number += str(n)
            counter += 1

        support_card_number = ""
        for n in card_number:
            if int(n) > 9:
                n -= 9
            support_card_number += str(n)

        k = int(support_card_number)
        tab_numbers = []
        while not k == 0:
            last_number = k % 10
            k = (k - last_number) / 10
            tab_numbers.append(int(last_number))

        sum = 0
        for number in tab_numbers:
            sum += number

        sub = 60 - int(sum)

        repeat = False
        try:
            test_card_number = str(elementary_card_number) + str(sub)
            test_card_number = int(test_card_number)
            cursor.execute("SELECT * FROM card")
            for value in cursor.fetchall():
                if test_card_number == value[2]:
                    repeat = True
        except ValueError:
            continue

        if len(card_number) == 15 and 10 > sub >= 0 and not repeat:
            break

    elementary_card_number += str(sub)
    elementary_card_number = int(elementary_card_number)

    pin = ""
    for n in range(0, 4):
        n += 1
        r = random.randint(0, 4)
        pin += str(r)

    balance = 0

    data.update({'card_number': elementary_card_number, 'pin_number': pin, 'balance': balance})
    cursor.execute(f'INSERT INTO card(number, pin, balance) VALUES ("{elementary_card_number}", {pin}, {balance})')
    conn.commit()
    print("Your card has been created")

    print("Your card number:")
    print(elementary_card_number)

    print("Your card PIN:")
    print(pin)


def login(card_number: int, pin_number: int, cursor, conn):
    cursor.execute("SELECT * FROM card")
    success = False
    for value in cursor.fetchall():
        if card_number == int(value[1]) and pin_number == int(value[2]):
            print('You have successfully logged in!')
            success = True
            break

    if success:
        while True:
            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
            user_menu_option = int(input())

            if user_menu_option == 1:
                cursor.execute(f'SELECT balance FROM card WHERE number == {card_number}')
                balance = cursor.fetchone()
                print('Balance: %s' % balance)
            elif user_menu_option == 2:
                cursor.execute(f'SELECT balance FROM card WHERE number == {card_number}')
                balance = cursor.fetchone()
                print("Enter income:")
                income_input = int(input())
                if income_input > 0:
                    income = income_input + int(balance[0])
                    cursor.execute(f'UPDATE card SET balance = {income} WHERE number == {card_number} ')
                    conn.commit()
                    print("Income was added!")
                else:
                    print("Income must be greater than 0!")
            elif user_menu_option == 3:
                card_number_to_transfer = int(input("Transfer\nEnter card number:"))
                cursor.execute("SELECT * FROM card")
                exists = False
                for value in cursor.fetchall():
                    if card_number_to_transfer == int(value[1]):
                        exists = True
                        break
                if exists:
                    money_to_transfer = int(input("Enter how much money you want to transfer:"))
                    cursor.execute(f'SELECT balance FROM card WHERE number == {card_number}')
                    balance = cursor.fetchone()[0]
                    if balance > money_to_transfer > 0:
                        new_balance = balance - money_to_transfer
                        cursor.execute(f'UPDATE card SET balance = {new_balance} WHERE number = {card_number}')
                        conn.commit()

                        cursor.execute(f'SELECT balance FROM card WHERE number == {card_number_to_transfer}')
                        new_balance_receiver = cursor.fetchone()[0] + money_to_transfer
                        cursor.execute(f'UPDATE card SET balance = {new_balance_receiver} WHERE number = {card_number_to_transfer}')
                        conn.commit()

                        print("Success!")
                    else:
                        print("Not enough money")
                else:
                    check_card = str(card_number_to_transfer)[:15]
                    luhn_card = ""
                    counter = 1
                    for number in check_card:
                        if not counter % 2 == 0:
                            number = int(number) * 2
                        luhn_card += str(number)
                        counter += 1

                    luhn_card_step_two = ""
                    for number in luhn_card:
                        if int(number) > 9:
                            number -= 9
                        luhn_card_step_two += number

                    amount = 0
                    for number in luhn_card_step_two:
                        amount += int(number)

                    last_number = str(card_number_to_transfer)[:1]
                    amount += int(last_number)
                    if amount % 10 == 0:
                        print("Such a card does not exist.")
                    else:
                        print("Probably you made a mistake in the card number. Please try again!")
            elif user_menu_option == 4:
                cursor.execute(f'DELETE FROM card WHERE number == {card_number}')
                conn.commit()
                print("The account has been closed!")
            elif user_menu_option == 5:
                print('You have successfully logged out!')
                break
            else:
                print('Bye!')
                sys.exit()
    else:
        print("Wrong card number or PIN!")


if __name__ == "__main__":
    cur, conn = database("./card.s3db")
    while True:
        option = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
        if option == 1:
            create_account(cur, conn)
        elif option == 2:
            login(int(input("Enter your card number:\n")), int(input("Enter your PIN:\n")), cur, conn)
        elif option == 0:
            sys.exit()
