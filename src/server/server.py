import socket
import threading
import mimetypes
from datetime import datetime
from os import path

HOST = "127.0.0.1"
PORT = 8080
WWW_ROOT = "src/www"
BUFFER_SIZE = 1024

'''
    Simple HTTP Server
    This is a simple HTTP server that serves static files from a specified directory.
    It handles GET requests.
    Returns the requested file or a 404 error if the file is not found.
'''
class HTTPServer:
    
    host = None
    port = None
    root = None
    logger = None 
    server_socket = None
    
    '''
        Initialize the server with the specified host, port, and root directory.
        The server socket is created and bound to the specified host and port.
    '''
    def __init__(self, host, port, root):
        
        self.host = host
        self.port = port
        self.root = root
        self.logger = Logger()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# AF_INET = IPv4, SOCK_STREAM = TCP
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set the socket to be reusable
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
    '''
        Start the server and listen for incoming connections.
        When a connection is accepted, a new thread start to handle the request.
        The server will run indefinitely until interrupted by the user.
    '''
    def start(self):
        self.logger.log("green", f"Server started on {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            
            # Log the connection
            self.logger.log("blue", f"Connection from {addr}") 
            
            # Spawn a new thread to handle the request
            threading.Thread(target=self.handle_request, args=(client_socket,)).start()
    
    '''
        Handle incoming requests from clients.
        This method reads the request, parses the headers, and serves the requested file.
        If the file is not found, a 404 error is returned.
    '''
    def handle_request(self, client_socket):
        request = client_socket.recv(BUFFER_SIZE).decode()
        
        if not request:
            self.logger.log("red", "No request received.")
            client_socket.close()
            return
        
        headers = request.split("\r\n")
        
        try:
            method, url_path, _ = headers[0].split()
        except ValueError:
            self.logger.log("red", "Malformed request.")
            client_socket.close()
            return

        if method == "GET":
            self.logger.log("green", f"GET request for {url_path}")
    
            # Normalize the URL path        
            if url_path == "/":
                url_path = "/index.html"
            
            
            file_path = path.join(self.root, url_path.lstrip("/"))
            
            # Check if the file exists and is a file
            if path.exists(file_path) and path.isfile(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                
                content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                
                # Log the file being served
                self.logger.log("green", f"Serving file: {file_path}")
                
                # Send the response OK!
                self.send_response(client_socket, "200 OK", content_type, content)
            else:
                self.logger.log("red", f"File not found: {file_path}")
                body = b"<h1>404 Not Found</h1>"
                
                #Send the response 404
                self.send_response(client_socket, "404 Not Found", "text/html", body)
        else:
            self.logger.log("red", f"Unsupported method: {method}")
            body = b"<h1>405 Method Not Allowed</h1>"
            self.send_response(client_socket, "405 Method Not Allowed", "text/html", body)
    
    '''
        Send an HTTP response to the client.
        The response includes: 
            - status code;
            - content type;
            - body.
        The connection is closed after sending the response.
    '''
    
    def send_response(self, client_socket, status_code, content_type, body):
        
        if isinstance(body, str):
            body = body.encode()
            

        header = f"HTTP/1.1 {status_code}\r\n" 
        header += f"Content-Type: {content_type}\r\n"
        header += f"Content-Length: {len(body)}\r\n"
        header += f"Connection: close\r\n\r\n"
        

        client_socket.sendall(header.encode() + body)
        client_socket.close()
            
'''
    Logger class
    This class is responsible for logging messages to the console.
    It uses ANSI escape codes to color the output.
    The log method takes a color and a message as arguments and prints the message in the specified color.
    COLORS:
        - reset (White): Default Color 
        - red: Error!
        - green: OK!
        - blue: Info!
'''
class Logger:
    colors = {
            "reset": "\033[0m", # White
            "red": "\033[31m", # Error
            "green": "\033[32m", # OK
            "blue": "\033[34m", # Info
        }

    def __init__(self):
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"{self.colors.get('blue', '')}Logger start on {date}{self.colors['reset']}"
        
        print(message)

    def log(self, color, message):
    
        log_entry = f"[{datetime.now()}] {message}\n"
        colored = f"{self.colors.get(color, '')}{log_entry}{self.colors['reset']}"
        
        print(colored)
        
if __name__ == "__main__":
    server = HTTPServer(HOST, PORT, WWW_ROOT)
    try:
        server.start()
    except KeyboardInterrupt:
        server.server_socket.close()
        server.logger.log("blue", "Server stopped by user.")