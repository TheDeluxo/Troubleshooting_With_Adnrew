# CollatzSequence.py

# from chapter 3 "Functions"

import sys

def collatz(num):
    try:
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
                collatz(res)
                res = collatz(res)
                if res == 1:
                    print("We've reached 1! Exiting...")
                    # break
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
                    # break
                    sys.exit()
    except ValueError:
        print ("I said A NUMBER!!!")
    return res


print("Welcome to the Collatz Sequencer!")
print("Please type a whole number to begin!")

inp = int(input())

collatz(inp)

# The task is described at the end of the page at this url:
# https://automatetheboringstuff.com/2e/chapter3/

