import nmap
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kali",
    database="Testip"
)

mycursor = mydb.cursor()


def nmap_version_scan(target_ip):
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments='-sV')

    scan_results = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                sql = "INSERT  INTO scan_results (ip, port, protocol, service, product, version) VALUES (%s,%s,%s,%s,%s,%s)"
                service = nm[host][proto][port]
                values = host, port, proto, service['name'], service['product'], service['version']



                







                mycursor.execute(sql, values)
                mydb.commit()

                scan_results.append({
                    'ip': host,
                    'port': port,
                    'protocol': proto,
                    'service_name': service['name'],
                    'service_product': service['product'],
                    'service_version': service['version']
                })

    return scan_results


if __name__ == '__main__':
    target_ip = "45.44.151.148"
    scan_results = nmap_version_scan(target_ip)
    for result in scan_results:
        print(f"IP: {result['ip']}, Port: {result['port']}, Protocol: {result['protocol']}")
        print(f"Service: {result['service_name']}, Product: {result['service_product']}")
        print(f"Version: {result['service_version']}")
        print("-" * 30)



# 45.44.151.148