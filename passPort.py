import paramiko


def check_ssh_default_password(hostname, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname, username=username, password=password)
        print(f"SSH login successful with default password: {password}")
        ssh_client.close()
        return True
    except paramiko.AuthenticationException:
        print(f"SSH login failed with default password: {password}")
        return False


if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    username = 'admin'

    # Перевірка для SSH
    ssh_default_passwords = ["root", "admin", "toor", "password", "12345"]
    for password in ssh_default_passwords:
        check_ssh_default_password(target_host, username, password)

