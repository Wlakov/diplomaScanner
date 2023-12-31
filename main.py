import requests


def check_weak_passwords(device_ip, password_list):
    for password in password_list:
        try_password(device_ip, password)


def try_password(device_ip, password):
    url = f"http://{device_ip}/signin"
    data = {"username": username, "password": password}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=data)

    if response.status_code == 200:
        print(f"Successful login with {password}")
    else:
        print(f"Login failed with {password}")


device_ip = "localhost:3000"
username = "admin"
password_list = ["password1", "123456", "admin123", "admin", "password"]

check_weak_passwords(device_ip, password_list)
