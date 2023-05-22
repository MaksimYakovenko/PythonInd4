from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ""
PORT = 8001

if __name__ == '__main__':
    print(f'Локальний веб-сервер запущено на http://localhost:{PORT}')
    HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()