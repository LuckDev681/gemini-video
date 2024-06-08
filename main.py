import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import zipfile
import os
from moviepy.editor import VideoFileClip
from divide import divide_text
from merge import main
import srt
from srt import create_srt_file

directory_path = f"{os.path.dirname(__file__)}\\"
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": directory_path
  })
driver = webdriver.Chrome(options=options)
URL = 'https://drive.google.com/drive/folders/1sa9bNIfCuF-hIsEQJO_sp53Bjud2IkUl'
driver.get(URL)
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="drive_main_page"]/div/div[3]/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]').click()
time.sleep(70)
driver.quit()

# List all files in the directory
files = os.listdir(directory_path)

# Filter out only the zip file names
zip_files = [file for file in files if file.endswith('.zip')]

# Print the names of the zip files
for zip_file in zip_files:
    with zipfile.ZipFile(zip_file,"r") as zip_ref:
       zip_ref.extractall(directory_path)
    break

main()

genai.configure(api_key="AIzaSyBk_uJ8-8AXexsuaa7ZEyjvMlCUGV21CYE")

text='''
Stay fr.configuresh and hydrated with our
Portable Water Dispenser        
 Your ultimate solution for 
staying hydrated wherever you go
With its innovative design and 
convenience you have access to pure
refreshing water at your fingertips
Eliminating the need for unscrewing caps
or struggling with water bottles     
Don't wait to hydrate         
 Grab your HydroPure dispenser
today! 
'''

result_folder= os.path.join(directory_path, "Result")
os.makedirs(result_folder)
text_file = os.path.join(result_folder,  "text.txt")
with open(text_file, "w") as file:
    file.write(text)

parts = divide_text(text, 6)
data=[]

video_file_name="merged_output.mp4"
print(f"Uploading file...")
video_file=genai.upload_file(path=video_file_name)
print(f"Completed upload:{video_file.uri}")
time.sleep(20)
for i, part in enumerate(parts):
    print(part)
    prompt = "Please only output start time-end time: Which 5-second section section of the attached video best fits given script:" + part
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content([video_file, prompt])
    print(response.text)
    clip = VideoFileClip(video_file_name)
    start_time, end_time=response.text.split("-")
    start_minutes, start_seconds = start_time.split(":")
    start_seconds = int(start_minutes) * 60 + int(start_seconds)
    ## Split the end time into minutes and seconds
    end_minutes, end_seconds = end_time.split(":")
    end_seconds = int(end_minutes) * 60 + int(end_seconds)
    cut_clip = clip.subclip(start_seconds, end_seconds)
    cut_clip.write_videofile(f"{result_folder}/{i+1}.mp4")
    data.append({
        "start_time": start_time,
        "end_time":end_time,
        "text": part
    })
    time.sleep(1)
output_file=os.path.join(result_folder,"output.srt")
create_srt_file(data, output_file)