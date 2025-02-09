import cv2
from pyzbar.pyzbar import decode

def BarcodeReader(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image {image_path}")
        return

    # Resize the image to make the barcode larger
    scale_percent = 150  # Resize by 150%
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Enhance contrast
    enhanced_img = cv2.convertScaleAbs(gray_img, alpha=2.0, beta=50)

    # Try decoding the barcode
    bd = cv2.barcode.BarcodeDetector()
    decoded_info, points, retval = bd.detectAndDecode(img)
    #print(decoded_info)
    #print(retval)
    if not decoded_info:
    #detected_barcodes = decode(enhanced_img)

    #if not detected_barcodes:
        print("Barcode Not Detected!")
        return

    # Process and return barcode data
    else:
        #(x, y, w, h) = barcode.rect
        #cv2.rectangle(img, (x-10, y-10), (x + w+10, y + h+10), (255, 0, 0), 2)
        #if barcode.data:
            #print(f"📦 Detected Barcode: {barcode.data.decode('utf-8')}")
                    #return barcode.data.decode("utf-8")
        return decoded_info

    # Display the processed image
    cv2.imshow("Processed Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test with the uploaded image
    image_path = "./IMG_3294.jpeg"  # Replace with the correct path
    barcode = BarcodeReader(image_path)
    if barcode:
        print(f"Detected Barcode: {barcode}")
    else:
        print("No barcode detected.")
