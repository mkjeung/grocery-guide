import requests

def get_product_ecoscore(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json?fields=product_name,ecoscore_grade"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        product = data.get("product", {})
        product_name = product.get("product_name", "Unknown")
        ecoscore = product.get("ecoscore_grade", "N/A")
        return product_name, ecoscore.upper()
    else:
        return "API request failed", "N/A"
def main():
    example_barcode = "3017620422003"  
    product_name, ecoscore = get_product_ecoscore(example_barcode)
    with open("all_items.txt", "a") as file:
        file.write(f"{product_name},{ecoscore}\n")
    print(f"Product: {product_name}")
    print(f"Eco-Score: {ecoscore}")
if __name__ == "__main__":
    main()