import schedule
import time
from pythonping import ping
import logging
import ipaddress

# List to store hosts to monitor
hosts_to_monitor = []

# Configure logging
logging.basicConfig(filename="network_monitor.log", level=logging.INFO, format="%(asctime)s - %(message)s")


# Function to check if an IP address is valid
def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


# Function to add a host to the monitoring list after validating the IP address
def add_host_to_monitor():
    while True:
        host = input("Enter the IP address to monitor (or 'done' to finish): ")

        if host.lower() == 'done':
            break

        if is_valid_ip(host):
            hosts_to_monitor.append(host)
            print(f"Added {host} to monitoring list.")
        else:
            print("Invalid IP address. Please enter a valid IPv4 address (e.g., 192.168.1.1).")


# Function to check host status
def check_host_status(host):
    try:
        response = ping(host, count=1)
        if response.rtt_avg_ms is not None:
            status = "Reachable"
            response_time = response.rtt_avg_ms
        else:
            status = "Unreachable"
            logging.warning(f"{host} is unreachable!")

        logging.info(f"{host} - Status: {status}, Response Time: {response_time} ms")
    except Exception as e:
        logging.error(f"Error while pinging {host}: {str(e)}")


# Main loop
if __name__ == "__main__":
    add_host_to_monitor()  # Collect IP addresses first
    for host in hosts_to_monitor:
        schedule.every(10).seconds.do(check_host_status, host)  # Schedule monitoring task

    while True:
        schedule.run_pending()
        time.sleep(1)
