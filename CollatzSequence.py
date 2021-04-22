# CollatzSequence.py

# from chapter 3 "Functions"

import sys

def collatz(num):
    num = int(num)
    print ("Last number in the sequence is " + str(num))
    if num == 1:
        print("The number is already 1! Exiting...")
        sys.exit()
    elif num % 2 == 0:
        print("This number is even")
        res = num // 2
        print("The result after the last iteration is " + str(res) + "\n")
        if res == 1:
            print("We've reached 1! Exiting...")
            sys.exit()
        while res != 1:
            res = collatz(res)
            if res == 1:
                print("We've reached 1! Exiting...")
                sys.exit()
    elif num % 2 == 1:
        print("This number is odd")
        res = 3 * num + 1
        print("The result after the last iteration is " + str(res) + "\n")
        if res == 1:
            print("We've reached 1! Exiting...")
            sys.exit()
        while res != 1:
            collatz(res)
            res = collatz(res)
            if res == 1:
                print("We've reached 1! Exiting...")
                sys.exit()
    return res


print("Welcome to the Collatz Sequencer!")
# print("Please type a whole number to begin!")
while True:
    try:
        for n in collatz(int(input("Please type a whole number to begin with!\n"))):
            print ("You've entered " + n + "for a starting number")
        break
    except ValueError:
        print("I said A NUMBER!!!")


# The task is described at the end of the page at this url:
# https://automatetheboringstuff.com/2e/chapter3/

