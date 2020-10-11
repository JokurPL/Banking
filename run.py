#!/usr/bin/python3
import random

data = {}


def create_account():
    while True:
        """
            Generate card number with Luhn Algorithm 
        """
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

        if len(card_number) == 15 and 10 > sub >= 0:
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

    print("Your card has been created")

    print("Your card number:")
    print(elementary_card_number)

    print("Your card PIN:")
    print(pin)


def login(card_number: int, pin_number: int):
    if card_number == int(data['card_number']) and pin_number == int(data['pin_number']):
        print('You have successfully logged in!')
        while True:
            print("1. Balance\n2. Log out\n0. Exit")
            option = int(input())

            if option == 1:
                print('Balance: %s' % data['balance'])
            elif option == 2:
                print('You have successfully logged out!')
                break
            else:
                print('Bye!')
                return
    else:
        print('Wrong card number or PIN!')


if __name__ == "__main__":
    while True:
        option = int(input("1. Create an account\n2. Log into account\n3. Exit\n"))
        if option == 1:
            create_account()
        elif option == 2:
            login(int(input("Enter your card number:\n")), int(input("Enter your PIN:\n")))
        elif option == 3:
            break
