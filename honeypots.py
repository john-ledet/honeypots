import socket
import threading
import logging

# Configure logging
logging.basicConfig(filename="attack_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# List of ports to monitor
PORTS = [22, 80, 443, 21, 3306, 3389]  # SSH, HTTP, HTTPS, FTP, MySQL, RDP

def handle_connection(port):
    """Function to listen on a port and log connection attempts."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(("0.0.0.0", port))
        sock.listen(5)
        logging.info(f"Listening on port {port}...")
        
        while True:
            conn, addr = sock.accept()
            logging.info(f"Connection attempt on port {port} from {addr[0]}:{addr[1]}")
            conn.close()
    
    except Exception as e:
        logging.error(f"Error on port {port}: {e}")
    finally:
        sock.close()

# Start listeners in threads
threads = []
for port in PORTS:
    thread = threading.Thread(target=handle_connection, args=(port,))
    thread.daemon = True
    threads.append(thread)
    thread.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    logging.info("Stopping the honeypot.")
