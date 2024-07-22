import logging
import os.path
import re
import io
import tkinter as tk
from tkinter import filedialog

# import googleapiclient.discovery
from googleapiclient.discovery import build
from googleapiclient import http
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#Configuração básica do logger
logging.basicConfig(filename='Classroom.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

def remove_emojis(input_string):
    # Encontra o primeiro número, ponto ou letra após a remoção dos emojis
    match = re.search(r'[\d\.a-zA-Z]', input_string)
    if match:
        result = input_string[match.start():]
        return result
    else:
        return input_string

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly",
          "https://www.googleapis.com/auth/classroom.topics.readonly",
          "https://www.googleapis.com/auth/classroom.coursework.me",
          "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
          "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/drive"]


def get_creds():
    """Shows basic usage of the Classroom API.
       Prints the names of the first 10 courses the user has access to.
       """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_topic_name(topic_id, topics):
    topic_name = None
    for topic in topics['topic']:
        if topic['topicId'] == topic_id:
            topic_name = topic['name']
    remove_emojis(topic_name)
    return topic_name

def download_drive_file(file_id,drive_service,file_path):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = http.MediaIoBaseDownload(fh, request)
    done = False
    print("Downloading: ", (file_path.split("\\")[-1]))
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    f = open(file_path, "wb")
    f.write(fh.getbuffer())

def download_assets(drive_service,save_location,material_assets):

    if material_assets.get("driveFile"):
        try:
            file_id = material_assets["driveFile"]["driveFile"]["id"]
            file_name = material_assets["driveFile"]["driveFile"]["title"].replace(" ", "_")
            file_path = os.path.join(save_location, re.sub(r'["<>:/|\?]', "-",file_name))

            if not os.path.exists(save_location):
                os.makedirs(save_location)
            if not os.path.exists(file_path):
                download_drive_file(file_id=file_id, file_path=file_path,drive_service=drive_service)
            else:
                print(f"{os.path.basename(save_location)} already exists")
        except Exception as e:
            str = "Error: ",file_path, material_assets["driveFile"]["driveFile"]["title"], material_assets["driveFile"]["driveFile"]["alternateLink"]
            print(str)
            logging.error(str)

    elif "youtubeVideo" in material_assets.keys():
        try:
            yturl = material_assets["youtubeVideo"]["alternateLink"]
            yt_name = material_assets["youtubeVideo"]["title"]

            if not os.path.exists(save_location):
                os.makedirs(save_location)
                print(f"youtube-dl.exe {yturl} -o {os.path.join(save_location, yt_name)}")
                os.system(
                    f"youtube-dl.exe {yturl} -f mp4 -o \"{os.path.join(save_location, '%(title)s.%(ext)s')}\"")
        except Exception as e:
            str = "Error (youtubeVideo): ",save_location, yt_name, yturl
            print(str)
            logging.error(str)

# Download materials
def download_materials(save_path, course_name,drive_service, classroom_service, course_id):
    topics = classroom_service.courses().topics().list(courseId=course_id).execute()
    course_work_materials = classroom_service.courses().courseWorkMaterials().list(courseId=course_id).execute()

    if course_work_materials.get('courseWorkMaterial'):
        for material in course_work_materials['courseWorkMaterial']:
            if 'materials' in material.keys() and 'title' in material.keys():
                aula_name = material["title"].replace(" ", "_")
                for material_assets in material["materials"]:
                    if material.get("topicId"):
                        topic_name = remove_emojis(get_topic_name(topic_id=material["topicId"], topics=topics).replace(" ", "_"))
                        course_name = course_name.replace(" ", "_")
                        #os.getcwd() ou cloud_path
                        save_location = os.path.join(save_path, "Classroom_Downloads", re.sub(r'["<>:/|\?]', "-", course_name), re.sub(r'["<>:/|\?]', "-", topic_name),
                                                     re.sub(r'["<>:/|\?]', "-", aula_name))
                    else:
                        save_location = os.path.join(save_path, "Classroom_Downloads", re.sub(r'["<>:/|\?]', "-", course_name),
                                                     re.sub(r'["<>:/|\?]', "-", aula_name))
                    download_assets(drive_service,save_location,material_assets)
    else:
        pass

# Download activities
def download_activities(save_path, classroom_service,drive_service, course_name,course_id):
    course_works = classroom_service.courses().courseWork().list(courseId=course_id).execute()
    if course_works.get("courseWork"):
        for work in course_works["courseWork"]:
            if 'materials' in work.keys() and 'title'in work.keys():
                activity_name = work["title"]
                for material in work["materials"]:
                    save_dir = os.path.join(save_path, "Classroom_Downloads", re.sub(r'["<>:/|\?]', "-", course_name), "Activities",
                                            re.sub(r'["<>:/|\?]', "-", activity_name))
                    download_assets(drive_service,save_dir,material)


def main():

    # Tkinter initialization
    root = tk.Tk()
    root.withdraw()

    # Google AUTH Initialization
    creds = get_creds()
    classroom_service = build('classroom', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    courses = classroom_service.courses().list().execute()

    # Print the courses and ask the user to select the courses he wants to download
    for i, course in enumerate(courses["courses"], start=1):
        print(f"Num: {i} --> Course Name: { course['name']} - { course['id'] }")
        i=i+1
    opt = input("Please select the courses you want to download: (ex: 1,3 or 1,2,3): ")

    # Split the input and create a list of selected course IDs
    selected_ids = [int(id_) for id_ in opt.split(',')]

    # Ask the user if he wants to change the download location
    opt_dir = input("Do you want to change the download location? (y/n)")
    if(opt_dir == "y"):
        save_path = filedialog.askdirectory()
        print("Selected location: \n", save_path)
    else:
        save_path = os.getcwd()


    # Filter the courses based on the selected IDs
    # courses["courses"] = [course for course in courses["courses"] if course["id"] in selected_ids]    
    for i, course in enumerate(courses["courses"], start=1):
        if(i in selected_ids):
            course_name = course["name"]
            print(f"-- Downloading {course_name}...")
            actualcoursename = course_name.replace(" ", "_")
            actualcoursename = course_name.replace("|", "_")
            course_folder_path = os.path.join(save_path,"Classroom_Downloads", actualcoursename)
            if not os.path.exists(course_folder_path):
                os.makedirs(course_folder_path)

            course_id = course["id"]
            download_materials(save_path, actualcoursename,drive_service, classroom_service,course_id)
            download_activities(save_path, classroom_service,drive_service, actualcoursename,course_id)
            
            print(f"-- Download of { actualcoursename } complete! Check for errors at Classroom.log\n")
        else:
            print(f"-- Skipping download for {course['name']}")

if __name__ == '__main__':
    main()
