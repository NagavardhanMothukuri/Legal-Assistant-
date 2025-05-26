import os
import zipfile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def zip_folder(folder_path, zip_name):
    zip_path = os.path.join(os.path.expanduser("~"), "Desktop", zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"✅ Folder zipped at: {zip_path}")
    return zip_path

def upload_to_drive(zip_file_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens a browser for Google login
    drive = GoogleDrive(gauth)

    file_name = os.path.basename(zip_file_path)
    gfile = drive.CreateFile({'title': file_name})
    gfile.SetContentFile(zip_file_path)
    gfile.Upload()

    print(f"✅ Uploaded to Google Drive as: {file_name}")

# 🧠 Local folder to zip (your 'img' folder path)
folder_to_zip = r"C:\Users\NAGAVARDHAN\Downloads\DeepFashion-20250407T144630Z-009\DeepFashion\In-shop Clothes Retrieval Benchmark\Anno\densepose\img_iuv\img"
zip_file_name = "DeepFashionImages.zip"

# 🔁 Step 1: Compress
zip_file_path = zip_folder(folder_to_zip, zip_file_name)

# ☁️ Step 2: Upload to Google Drive
upload_to_drive(zip_file_path)
