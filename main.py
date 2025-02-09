import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time
from barcodescanner import BarcodeReader
from apirequest import get_product_ecoscore
from tts import text_to_speech
from llm import GPTModel
import os

class Camera:
    def __init__(self, save_path=""):
        """Initialize the button and camera module."""
        self.button_pin = 11
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

        # Set up event detection
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.handle_button, bouncetime=300)

        print(f"ButtonCamera initialized. Waiting for button press... (GPIO {self.button_pin})")

    def capture_photo(self):
        """Capture a photo and save it with a timestamp."""
        filename = f"photo.jpg"
        self.picam2.capture_file(filename)
        print(f"Photo saved: {filename}")
    
    def text_out(self, string):
        text_to_speech(string)

    def handle_button(self):
        self.capture_photo()
        barcode = BarcodeReader("photo.jpg")
        if not barcode or barcode == "":
            self.text_out("Please try again, scan a valid barcode")
            #os.remove("photo.jpg")
            return

        product_name, ecoscore = get_product_ecoscore(barcode)
        if product_name == 'API request failed':
            self.text_out("Could not find item")
            #os.remove("photo.jpg")
            return
        ecoscore = ecoscore.upper()
        print("ecoscore:", ecoscore)
        if ecoscore not in ['A', 'B', 'C', 'D', 'E']:
            ecoscore = 'C'
        else:
            if ecoscore == 'A' or ecoscore == 'B':
                GPIO.output(self.green_pin, GPIO.HIGH)
            elif ecoscore == 'C' or ecoscore == 'D':
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
        #os.remove("photo.jpg")
    

    def test_lights(self):
        for i in range(3):
            GPIO.output(self.green_pin, GPIO.HIGH)
            GPIO.output(self.yellow_pin, GPIO.HIGH)
            GPIO.output(self.red_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.green_pin, GPIO.LOW)
            GPIO.output(self.yellow_pin, GPIO.LOW)
            GPIO.output(self.red_pin, GPIO.LOW)
            time.sleep(1)

    def run(self):
        """Keep the script running and handle cleanup on exit."""
        # try:
        #     while True:
        #         time.sleep(0.1)  # Keep the script running
        # except KeyboardInterrupt:
        #     print("\nExiting...")
        #     self.cleanup()
        #self.test_lights()


    def cleanup(self):
        """Cleanup GPIO settings on exit."""
        os.remove("photo.jpg")
        GPIO.cleanup()
        print("GPIO cleaned up.")

    
# Run the program
if __name__ == "__main__":
    camera = Camera()  # Change the GPIO pin if needed
    camera.run()