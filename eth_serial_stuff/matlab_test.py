
import socket
import sys

TARGET_IP = '10.0.3.33'
#PORT = int(sys.argv[2])
#polarization = sys.argv[1]
PORT = 1400
polarization = 'V1,3500'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((TARGET_IP, PORT))

    print(f"connected to server at {TARGET_IP}:{PORT}")


    data = "2"
    client_socket.sendall(data.encode())
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((TARGET_IP, PORT))

    print(f"connected to server at {TARGET_IP}:{PORT}")


    data = "c"
    client_socket.sendall(data.encode())
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((TARGET_IP, PORT))

    print(f"connected to server at {TARGET_IP}:{PORT}")


    data = "H"
    client_socket.sendall(data.encode())
    # data = "V1,100"
    # client_socket.sendall(data.encode())
    # data = 'V1,200'
    # client_socket.sendall(data.encode())

