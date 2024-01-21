import socket


def get_internal_ip():
    # Create a UDP socket to an external server to determine the local IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Doesn't have to be reachable
            s.connect(('10.255.255.255', 1))
            internal_ip = s.getsockname()[0]
            return internal_ip
        except Exception as e:
            print(f"Error getting internal IP: {e}")
            return None
