import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time
from barcodescanner import BarcodeReader
from apirequest import get_product_ecoscore
from tts import text_to_speech
from llm import GPTModel
import os
from pynput import keyboard

class Camera:
    def __init__(self, save_path=""):
        """Initialize the button and camera module."""
        self.button_pin = 8
        self.save_path = save_path
        self.green_pin = 3
        self.yellow_pin = 5
        self.red_pin = 7

        # GPIO setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.setup(self.yellow_pin, GPIO.OUT)
        GPIO.output(self.yellow_pin, GPIO.LOW)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.output(self.red_pin, GPIO.LOW)

        # Camera setup
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())  # Set still mode
        self.picam2.start()

        print(f"Camera initialized. Waiting for button press or spacebar... (GPIO {self.button_pin})")

    def capture_photo(self):
        """Capture a photo and save it."""
        filename = "photo.jpg"
        self.picam2.capture_file(filename)
        print(f"Photo saved: {filename}")

    def text_out(self, string):
        text_to_speech(string)

    def handle_capture(self):
        print("Capture triggered!")
        self.capture_photo()
        barcode = BarcodeReader("photo.jpg")
        if not barcode or barcode == "":
            barcode = '3017620422003'

        product_name, ecoscore = get_product_ecoscore(barcode)
        if product_name == 'API request failed':
            self.text_out("Could not find item")
            return
        
        ecoscore = ecoscore.upper()
        print("Ecoscore:", ecoscore)
        if ecoscore not in ['A', 'B', 'C', 'D', 'E']:
            ecoscore = 'C'
        else:
            if ecoscore in ['A', 'B']:
                GPIO.output(self.green_pin, GPIO.HIGH)
            elif ecoscore in ['C', 'D']:
                GPIO.output(self.yellow_pin, GPIO.HIGH)
            elif ecoscore == 'E':
                GPIO.output(self.red_pin, GPIO.HIGH)
            
            model = GPTModel()
            eco_message = model.generate_output(product_name, ecoscore)
            self.text_out(eco_message)
            time.sleep(1)
        
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.yellow_pin, GPIO.LOW)
        GPIO.output(self.red_pin, GPIO.LOW)

    def run(self):
        """Keep the script running and handle cleanup on exit."""
        def on_press(key):
            if key == keyboard.Key.space:
                self.handle_capture()
        
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        try:
            while True:
                if GPIO.input(self.button_pin) == GPIO.HIGH:
                    print("Button pressed!")
                    self.handle_capture()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            self.cleanup()
        
        listener.stop()
        self.cleanup()

    def cleanup(self):
        """Cleanup GPIO settings on exit."""
        GPIO.cleanup()
        print("GPIO cleaned up.")

# Run the program
if __name__ == "__main__":
    camera = Camera()
    camera.run()
