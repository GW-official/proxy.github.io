# proxy_server.py

import http.server
import socketserver
import threading
import requests  # Import requests library for HTTP requests

# Global variables for installation details
PROXY_ADDRESS = "https://github.com/GW-official/proxy.github.io/proxy_server.py"  # Replace with your GitHub Pages URL
PORT = 1234
ERROR_OCCURRED = False
ERROR_MESSAGE = ""

# Function to send installation status to SheetDB
def send_installation_status():
    global PROXY_ADDRESS, PORT, ERROR_OCCURRED, ERROR_MESSAGE

    # SheetDB API endpoint URL (replace with your actual SheetDB endpoint)
    sheetdb_api_url = "https://sheetdb.io/api/v1/o3iz1tpzsl6yl"

    # Data to be sent in the POST request
    data = {
        "installed": "yes",
        "proxy_address": PROXY_ADDRESS,
        "port": PORT,
        "error": "yes" if ERROR_OCCURRED else "no",
        "errors": ERROR_MESSAGE if ERROR_OCCURRED else ""
    }

    try:
        # Send POST request to SheetDB API
        response = requests.post(sheetdb_api_url, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        print("Installation status sent successfully to SheetDB.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send installation status to SheetDB: {e}")

# Proxy server handler
class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(self.rfile, self.wfile)

# Function to run the proxy server
def run_proxy_server():
    global ERROR_OCCURRED, ERROR_MESSAGE

    # Specify the port you want to run the proxy server on
    PORT = 8080

    # Set up the proxy server
    handler = ProxyHandler
    with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
        print("Proxy server running on port", PORT)

        try:
            # Attempt to send installation status to SheetDB upon successful start
            send_installation_status()
        except Exception as e:
            ERROR_OCCURRED = True
            ERROR_MESSAGE = str(e)
            print(f"Error sending installation status to SheetDB: {e}")

        httpd.serve_forever()

if __name__ == "__main__":
    run_proxy_server()

