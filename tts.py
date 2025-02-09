from gtts import gTTS
import os
import subprocess

def set_usb_speaker_as_output():
    try:
        print("Setting USB speaker as the default output device...")
        os.system("amixer cset numid=3 1") 
        print("USB speaker configured successfully!")
    except Exception as e:
        print(f"Error setting USB speaker: {e}")

def text_to_speech(text):
    
    try:
        tts = gTTS(text, lang='en') 
        tts.save("speech.mp3") 

        subprocess.run(["mpg321", "speech.mp3"], check=True)  
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    set_usb_speaker_as_output()

    text = "test"
    text_to_speech(text)
