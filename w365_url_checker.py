import socket
import urllib.request
import csv

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
timeout_seconds=1
pass_counter = 0
fail_counter = 0

with open("hosts.csv","r") as hostlist:
    csvreader = csv.reader(hostlist)
    for row in csvreader:
        host = row[0]
        ports = [int(item) for item in row[1:] if item != ""]
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout_seconds)
                result = sock.connect_ex((host,port))
                if result == 0:
                    output = f"Host: {host}, Port: {port}, Status: Passed"
                    pass_counter += 1
                else:
                    output = f"Host: {host}, Port: {port}, Status: Failed"
                    fail_counter += 1
                sock.close()
                print(output)
            except socket.gaierror:
                print(f"{host} FAILED DNS LOOKUP")
                fail_counter += 1

print(f"Your public IP is {external_ip}")
print(f"{pass_counter} Tests Passed")
print(f"{fail_counter} Tests Failed")