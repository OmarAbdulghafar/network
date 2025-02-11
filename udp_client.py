import socket

target_host = "127.0.0.1"
target_port = 9998

# Creat socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
client = sendto(b"Hello,its me",(target_host,target_port))

# receive data
data, addr = client.recvfrom(4096) #maximum num of bytes

print(data.decode())
client.close
