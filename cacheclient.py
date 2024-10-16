import socket

class CacheClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(command.encode())
            response = s.recv(1024)
            return response.decode()

if __name__ == '__main__':
    client = CacheClient()
    
    # Set a value
    print(client.send_command('SET key1 value1'))  # Output: SET OK
    
    # Get a value
    print(client.send_command('GET key1'))          # Output: value1
    
    # Get a non-existent value
    print(client.send_command('GET key2'))          # Output: NOT FOUND
    
    # Exit the client
    print(client.send_command('EXIT'))

