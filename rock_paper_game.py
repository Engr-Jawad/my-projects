# #input from the user
# #computer random choice
# #print rersults

# # cases
# # case 1
# # rock->rock=Tie
# # rock->paper=paper win
# # rock->scissors=rock win


# # case 2
# # paper -> rock =paper win
# # paper -> paper =tie
# # paper -> scissors = scissors win 


# # case 3
# # scissors -> rock= rock win
# # scissors -> paper = scissors win 
# # scissors -> scissors =tie

# # # lets start coding
# import random
# # attempt=0
# # while(attempt < 5):
# list=['rock','paper','scissors']
# user_action=input("enter your choice (rock,paper,scissors) :")
# computer_action=random.choice(list)
# print(f"\n you chose {user_action},computer choice {computer_action}.\n")
# if user_action==computer_action:
#     print(f"both players selected {user_action}.its a tie !")
# elif user_action=='rock':
#     if computer_action == 'paper':
#         print("paper cover rock so computer wins ")
#     else:
#         print("rock  break the scissors so rock wins")
# elif user_action == 'paper':
#     if computer_action=='scissors':
#         print("scissors cut paper so computer wins")
#     else:
#         print("paper cover rock so paper wins")
# elif user_action=='scissors':
#     if computer_action=='rock':
#         print("rock break the scissors so computer wins")
#     else:
#         print("scissor cut paper so scissors wins")




# ##############################same code but below code have the gui  and the above code have not gui ##############
import random
import tkinter as tk

# Main window
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("400x300")

choices = ['rock', 'paper', 'scissors']

# Result label
result_label = tk.Label(root, text="Choose Rock, Paper, or Scissors",
                        font=("Arial", 12), pady=20)
result_label.pack()

def play(user_action):
    computer_action = random.choice(choices)

    if user_action == computer_action:
        result = f"Both chose {user_action}. It's a Tie!"
    elif user_action == 'rock':
        if computer_action == 'paper':
            result = "Paper covers Rock. Computer Wins!"
        else:
            result = "Rock breaks Scissors. You Win!"
    elif user_action == 'paper':
        if computer_action == 'scissors':
            result = "Scissors cut Paper. Computer Wins!"
        else:
            result = "Paper covers Rock. You Win!"
    elif user_action == 'scissors':
        if computer_action == 'rock':
            result = "Rock breaks Scissors. Computer Wins!"
        else:
            result = "Scissors cut Paper. You Win!"

    result_label.config(
        text=f"You chose: {user_action}\nComputer chose: {computer_action}\n\n{result}"
    )

# # Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

rock_btn = tk.Button(button_frame, text="Rock", width=20,
                     command=lambda: play('rock'))
paper_btn = tk.Button(button_frame, text="Paper", width=20,
                      command=lambda: play('paper'))
scissors_btn = tk.Button(button_frame, text="Scissors", width=20,
                         command=lambda: play('scissors'))

rock_btn.grid(row=0, column=0, padx=5)
paper_btn.grid(row=0, column=1, padx=5)
scissors_btn.grid(row=0, column=2, padx=5)

# Start GUI loop
root.mainloop()



























import tkinter as tk
from PIL import Image, ImageTk
import random

# ----------------- Game Logic -----------------
choices = ["rock", "paper", "scissors"]

def play(user_choice):
    computer_choice = random.choice(choices)

    result_text = f"You chose {user_choice}\nComputer chose {computer_choice}\n\n"

    if user_choice == computer_choice:
        result_text += "It's a Tie!"
    elif user_choice == "rock":
        if computer_choice == "paper":
            result_text += "Paper covers Rock\nComputer Wins!"
        else:
            result_text += "Rock breaks Scissors\nYou Win!"
    elif user_choice == "paper":
        if computer_choice == "scissors":
            result_text += "Scissors cut Paper\nComputer Wins!"
        else:
            result_text += "Paper covers Rock\nYou Win!"
    elif user_choice == "scissors":
        if computer_choice == "rock":
            result_text += "Rock breaks Scissors\nComputer Wins!"
        else:
            result_text += "Scissors cut Paper\nYou Win!"

    result_label.config(text=result_text)

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("400x450")

title = tk.Label(root, text="Rock Paper Scissors", font=("Arial", 18, "bold"))
title.pack(pady=10)

# ----------------- Load Images -----------------
rock_img = ImageTk.PhotoImage(Image.open("rock.png").resize((100, 100)))
paper_img = ImageTk.PhotoImage(Image.open("paper.png").resize((100, 100)))
scissors_img = ImageTk.PhotoImage(Image.open("scissors.png").resize((100, 100)))

# ----------------- Buttons -----------------
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

rock_btn = tk.Button(button_frame, image=rock_img, command=lambda: play("rock"))
rock_btn.grid(row=0, column=0, padx=10)

paper_btn = tk.Button(button_frame, image=paper_img, command=lambda: play("paper"))
paper_btn.grid(row=0, column=1, padx=10)

scissors_btn = tk.Button(button_frame, image=scissors_img, command=lambda: play("scissors"))
scissors_btn.grid(row=0, column=2, padx=10)

# ----------------- Result Label -----------------
result_label = tk.Label(root, text="", font=("Arial", 12), justify="center")
result_label.pack(pady=20)

root.mainloop()
rock.png
paper.png
scissors.png
