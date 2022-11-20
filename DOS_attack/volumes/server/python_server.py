'''
    author: jinal (kapatelj@uwindsor.ca)
'''

# Python server code
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "10.9.0.5"
serverPort = 8000

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path) 
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Web Server Home Page</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Welcome to the home page !!</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), WebServer)
    print("Web server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")