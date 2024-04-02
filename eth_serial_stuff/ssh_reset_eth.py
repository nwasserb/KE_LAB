import paramiko

def ssh_command(hostname, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        client.close()
        return True  # Command executed successfully
    except Exception as e:
        print("Error:", e)
        return False  # Command execution failed

if __name__ == "__main__":
    hostname = '10.0.3.33'
    username = 'pi5'
    password = 'pi5'  
    command = 'python3 /Documents/Python/reset_eth.py'
    #command = 'ping 10.0.3.33'

    success = ssh_command(hostname, username, password, command)

    if success:
        print("Command executed successfully.")
    else:
        print("Failed to execute command.")
