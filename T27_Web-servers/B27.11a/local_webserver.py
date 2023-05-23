from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ""
PORT = 8021

if __name__ == '__main__':
    print("=== Local CGI webserver ===")
    HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()