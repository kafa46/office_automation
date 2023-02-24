'''
Socket Client
윈도우 서버에서 생성한 파일을 보내기 위한 소켓 서버
- Reference: 
    https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
'''

import socket
import os
import tqdm
from config import FILE_OUTPUT_DIR

class SocketClient():
    def __init__(
        self,
        host: str = '203.252.240.43',
        port: int = 9876,
    ) -> None:
        self.host = host
        self.port = port 
        self.buffer_size = 1024
        self.target_dir = FILE_OUTPUT_DIR
        self.seperator = "<SEPARATOR>"
    
    def send_file(self, filename: str = 'test\socket_test.txt') -> None:
        filesize = os.path.getsize(filename)
        print(f'File size: {filesize}')
        client = socket.socket()
        print(f"[+] Connecting to {self.host}:{self.port}")
        client.connect((self.host, self.port))
        print("[+] Connected.")
        client.send(f"{filename}{self.seperator}{filesize}".encode())
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(self.buffer_size)
                if not bytes_read:
                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))
        client.close()

def run(filename):
    socket = SocketClient()
    filename = os.path.join(socket.target_dir, filename)
    socket.send_file(filename)
    print(f'File transferred: {filename}')

if __name__=='__main__':
    f_name = '4aec67adf85ccc2c6c3abf528d4f343a54085ce11e18cf3e917b0a055f3546ac.pdf'
    # client = SocketClient()
    # client.send_file()
    run(f_name)