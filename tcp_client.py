import socket

target_host = "www.google.com"
target_port = 80

# Creat socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4 , TCP)

client.connect((target_host, target_port))

client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

respone = client.recv(4096) #maximum num of bytes

print(respone.decode())
client.close()
