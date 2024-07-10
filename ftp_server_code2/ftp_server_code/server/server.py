import signal
import sys
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def load_users_from_file(filename):
    users = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                username, password, directory = parts
                users.append((username, password, directory))
    return users

def start_ftp_server():
    authorizer = DummyAuthorizer()

    users = load_users_from_file('users.txt')
    for username, password, directory in users:
        authorizer.add_user(username, password, directory, perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("192.168.1.102", 2121), handler)

    def signal_handler(sig, frame):
        print('Shutting down server...')
        server.close_all()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting FTP server on port 2121...")
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()
