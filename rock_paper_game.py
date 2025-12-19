#input from the user
#computer random choice
#print rersults

# cases
# case 1
# rock->rock=Tie
# rock->paper=paper win
# rock->scissors=rock win


# case 2
# paper -> rock =paper win
# paper -> paper =tie
# paper -> scissors = scissors win 


# case 3
# scissors -> rock= rock win
# scissors -> paper = scissors win 
# scissors -> scissors =tie

# lets start coding
import random
list=['rock','paper','scissors']
user_action=input("enter your choice (rock,paper,scissors) :")
computer_action=random.choice(list)
print(f"\n you chose {user_action},computer choice {computer_action}.\n")
if user_action==computer_action:
    print(f"both players selected {user_action}.its a tie !")
elif user_action=='rock':
    if computer_action == 'paper':
        print("paper cover rock so computer wins ")
    else:
        print("rock  break the scissors so rock wins")
elif user_action == 'paper':
    if computer_action=='scissors':
        print("scissors cut paper so computer wins")
    else:
        print("paper cover rock so paper wins")
elif user_action=='scissors':
    if computer_action=='rock':
        print("rock break the scissors so computer wins")
    else:
        print("scissor cut paper so scissors wins")
        