import nmap

def nmap_version_scan(target_ip):
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments='-sV')

    scan_results = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                service = nm[host][proto][port]
                scan_results.append({
                    'ip': host,
                    'port': port,
                    'protocol': proto,
                    'service_name': service['name'],
                    'service_product': service['product'],
                    'service_version': service['version'],
                    'service_extrainfo': service['extrainfo']
                })

    return scan_results

# Визначаємо IP-адресу для сканування
target_ip = "45.44.151.148"

# Викликаємо функцію сканування та виводимо результат
scan_results = nmap_version_scan(target_ip)
for result in scan_results:
    print(f"IP: {result['ip']}, Port: {result['port']}, Protocol: {result['protocol']}")
    print(f"Service: {result['service_name']}, Product: {result['service_product']}")
    print(f"Version: {result['service_version']}, Extra Info: {result['service_extrainfo']}")
    print("-" * 30)
