import requests

barcode = "3017620422003"  

url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json?fields=product_name,ecoscore_grade"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    product = data.get("product", {})
    product_name = product.get("product_name", "Unknown")
    ecoscore = product.get("ecoscore_grade", "N/A")
    
    print(f"Product: {product_name}")
    print(f"Eco-Score: {ecoscore.upper()}") 
else:
    print("API request failed")
