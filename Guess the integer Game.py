import random

print("Welcome to play this game! ")

low = 0
high = 10000

Correct_answer = random.randint(low, high)

while True:
    try:
        Guess_answer = int(input("Please guess a whole number from 0 to 10000: "))
        if Guess_answer < Correct_answer:
            print("Too low! ")
        elif Guess_answer > Correct_answer:
            print("Too high! ")
        else:
            print("You are right! Good job! ")
            print("Thank you for playing! ")
            break
    except ValueError:
        print("Invalid input! Please re-enter a whole number! ")
