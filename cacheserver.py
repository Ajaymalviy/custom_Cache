import socket
import threading
import time

class CacheServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.cache = {}
        self.lock = threading.Lock()
        self.host = host
        self.port = port

    def handle_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode().strip().split(' ')
            if command[0] == 'GET':
                key = command[1]
                value = self.cache.get(key, 'NOT FOUND')
                conn.sendall(value.encode())
            elif command[0] == 'SET':
                key = command[1]
                value = command[2]
                with self.lock:
                    self.cache[key] = value
                conn.sendall(b'SET OK')
            elif command[0] == 'EXIT':
                break
        conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f'Server listening on {self.host}:{self.port}')
            while True:
                conn, addr = s.accept()
                print(f'Connected by {addr}')
                threading.Thread(target=self.handle_client, args=(conn,)).start()

if __name__ == '__main__':
    server = CacheServer()
    server.start()

