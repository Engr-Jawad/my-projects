def load_data():
    pass

def list_all_videos(videos):
    pass

def add_videos(videos):
    pass

def  update_videos(videos):
    pass

def delete_videos(videos):
    pass

def main():
    videos=[]
    while(True):
        print("welcome to the youtube manager app ")
        print("1.list of the videos ")
        print("2.add youtube videos")
        print("3.update a youtube videos ")
        print("4.delete videos")
        print("5.exit")
        print("choose your option in the above")
        choice=int(input("enter  your choice here : "))
        
        match choice:
            case '1':
                list_all_videos(videos)
            case '2':
                add_videos(videos)
            case '3':
                update_videos(videos)
            case '4':
                delete_videos(videos)
            case '5':
                break
            case _:
                print("invalid option")

if __name__ == "__main__":
    main()