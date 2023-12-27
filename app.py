import os
from flask import Flask
import pickle
import threading
import time

app = Flask(__name__)

# Define the Product class
class Product:
    def __init__(self, barcode, name, shelf_num, notes, physical_media):
        self.barcode = barcode
        self.name = name
        self.shelf_num = shelf_num
        self.notes = notes
        self.physical_media = physical_media
        self.is_taken_out = False
        self.last_watched = "N/A"

# Function to load products from the default directory
def load_products_from_default_directory():
    # Construct the file path
    file_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'MovieDB', 'products.pkl')

    # Check if the file exists before loading it
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            products = pickle.load(file)
        return products
    else:
        print("The file does not exist in the default directory.")
        return []

# Function to update products every 5 minutes
def update_products():
    while True:
        # Load data from the .pkl file (replace 'products.pkl' with your file name)
        products = load_products_from_default_directory()

        # Sort products by shelf number
        products_sorted = sorted(products, key=lambda x: x.shelf_num)

        # Update the global variable holding the sorted products
        global sorted_products
        sorted_products = products_sorted

        print("Checked for updates!")
        # Wait for 5 minutes before the next update
        time.sleep(60)

# Start a thread to update products periodically
update_thread = threading.Thread(target=update_products)
update_thread.daemon = True
update_thread.start()

# Global variable to store sorted products
sorted_products = []

@app.route('/')
def display_products():
    global sorted_products
    
    # Generate HTML content dynamically
    html_content = "<h1>Product Information</h1>"
    html_content += "<table border='1'>"
    html_content += "<tr><th>Barcode</th><th>Name</th><th>Shelf Number</th><th>Notes</th><th>Physical Media</th><th>Is Taken Out</th><th>Last Watched</th></tr>"

    for product in sorted_products:
        html_content += f"<tr><td>{product.barcode}</td><td>{product.name}</td><td>{product.shelf_num}</td><td>{product.notes}</td><td>{product.physical_media}</td><td>{product.is_taken_out}</td><td>{product.last_watched}</td></tr>"

    html_content += "</table>"
    
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
