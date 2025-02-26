import socket
import psutil
import time
import json

# Ask user for a custom name to describe the device
device_name = input("Enter a name to describe the device: ")

def get_storage_info():
    """Retrieve storage information, ignoring inaccessible drives."""
    storage_info = []
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)  # 🔹 Intentar obtener uso del disco
        except PermissionError:
            print(f"⚠️ No se pudo acceder a {partition.mountpoint}, ignorando...")
            continue  # 🔹 Saltar esta partición si no se puede acceder

        # Convertir bytes a GB
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
            print(data)
            # Send the actual data
            client_socket.sendall(data.encode('utf-8'))
            print("Data sent successfully.")
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    server_ip = '192.168.100.27' # CAMBIAR ESTA IP POR LA IP DE LA COMPU QUE ESTÁ EJECUTANDO EL SERVIDOR
    server_port = 12123

    while True:
        if check_internet():
            storage_info = get_storage_info()
            print("Internet connected. Data to be sent:")
            for info in storage_info:
                print(info)

            send_data_to_server(server_ip, server_port, json.dumps(storage_info))
        else:
            print("No internet connection. Retrying...")
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
