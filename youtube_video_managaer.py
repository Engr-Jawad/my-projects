import json
def load_data():
    try:
        with open ('youtube.txt','r') as file:
           test =  json.load(file)
        return test
           
    except FileNotFoundError :
        return []


def save_data(videos):
    with open ('youtube.txt','w') as file :
        json.dump(videos,file)



def list_all_videos(videos):
    for index,video in enumerate(videos,start=1):
        print("\n")
        print(f"{index}.  Video Name : {video['name']}, Durations : {video['time']}")
        print("_" * 30)

def add_videos(videos):
    name=input("enter the video name : ")
    time=input("enter the video length : ")
    videos.append({'name':name,'time':time})
    save_data(videos)




def  update_videos(videos):
    pass




def delete_videos(videos):
    pass




def main():
    videos=load_data()
    while(True):
        print("YOUTUBE MANAGER APP")
        print("1.list of the videos ")
        print("2.add youtube videos")
        print("3.update a youtube videos ")
        print("4.delete videos")
        print("5.exit")
        # print("choose your option in the above")
        choice=(input("enter  your choice here : "))
        
        
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