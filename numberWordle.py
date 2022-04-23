import random
from itertools import permutations

digits = "0123456789"
operators = "+-/*"
characters = digits + operators


minValue = 10
maxValue = 200

def is_valid(expression):
    if expression[0] in "+/*0-": return False
    if expression[4] in operators: return False
    for n, char in enumerate(expression):
        if char in operators:
            if n != 0 and expression[n - 1] in operators: return False
            if n != 4 and expression[n + 1] in operators: return False
        if char == "0":
            if n != 0 and expression[n - 1] in operators: return False
        if char == "1":
            if (n == 0 or expression[n - 1] in operators):
                if (n == 4 or expression[n + 1] in operators):
                    if (n != 0 and expression[n - 1] in "*/"):
                        return False
                    if (n != 4 and expression[n + 1] == "*"):
                        return False
    result = eval("".join(expression))
    if (minValue < result < maxValue) and round(result) == result: return True
    return False


def make_green(char):
    return "\033[92;1m{}\033[0m".format(char)


def make_yellow(char):
    return "\033[93;1m{}\033[0m".format(char)


def make_gray(char):
    return "\033[37;2m{}\033[0m".format(char)


def make_bold(char):
    return "\033[1m{}\033[0m".format(char)


def color_guess(guess, actual):
    hint = ""
    for guess_char, actual_char in zip(guess, actual):
        if guess_char == actual_char:
            hint += make_green(guess_char)
        elif guess_char in actual:
            times_green = len([
                i for i, char in enumerate(guess) if
                char == guess_char and actual[i] == guess_char
            ])
            occurences = actual.count(guess_char)
            if occurences > times_green:
                hint += make_yellow(guess_char)
            else:
                 hint += make_gray(guess_char)
        else:
            hint += make_gray(guess_char)
    return hint

print("Welcome to Mathdle")

print("Expression must have five characters")
print()
loop = True
while loop:


    possibles = permutations(characters, 5)
    valid = filter(is_valid, possibles)
    equations = [{
        "expression": "".join(p), "result": eval("".join(p))
    } for p in valid]
    equation = random.choice(equations)


    print("Find the expression that equals: {}".format(make_bold(equation["result"])))
    print()
    guess_number = 1
    while True:
        guess = input("Guess {}: ".format(guess_number))
        if len(guess) != 5:
            print("Expression must have five characters")
        elif any(c for c in guess if c not in characters) or not is_valid(guess):
            print("Not a valid guess")
        elif eval(guess) != equation["result"]:
            print("That doesn't equal {}".format(equation["result"]))
        elif guess != equation["expression"]:
            print(color_guess(guess, equation["expression"]))
            print()
            guess_number += 1
            if guess_number > 6:
                print("It was {}".format(equation["expression"]))
                break
        else:
            print(color_guess(guess, equation["expression"]))
            print("Congratulations!")
            break
    playAgain = input("Do you want to play again? Y/YES/N/NO: ").upper()
    if playAgain == "N" or playAgain == "NO":
        loop = False
    while playAgain != "N" and playAgain != "NO" and playAgain != "Y" and playAgain != "YES":
        playAgain = input("Enter Y, YES, N or NO: ").upper()
    print()