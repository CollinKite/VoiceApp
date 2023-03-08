import requests
import os          
import tkinter as tk
import requests                                                                                                                                                                                                
from dotenv import load_dotenv
from pathlib import Path
from pygame import mixer
import io
load_dotenv(Path(".env"))
key = os.getenv("xi-api-key")

def GetVoiceOptions():
    #add api key to header
    headers = {
        'xi-api-key': key
    }
    response = requests.get('https://api.elevenlabs.io/v1/voices', headers=headers)
    
    data = response.json()
    voice_dict = {voice['voice_id']: voice['name'] for voice in data['voices']}
    return voice_dict


# Define the dictionary of id: name pairs
name_dict = GetVoiceOptions()
# Define the function that will be called when the submit button is pressed
def submit():
    # Get find the id of the selected name
    selected_name = id_dropdown.get()
    selected_id = [id for id, name in name_dict.items() if name == selected_name][0]
    text_input = text_box.get("1.0", "end").strip()

    # Make the POST request with the id and text in the headers
    headers = {
        'xi-api-key': key
    }
    json = {"text": text_input}
    response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/" +selected_id, headers=headers , json=json)

    #get the audio file from the response content as a
    #content type of audio/mpeg
    audio_file = io.BytesIO(response.content)
    #play the audio file
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.play()
    

# Create the GUI window
window = tk.Tk()
window.title("Text to Speech")

# Create the ID dropdown menu
id_dropdown = tk.StringVar(window)
id_dropdown.set("Select an Person") # default value
id_menu = tk.OptionMenu(window, id_dropdown, *name_dict.values())
id_menu.pack()

# Create the text box
text_box = tk.Text(window, height=5, width=50, wrap=tk.WORD)
text_box.pack()

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.pack()

# Start the main loop of the GUI
window.mainloop()
