import paramiko
import socket
import time

def run_socket_communication(target_ip, port, polarization):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((target_ip, port))
            print(f"Connected to server at {target_ip}:{port}")

            # Send commands over the socket
            data = "V1,1000"
            client_socket.sendall(data.encode())

            data = "c"
            client_socket.sendall(data.encode())

            data = str(polarization)
            client_socket.sendall(data.encode())

            print("Socket communication completed.")

    except Exception as e:
        print("Error during socket communication:", e)

def ssh_command(hostname, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        # Execute the command and keep the channel open
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        # Read and print standard output
        for line in stdout:
            print("STDOUT:", line.strip())
        
        # Read and print standard error
        for line in stderr:
            print("STDERR:", line.strip())
        
        # Wait for a couple of seconds for rp_eth_com.py to execute
        time.sleep(10)

        # Perform socket communication
        run_socket_communication(target_ip, port, polarization)
        time.sleep(5)

        # Close the SSH session
        client.close()
        return True  # Command executed successfully
    except Exception as e:
        print("Error:", e)
        return False  # Command execution failed

if __name__ == "__main__":
    # SSH parameters
    hostname = '10.0.3.33'
    username = 'pi5'
    password = 'pi5'
    ssh_command_to_run = 'bash Documents/Python/bash_test.sh'

    # Socket parameters
    target_ip = '10.0.3.33'
    port = 1800
    polarization = 'V1,-3500'

    # Execute SSH command
    success = ssh_command(hostname, username, password, ssh_command_to_run)

    if success:
        print("SSH command executed successfully.")
    else:
        print("Failed to execute SSH command.")
