
import pyttsx3
import speech_recognition as sr
import datetime
import pyjokes
import pywhatkit as kit
import webbrowser
import pyautogui
import wikipedia
import os
from ultralytics import YOLO
import cv2
import cvzone
import math
import calendar
import cv2
import subprocess
import requests
import google.generativeai as genai
cm=open("name.txt","r")
listener=sr.Recognizer()
engie=pyttsx3.init()
voices=engie.getProperty("voices")
engie.setProperty("voice",voices[1].id)
engie.setProperty("rate",170)
name=cm.read()
def chandramuki(): 
 cap = cv2.VideoCapture(0)  # For WebCam
# cap = cv2.VideoCapture("../Videos/cars.mp4")  # For Video
 cap.set(3, 1280)  # For Webcam
 cap.set(4, 720)  # For WebCam
 model = YOLO("../Yolo-Weights/yolov8x.pt")

 classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

 success, img = cap.read()
 results = model(img, stream=True)
 talk(results)
 for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2,  y2 = box.xyxy[0]
            # x1, y1, w, h = box.xywh[0]
            # x1, y1, w, h = int(x1), int(y1), int(w), int(h)
            # cv2.rectangle(img,(x1, y1), (x2, y2), (255,0,255),3)
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = (x2-x1), (y2-y1)
            print(x1, y1, x2, y2)
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0]*100))
            print(conf)
            # Class Names
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{classNames[cls]} ', (max(0, x1), max(0, y1 + 35)), scale=1, thickness=1)
            talk(classNames[cls])




 cv2.imshow("Image", img)
 cv2.waitKey(1)
 
def ai(prompt):
    try:
        # Your Gemini AI API key
        api= "# Your Gemini AI API key"



        genai.configure(api_key=api)

