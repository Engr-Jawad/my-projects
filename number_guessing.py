import random
number = random.randint(1,100)
while True:
    try:
        user_choice=int(input("guess the number between one and hundred : "))
    except:
        print("not valid value ")
    if user_choice < number :
        print("your guess is too low ")
    elif user_choice > number :
        print("your guess is too high")
    else:
        print("congratulations you got the number ")
    
    