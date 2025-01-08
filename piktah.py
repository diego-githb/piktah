import os
import random
import io
import tkinter as ui
from PIL import Image, ImageTk, ExifTags
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request  

# Constants
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DISPLAY_TIME = 10000  
MAX_IMAGE_SIZE = (300, 300)
TRANSPARENCY = 0.6
#The google drive folder ID is located in the url of the folder when viewed from a web browser. It's the portion of the url after 'https://drive.google.com/drive/folders/' and before the question mark '?'
GOOGLE_DRIVE_FOLDER_ID = '________________replace_me__________________'

# Authenticate and get credentials
def authenticate_user():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_id.json", SCOPES)
            creds = flow.run_local_server(port=0, access_type="offline")
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

# Main application class for the image shuffler
class ImageShuffler:
    def __init__(self, root, creds):
        self.root = root
        self.service = build('drive', 'v3', credentials=creds)
        self.images = self.load_images(GOOGLE_DRIVE_FOLDER_ID)
        self.image_queue = [] 
        self.label = ui.Label(root, bg="black")
        self.label.pack(fill="both", expand=True)
        self.show_image()

    def load_images(self, folder_id):
        results = self.service.files().list(
            q=f"'{folder_id}' in parents and (mimeType='image/jpeg' or mimeType='image/png')",
            spaces='drive',
            fields='files(id, name)').execute()
        return results.get('files', [])

    def show_image(self):
     if not self.image_queue:
        # Shuffle the images and refill the queue when it's empty
        self.image_queue = random.sample(self.images, len(self.images))

     file = self.image_queue.pop(0)  
     request = self.service.files().get_media(fileId=file['id'])
     fh = io.BytesIO()
     downloader = MediaIoBaseDownload(fh, request)
     done = False
     while not done:
         status, done = downloader.next_chunk()
     fh.seek(0)
     img = Image.open(fh)

     # Correct picture orientation based on EXIF metadata
     try:
         for orientation in ExifTags.TAGS.keys():
             if ExifTags.TAGS[orientation] == "Orientation":
                 break
         exif = img._getexif()
         if exif is not None:
             orientation_value = exif.get(orientation, None)
             if orientation_value == 3:
                 img = img.rotate(180, expand=True)
             elif orientation_value == 6:
                 img = img.rotate(270, expand=True)
             elif orientation_value == 8:
                 img = img.rotate(90, expand=True)
     except (AttributeError, KeyError, IndexError):
         pass

     img.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
     img_tk = ImageTk.PhotoImage(img)
     self.label.config(image=img_tk)
     self.label.image = img_tk
     self.root.after(DISPLAY_TIME, self.show_image)

if __name__ == "__main__":
    creds = authenticate_user()
    root = ui.Tk()
    root.title("Piktah")

    #root.iconphoto(False, ui.PhotoImage(file="C:/Users/The_User/Downloads/frikandel.png"))

    root.geometry(f"{MAX_IMAGE_SIZE[0]}x{MAX_IMAGE_SIZE[1]}")
    root.attributes("-topmost", True)
    root.attributes("-alpha", TRANSPARENCY)
    app = ImageShuffler(root, creds)
    root.mainloop()
