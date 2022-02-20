import random

def generate_number():    
    return random.sample([x for x in range(10)], 4)

def check_number(number, guess):
    a, b = 0, 0

    for i in range(4):
        for j in range(4):
            if guess[i] == number[j]:
                if i == j:
                    a += 1
                else:
                    b += 1

    return a, b

number = generate_number()
count = 0
status = []
while True:
    count += 1
    while True:
        guess = input("Input a 4 digit number: ")
        if guess.isdecimal() and len(guess) == 4:
            guess = [int(x) for x in guess]
            break
    a, b = check_number(number, guess)
    status.append((count, "".join([str(x) for x in guess]), a, b))
    for s in status:
        print(f'({s[0]}) {s[1]} -> {s[2]}A{s[3]}B')

    if a == 4:
        break
