"""
..................................................................................PROJECT BUILDING..........................................................................
HERE we use the dictionary in this project and dictionary stores  data in the form of keys and values  and on the left side we have keys and on the right side we have values 
............................................In this program we have six  functions...........................................................................................
first_one adding a student 
2nd_one  updating a student
3rd_one deleteing a student
4th_one displaying all student
5th_one exiting a student
6th_one main function
......................
IF ELSE
in this project we also use if else conditions that mainly work in the main functions 
............................................................................LETS STARTPROJECTS...............................................................................
"""

student_dict={  }

# adding student 
def add_stuent(name,grade):
    student_dict[name]=grade
    print(f"added student {name} with a grade {grade}")
    
def update_student(name,grade):
    if name in student_dict:
        student_dict[name]=grade
        print(f"{name} with  marks are updated {grade}")
    else:
        print("student {name} is not found ")
        
def delete_Student(name):
    if name in student_dict:
        del student_dict[name]
        print(f"{name} is successfully deleted ")
    else:
        print("not found ")
        
def display_all_student():
    if student_dict:
        for name,grade in student_dict.items():
            print(f"{name} : {grade}")
            
    else:
        print("no student found ")
        
       
def main():
    while(True):
        print("\n\nSTUDENT GRADE MANGAMENT SYSTEM")
        print("1.add a student")
        print("2.update student")
        print("3.delete student")
        print("4.view student")
        print("5.exit")
        
        choice=int(input("enter your choice from one to five :"))
        if choice == 1:
            name=input("enter student name : ")
            grade=int(input("enter student grade :"))
            print("\n")
            add_stuent(name,grade)
            
        elif choice == 2:
            name=input("enter student name : ")
            grade=int(input("enter student grade :"))
            print("\n")
            update_student(name,grade)
            
        elif choice == 3 :
            name=input("enter the student name : ")
            print("\n")
            delete_Student(name)
           
        elif choice == 4 :
            display_all_student()
            
        elif choice == 5 :
            print("program closed......")
        else:
            print("invalid choice")
            
main()
        