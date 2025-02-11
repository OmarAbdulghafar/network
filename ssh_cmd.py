import paramiko


def ssh_command(ip, port, passwd, cdm):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port= port, username= user, password= passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:

        print("---Outout---")
        for line in output:
            print(line.strip())

if __name__ == "__main__":
    import getpass
    user = print("Username: ")
    password = getpass.getpass()

    ip = input("Enter server IP: ")
    port = input("Enter port or <CR>: ")
    cmd = input("Enter command or <CR>")
    ssh_command(ip, port, user, password, cmd)