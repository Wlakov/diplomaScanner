import socket
import threading
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kali",
    database="Testip"
)


mycursor = mydb.cursor()


def is_port_open(host, port, result_lock, open_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((host, port))
        with result_lock:
            open_ports.append(port)
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        s.close()


def scan_ports(host, start_port, end_port, num_threads):
    open_ports = []
    result_lock = threading.Lock()
    threads = []

    print(f"Початок сканування {host} з порту {start_port} до порту {end_port}")

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=is_port_open, args=(host, port, result_lock, open_ports))
        threads.append(thread)
        thread.start()

        # Обмеження кількості одночасно працюючих потоків
        if len(threads) >= num_threads:
            for t in threads:
                t.join()
            threads = []

    # Завершення решти потоків
    for thread in threads:
        thread.join()

    return open_ports


if __name__ == "__main__":
    host = input("Введіть IP-адресу цільового сервера: ")
    start_port = 1
    end_port = 10000
    num_threads = 400

    open_ports = scan_ports(host, start_port, end_port, num_threads)

    if open_ports:
        print("Відкриті порти:")
        print(open_ports)
        sql = "INSERT  INTO scan_results (ip,o_ports,device)"
    else:
        print("На жаль, відкритих портів не знайдено.")
