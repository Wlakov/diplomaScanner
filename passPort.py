import paramiko
import telnetlib


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


def check_telnet_default_password(hostname, username, password):
    try:
        tn = telnetlib.Telnet(hostname)
        tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        response = tn.read_some()
        if b"Login incorrect" not in response:
            print(f"Telnet login successful with default password: {password}")
            tn.close()
            return True
        else:
            print(f"Telnet login failed with default password: {password}")
            tn.close()
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    username = input("Enter the username: ")

    # Перевірка для SSH
    ssh_default_passwords = ["root", "admin", "toor", "password", "12345"]
    for password in ssh_default_passwords:
        check_ssh_default_password(target_host, username, password)

    # Перевірка для Telnet
    telnet_default_passwords = ["root", "admin", "toor", "password", "12345"]
    for password in telnet_default_passwords:
        check_telnet_default_password(target_host, username, password)
