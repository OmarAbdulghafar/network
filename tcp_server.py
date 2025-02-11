import socket
import threading

IP = "0.0.0.0"
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(IP, PORT)
    sever.listen(5) # Maxmun num connection
    print(f"[*] Listening on {IP}:{PORT}")

    while True: # this loop for creating new thread for each connection
        client, address = server.accept() # client => OP (socket) , Address => (IP, PORT)
        print(f"[*] Accepted connection from {address[0]} : {address[1]}")
        client_handler = threading.Thread(target= handle_client, args= (client,)) # Create new thread
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode("utf-8")}")
        sock.send(b"ACK")


if __name__ == '__main__':
    main()

