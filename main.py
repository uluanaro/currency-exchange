from http.server import HTTPServer, BaseHTTPRequestHandler
from database import init_db
from handler import Handler


if __name__ == '__main__':
    init_db()
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()