from gtts import gTTS
import os

def text_to_speech(text):
    try:
        tts = gTTS(text, lang='en') 
        tts.save("speech.mp3")  

        os.system("mpg321 speech.mp3") 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    text_to_speech("placeholder")
