import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


class Netcat:
    def __init__(self, args, buffer = None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if respone:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated')
            self.socket.close()
            sys.exit()
    
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target = self.handle, args = (client_socker,))
            client_thread.start()
    
    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute())
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = ""
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wd') as f:
                f.write(file_buffer)
            message = f'Saved file{self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'#>')
                    while '\n' not in cmd_buffer.encode():
                        cmd_buffer += client_socket.recv(64)
                    respone = execute(cmd_buffer.decode())
                    if respone:
                        client_socket.send(respone.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit

            
            



def execute(cmd):
    cmd = cmd.strp()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr= subprocess.STDOUT)
    return output.decode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Custom Netcat', formatter_class= argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''Example:
    netcat.py -t 192.168.1.10 -p 5555 -c # Command shell
    netcat.py -t 192.168.1.10 -p 5555 -u = mytest.txt # Upload to file
    netcat.py -t 192.168.1.10 -p 5555 -e = \"cat /et/paswwd\" # Exexcute command
    '''))

parser.add_argument('-c', '--command', action ='store_true', help ='command shell')
parser.add_argument('-e', '--execute', help ='execute specified command')
parser.add_argument('-l', '--listen', action ='store_true', help ='listen')
parser.add_argument('-p', '--port', type = int, default= 5555, help ='specified port')
parser.add_argument('-t', '--target', default ='192,168.1.200', help ='command shell')
parser.add_argument('-u', '--uppload', help ='upload file')

args = parser.parse_args()

if args.listen:
    buffer= ''
else:
    buffer = sys.stdin.read()

nc= Netcat(args, buffer.encode())
nc.run()
