import os
import hashlib
import time

# List of configuration files to monitor
CONFIG_FILES = [
    # System configuration files
    "/etc/sysctl.conf",
    "/etc/security/limits.conf",
    "/etc/syslog.conf",
    "/etc/network/interfaces",
    "/etc/resolv.conf",
    "/etc/passwd",
    "/etc/group",
    "/etc/shadow",
    "/etc/fstab",
    "/etc/mtab",

    # Apache server configuration files
    "/etc/apache2/apache2.conf",
    "/etc/apache2/sites-available/000-default.conf",
    "/etc/httpd/conf/httpd.conf",

    # MySQL configuration files
    "/etc/mysql/my.cnf",
    "/etc/my.cnf",

    # Splunk configuration files
    "/opt/splunk/etc/system/local/server.conf",
    "/opt/splunk/etc/system/local/web.conf",

    # Additional application-specific files
    "/etc/docker/daemon.json",
    "/etc/paloalto/panorama.conf",
    "/etc/ntp.conf",
    "/etc/dhcp/dhcpd.conf",
]

# File to store hashes of monitored files
HASH_FILE = "config_file_hashes.txt"

# Function to calculate SHA256 hash of a file
def calculate_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            return hashlib.sha256(file_data).hexdigest()
    except FileNotFoundError:
        print(f"Warning: {file_path} does not exist.")
        return None
    except PermissionError:
        print(f"Error: Permission denied for {file_path}.")
        return None

# Load previously saved hashes
def load_previous_hashes():
    previous_hashes = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            for line in f:
                file_path, file_hash = line.strip().split(" ", 1)
                previous_hashes[file_path] = file_hash
    return previous_hashes

# Save current hashes to file
def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        for file_path, file_hash in hashes.items():
            f.write(f"{file_path} {file_hash}\n")

# Monitor files for changes
def monitor_files():
    previous_hashes = load_previous_hashes()
    current_hashes = {}

    for file_path in CONFIG_FILES:
        file_hash = calculate_file_hash(file_path)

        if file_hash:  # Proceed only if the file hash was successfully calculated
            current_hashes[file_path] = file_hash

            if file_path in previous_hashes:
                if previous_hashes[file_path] != file_hash:
                    print(f"Change detected in {file_path}")
            else:
                print(f"New file detected: {file_path}")

    save_hashes(current_hashes)

if __name__ == "__main__":
    while True:
        monitor_files()
        print("Monitoring complete. Waiting for the next check...")
        time.sleep(60)
