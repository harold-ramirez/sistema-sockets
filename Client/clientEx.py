import socket
import psutil
import time
import json

# Ask user for a custom name to describe the device
device_name = input("Enter a name to describe the device: ")

def get_storage_info():
    """Retrieve storage information."""
    storage_info = []
    
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)

        # Convert bytes to human-readable GB
        to_gb = lambda bytes: round(bytes / (1024 ** 3), 2)

        storage_info.append({
            'device_name': device_name,
            'mountpoint': partition.mountpoint,
            'total': to_gb(usage.total),
            'used': to_gb(usage.used),
            'free': to_gb(usage.free),
            'percent': usage.percent
        })
    return storage_info

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Check for internet connectivity."""
    try:
        socket.create_connection((host, port), timeout)
        return True
    except OSError:
        return False

def send_data_to_server(server_ip, server_port, data):
    """Send data to the server via socket."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            # Serialize data to JSON
            serialized_data = json.dumps(data)
            print(serialized_data)
            # Send data length first (for chunk handling)
            #client_socket.sendall(f"{len(serialized_data):<10}".encode('utf-8'))
            # Send the actual data
            client_socket.sendall(serialized_data.encode('utf-8'))
            print("Data sent successfully.")
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    server_ip = '10.116.134.23'
    server_port = 12345

    while True:
        if check_internet():
            storage_info = get_storage_info()
            print("Internet connected. Data to be sent:")
            for info in storage_info:
                print(info)

            send_data_to_server(server_ip, server_port, str(storage_info))
        else:
            print("No internet connection. Retrying...")
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
