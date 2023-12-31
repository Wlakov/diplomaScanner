import nmap


def scan_network(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range,
            arguments='-sV -p-')  # -sV для виведення інформації про версії, -p- для сканування всіх портів

    for host in nm.all_hosts():
        print(f"Host: {host}")
        print(f"  Name: {nm[host].hostname()}")

        if 'osclass' in nm[host]:
            for osclass in nm[host]['osclass']:
                print(f"  OS Class: {osclass['osclasstype']} - {osclass['osfamily']} {osclass['osgen']}")

        for proto in nm[host].all_protocols():
            print(f"  Protocol: {proto}")
            ports = nm[host][proto].keys()
            for port in ports:
                port_info = nm[host][proto][port]
                print(
                    f"    Port: {port} - State: {port_info['state']} - Service: {port_info['name']} - Version: {port_info['product']} {port_info['version']}")


ip_range = '192.168.1.1-255'  # Замініть на ваш діапазон IP

scan_network(ip_range)
