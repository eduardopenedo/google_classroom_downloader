from __future__ import print_function

import os.path
import re
import io

# import googleapiclient.discovery
from googleapiclient.discovery import build
from googleapiclient import http
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

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
    return topic_name


def download_drive_file(file_id,drive_service,file_path):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = http.MediaIoBaseDownload(fh, request)
    done = False
    print(file_path.split("\\")[-1])
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    f = open(file_path, "wb")
    f.write(fh.getbuffer())


def download_assets(drive_service,save_location,material_assets):
    if material_assets.get("driveFile"):
        file_id = material_assets["driveFile"]["driveFile"]["id"]
        file_name = material_assets["driveFile"]["driveFile"]["title"]
        file_path = os.path.join(save_location, file_name)

        if not os.path.exists(save_location):
            os.makedirs(save_location)
        try:
            if not os.path.exists(file_path):
                download_drive_file(file_id=file_id, file_path=file_path,drive_service=drive_service)
            else:
                print(f"{os.path.basename(save_location)} already exists")
        except Exception as e:
            print(e)

    elif "youtubeVideo" in material_assets.keys():
        yturl = material_assets["youtubeVideo"]["alternateLink"]
        yt_name = material_assets["youtubeVideo"]["title"]

        if not os.path.exists(save_location):
            os.makedirs(save_location)
            print(f"youtube-dl.exe {yturl} -o {os.path.join(save_location, yt_name)}")
            os.system(
                f"youtube-dl.exe {yturl} -f mp4 -o \"{os.path.join(save_location, '%(title)s.%(ext)s')}\"")


def download_materials(course_name,drive_service, classroom_service, course_id):
    topics = classroom_service.courses().topics().list(courseId=course_id).execute()
    course_work_materials = classroom_service.courses().courseWorkMaterials().list(courseId=course_id).execute()

    if course_work_materials.get('courseWorkMaterial'):
        for material in course_work_materials['courseWorkMaterial']:
            aula_name = material["title"]

            if 'materials' in material.keys():
                for material_assets in material["materials"]:
                    if material.get("topicId"):
                        topic_name = get_topic_name(topic_id=material["topicId"], topics=topics)
                        save_location = os.path.join(os.getcwd(), "Classroom Downloads", re.sub(r'["<>:/|\?]', "-", course_name), re.sub(r'["<>:/|\?]', "-", topic_name),
                                                     re.sub(r'["<>:/|\?]', "-", aula_name))
                    else:
                        save_location = os.path.join(os.getcwd(), "Classroom Downloads", re.sub(r'["<>:/|\?]', "-", course_name),
                                                     re.sub(r'["<>:/|\?]', "-", aula_name))
                    download_assets(drive_service,save_location,material_assets)
    else:
        pass


def download_activities(classroom_service,drive_service, course_name,course_id):
    course_works = classroom_service.courses().courseWork().list(courseId=course_id).execute()
    if course_works.get("courseWork"):
        for work in course_works["courseWork"]:
            activity_name = work["title"]
            if 'materials' in material.keys():
                for material in work["materials"]:
                    save_dir = os.path.join(os.getcwd(), "Classroom Downloads", re.sub(r'"[<>:/|\?]', "-", course_name), "Activities",
                                            re.sub(r'"[<>:/|\?]', "-", activity_name))
                    download_assets(drive_service,save_dir,material)


def main():
    creds = get_creds()

    classroom_service = build('classroom', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    courses = classroom_service.courses().list().execute()

    for course in courses["courses"]:
        course_name = course["name"]
        course_folder_path = os.path.join(os.getcwd(),"Classroom Downloads", course_name)
        if not os.path.exists(course_folder_path):
            os.makedirs(course_folder_path)

        course_id = course["id"]
        download_materials(course_name,drive_service, classroom_service,course_id)
        download_activities(classroom_service,drive_service, course_name,course_id)


if __name__ == '__main__':
    main()