import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time
from barcodescanner import BarcodeReader
from apirequest import get_product_ecoscore
from tts import text_to_speech
from llm import GPTModel

class Camera:
    def __init__(self, button_pin=17, save_path=""):
        """Initialize the button and camera module."""
        self.button_pin = button_pin
        self.save_path = save_path

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Camera setup
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())  # Set still mode
        self.picam2.start()

        # Set up event detection
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.capture_photo, bouncetime=300)

        print(f"ButtonCamera initialized. Waiting for button press... (GPIO {self.button_pin})")

    def capture_photo(self):
        """Capture a photo and save it with a timestamp."""
        filename = f"photo.jpg"
        self.picam2.capture_file(filename)
        print(f"Photo saved: {filename}")

    def run(self):
        """Keep the script running and handle cleanup on exit."""
        # try:
        #     while True:
        #         time.sleep(0.1)  # Keep the script running
        # except KeyboardInterrupt:
        #     print("\nExiting...")
        #     self.cleanup()
        self.capture_photo()
        barcode = BarcodeReader("photo.jpg")
        if not barcode or barcode == "":
            text_to_speech("Please try again, scan a valid barcode")
            self.cleanup()

        product_name, ecoscore = get_product_ecoscore(barcode)
        model = GPTModel()
        eco_message = model.generate_output(product_name, ecoscore)
        text_to_speech(eco_message)
        self.cleanup()

    def cleanup(self):
        """Cleanup GPIO settings on exit."""
        GPIO.cleanup()
        print("GPIO cleaned up.")

    
# Run the program
if __name__ == "__main__":
    camera = Camera(button_pin=17)  # Change the GPIO pin if needed
    camera.run()