# Set up the model
        generation_config = {
           "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
                       }



        
        safety_settings = [
       {
       "category": "HARM_CATEGORY_HARASSMENT",
       "threshold": "BLOCK_MEDIUM_AND_ABOVE"
       },
       {
       "category": "HARM_CATEGORY_HATE_SPEECH",
       "threshold": "BLOCK_MEDIUM_AND_ABOVE"
       },
       {
       "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
       "threshold": "BLOCK_MEDIUM_AND_ABOVE"
       },
       {
       "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
       "threshold": "BLOCK_MEDIUM_AND_ABOVE"
       },
      ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
        convo = model.start_chat(history=[
])

        convo.send_message(prompt)
        print(convo.last.text)
        talk(convo.last.text)
        
    except Exception as e:
        print("An error occurred:", e)
        return None


def talk(text):
    engie.say(text)
    engie.runAndWait()
def take_command():
    try:
        with sr.Microphone() as source:
         print("Listening.....")
         voice=listener.listen(source,phrase_time_limit=3)
         command=listener.recognize_google(voice)
         command=command.lower()
         print(command)
         return command
    except:
        return""

def greetings():
   current_time=datetime.datetime.now()
   hour=current_time.hour
   if 1<=hour< 12:
      talk("good morning sandeep I am "+name+"your personal assistant")
   elif 12<=hour<16:
      talk("good afternoon sandeep I am "+name+"your personal assistant")
   elif 16<=hour<7:
      talk("good evening sandeep I am "+name+"your personal assistant")
   else:
      talk("hello sandeep I am "+name+"your personal assistant")





def run_assis():
   command=take_command()
   if "hello" in command or "hi" in command:
      talk("hello sandeep how may i help you today")  
   elif "goodbye" in command:
      talk("good bye!")
      exit()
   elif "joke" in command:
      talk(pyjokes.get_joke())
   elif "song" in command or "video" in command:
      talk("playing.."+command)
      kit.playonyt(command)
   elif "time" in command:
      time=datetime.datetime.now().strftime("%I:%M %p")
      print(time)
      talk(time)
   elif "open" in command:
      command=command.replace("open","")
      pyautogui.press("super")
      
      pyautogui.typewrite(command)
      pyautogui.sleep(1)
      pyautogui.press("enter")
      talk("opening"+command)
   elif "close" in command:
      pyautogui.hotkey("alt","f4")
      talk("closing sir")
   elif "camera" in command or "take a photo" in command:
      camera_port=0
      camera=cv2.VideoCapture(camera_port)
      return_value, image=camera.read()
      cv2.imwrite("auth.jpg",image)
      del(camera)

   elif "who is" in command or "what is" in command or "why" in command :
     try:
      person=command.replace("who is","")
      info=wikipedia.summary(person,3)
      print(info)
      talk(info)
     except:
        talk("sorry i am unable to peocess your command!")
   elif "remember that" in command:
      remembermessage=command.replace("remember that","")
      talk("you told me to remember that"+remembermessage)
      remember=open("remember.txt","w")
      remember.write(remembermessage)
      remember.close()
   elif "what do you remember" in command:
      remember=open("remember.txt","r")
      talk("you told me to remember that "+remember.read())
   elif "weather" in command or "whether" in command:
            api_key = "ee6b438edb3cb44ce721340ed29abfe7"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            talk("what is the city name")
            city_name = take_command()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if "cod" in x and x["cod"] != "404":
              main_data = x.get("main", {})
              if "temp" in main_data and "humidity" in main_data:
                   current_temperature = main_data["temp"]
                   current_humidity = main_data["humidity"]
                   weather = x.get("weather", [])
                   if weather:
                      weather_description = weather[0].get("description", "Unknown")
                   else:
                      weather_description = "Unknown"

                   talk("Temperature in kelvin unit:"+str( current_temperature))
                   talk("Humidity in percentage:"+str(current_humidity))
                   talk("Description:" +weather_description)
              else:
                talk("Temperature or humidity information not available.")
            else:
              talk("City not found or weather data not available.")

   elif "clear file" in command:
      file=open("remember.txt","w")
      file.write(f"")
      talk("completed your command sir!")
   elif "shutdown" in command:
      talk("closing the system sir")
      talk("3......2....... 1")
      subprocess.call(['shutdown','/l'])
   elif "restart" in command:
      talk("restarting the system sir")
      talk("3. 2. 1")
      os.system("shutdown /r /t 1")  
   elif "news" in command:
      webbrowser.open_new_tab("https://timesofindia.indiatimes.com/india")
      talk("here are some latest news!")
   elif "change your name" in command:
      namec=command.replace("change your name to","")
      talk("you told me to change mys name as "+namec)
      name=open("name.txt","w")
      name.write(namec)
      name.close()
   elif "can i know your name" in command:
      namec=open("name.txt","r")
      talk("my name is :" +namec.read())
   elif ('how are you' in command or 'how r u' in command):
            talk( " I am fine?")
   elif ('search' in command):
      textWords = command.split()  # Split the command into words
      if 'search' in textWords:  # Check if 'search' is in the command
        index = textWords.index('search')  # Get the index of 'search'
        query_index = index + 1  # The index of the search query
        if query_index < len(textWords):  # Ensure there is a query after 'search'
            if textWords[query_index].lower() in ['for', 'about']:
                query_index += 1  # Move to the next word if 'for' or 'about' is found
            search_query = ' '.join(textWords[query_index:])  # Join the query words into a single string
            website = 'https://www.google.com/search?client=firefox-b-d&q=' + search_query.lower()
            talk(command + " " + "These are the search results.")
            webbrowser.open_new(website)
   elif "Using artificial intelligence".lower() in command:
            command=command.replace("using artificial intelligence"," ")
            ai(prompt=command)
   elif "detect the object" in command:
      chandramuki() 
      
           
   elif "stuck" in command or "play" in command:
      pyautogui.press("k")
      talk("done sir!")
   elif "date" in command or "day" in command:
    now = datetime.datetime.now()
    date = datetime.datetime.today()
    weekday = calendar.day_name[date.weekday()]  # E.g : Friday
    monthNum = now.month
    dayNum = now.day

    # A list of months
    month_names = ['January', 'Febraury', 'March', 'April', 'May', 'April', 'June', 'July', 'August', 'September',
                   'October', 'November', 'December']

    # A list of ordinal numbers
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
                      '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th',
                      '26th', '27th', '28th', '30th', '31st']

    talk('Today is ' + weekday + ' ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + ' . ')


   elif "full screen" in command:
      pyautogui.press("f")
      talk("done sir!")
   elif "message" in command:
      
        talk("Please provide the phone number.")
        number = take_command()  # Get phone number via voice
        talk("Please say the message.")
        message = take_command()  # Get message via voice
        kit.sendwhatmsg_instantly(f'+91{number}', message)
        pyautogui.sleep(10)
   
      

   elif command:
    website = 'https://www.google.com/search?client=firefox-b-d&q=' + command.lower()
    talk("Browsing " + command)
    webbrowser.open_new(website)
   
   
   else:
      talk("sorry i cant hear you")

greetings()
def authenticate_user(known_voiceprint):
    microphone = sr.Microphone()

    with microphone as source:
        print("Please say the passphrase for authentication:")
        talk("Please say the passphrase for authentication:")
        listener.adjust_for_ambient_noise(source)
        audio_data = listener.listen(source,phrase_time_limit=3)

    try:
        # Convert speech to text
        spoken_text = listener.recognize_google(audio_data)
        print("You said:", spoken_text)
        
        # Compare spoken text to known voiceprint
        if spoken_text.lower() == known_voiceprint.lower():
            talk("Authentication successful!")
            talk("now i am ready for you commands sandeep")
            
            while True:
             run_assis()
        else:
            talk("Authentication failed. Voice not recognized.")
    except sr.UnknownValueError:
        talk("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        talk("Error fetching results from Google Speech Recognition service:", e)

# Example usage
known_voiceprint = "sandeep"

# Authenticate user

authenticate_user("sandeep")
