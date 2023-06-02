from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ""
PORT = 8080

if __name__ == '__main__':
    print("=== Local webserver ===")
    HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()