import requests
import socket
import os
import time
import datetime

def print_green(message):
    """Prints the message in green color."""
    print(f"\033[92m{message}\033[0m")  

def log_results(filename, header, results):
    """Log found results to a file."""
    if results:  
        with open(filename, 'a') as f:
            f.write(f"\n{header}:\n")
            for result in results:
                f.write(f"{result}\n")
                print_green(f"{header}: {result}")

def loading_animation():
    """Display a loading animation."""
    print("Loading", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(" Done!")

def brute_force_subdomains(base_url, wordlist_path, output_file):
    """Brute force subdomains based on the provided wordlist."""
    found_domains = [] 
    try:
        with open(wordlist_path, "r") as file:
            subdomain_wordlist = file.read().splitlines()
    except FileNotFoundError:
        print("Wordlist file not found!")
        return found_domains

    for word in subdomain_wordlist:
        subdomain_url = f"http://{word}.{base_url}"  
        print(f"Checking: {subdomain_url}")  
        try:
            response = requests.get(subdomain_url, timeout=5)  
            if response.status_code == 200:
                found_domains.append(subdomain_url)  
                print_green(f"Found: {subdomain_url}")  
        except requests.exceptions.RequestException:
            print(f"Failed to connect: {subdomain_url}")  

    log_results(output_file, "Found Domains", found_domains)
    return found_domains

def brute_force_directories(base_url, wordlist_path, output_file):
    """Brute force directories based on the provided wordlist."""
    found_directories = []  
    try:
        with open(wordlist_path, "r") as file:
            directory_wordlist = file.read().splitlines()
    except FileNotFoundError:
        print("Wordlist file not found!")
        return found_directories

    for word in directory_wordlist:
        dir_url = f"http://{base_url}/{word}"  
        print(f"Checking: {dir_url}")  
        try:
            response = requests.get(dir_url, timeout=5)  
            if response.status_code == 200:
                found_directories.append(dir_url)  
                print_green(f"Found directory: {dir_url}")  
        except requests.exceptions.RequestException:
            print(f"Failed to connect: {dir_url}")  

    log_results(output_file, "Found Directories", found_directories)
    return found_directories

def brute_force_files(base_url, wordlist_path, extensions, output_file):
    """Brute force files based on the provided wordlist and extensions."""
    found_files = []  
    try:
        with open(wordlist_path, "r") as file:
            file_wordlist = file.read().splitlines()
    except FileNotFoundError:
        print("Wordlist file not found!")
        return found_files

    for word in file_wordlist:
        for ext in extensions:
            file_url = f"http://{base_url}/{word}{ext}"  
            print(f"Checking: {file_url}")  
            try:
                response = requests.get(file_url, timeout=5)  
                if response.status_code == 200:
                    found_files.append(file_url)  
                    print_green(f"Found file: {file_url}")  
            except requests.exceptions.RequestException:
                print(f"Failed to connect: {file_url}") 

    log_results(output_file, "Found Files", found_files)
    return found_files

def port_scanner(ip, port_range, output_file):
    """Scan specified ports for the given IP address."""
    print(f"\nStarting port scan on {ip}...")
    open_ports = []
    found_ports = []  

    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  
            result = sock.connect_ex((ip, port))
            if result == 0:  
                open_ports.append(port)
                found_ports.append(port)  
                print_green(f"Port {port} is open on {ip}")

    log_results(output_file, "Open Ports", found_ports)
    return open_ports

def run_subdomain_bruteforce(base_url, output_file):
    """Run subdomain brute-forcing."""
    wordlist_path = input("Enter the path to the subdomain wordlist file: ").strip()
    brute_force_subdomains(base_url, wordlist_path, output_file)

def run_directory_bruteforce(base_url, output_file):
    """Run directory brute-forcing."""
    wordlist_path = input("Enter the path to the directory wordlist file: ").strip()
    brute_force_directories(base_url, wordlist_path, output_file)

def run_file_bruteforce(base_url, output_file):
    """Run file brute-forcing."""
    wordlist_path = input("Enter the path to the file wordlist file: ").strip()
    print("Don't Miss (.), e.g.: .php, .json")
    extensions = input("Enter extensions to try (comma-separated, e.g., 'php,html'): ").strip().split(',')
    brute_force_files(base_url, wordlist_path, extensions, output_file)

def main():
    print("""                       █████                                                                       
                      ░░███                                                                        
  ██████   █████ ████ ███████    ██████             ████████   ██████   ██████   ██████  ████████  
 ░░░░░███ ░░███ ░███ ░░░███░    ███░░███ ██████████░░███░░███ ███░░███ ███░░███ ███░░███░░███░░███ 
  ███████  ░███ ░███   ░███    ░███ ░███░░░░░░░░░░  ░███ ░░░ ░███████ ░███ ░░░ ░███ ░███ ░███ ░███ 
 ███░░███  ░███ ░███   ░███ ███░███ ░███            ░███     ░███░░░  ░███  ███░███ ░███ ░███ ░███ 
░░████████ ░░████████  ░░█████ ░░██████             █████    ░░██████ ░░██████ ░░██████  ████ █████
 ░░░░░░░░   ░░░░░░░░    ░░░░░   ░░░░░░             ░░░░░      ░░░░░░   ░░░░░░   ░░░░░░  ░░░░ ░░░░░ 
                                                                                                   
                                                                                                   
                                                                                       Powred By Bo7           """)
    
    
    base_ip = input("Enter the target IP address (e.g., 192.168.1.1): ").strip()
    port_range_choice = input("Do you want to scan ports 1-1024 (type '1') or all ports (type 'all')? ").strip().lower()
    
    if port_range_choice == '1':
        port_range = (1, 1024)
    elif port_range_choice == 'all':
        port_range = (1, 65535)
    else:
        print("Invalid choice for port range.")
        return

    output_file = "enumeration_results.txt"  
    print(f"Target Address: {base_ip}")
    print(f"Start Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output File: {output_file}")
    print(f"Working Directory: {os.getcwd()}")
    
    loading_animation()  
    open_ports = port_scanner(base_ip, port_range, output_file)

    if 80 in open_ports:
        base_url = input("Enter the target domain (e.g., example.com): ").strip()
        loading_animation()  
        run_subdomain_bruteforce(base_url, output_file)

        while True:
            print("\nChoose an option:")
            print("1. Brute force directories")
            print("2. Brute force files")
            choice = input("Enter your choice (1 or 2, or 'q' to quit): ").strip()
            if choice == '1':
                loading_animation()
                run_directory_bruteforce(base_url, output_file)
            elif choice == '2':
                loading_animation()  
                run_file_bruteforce(base_url, output_file)
            elif choice.lower() == 'q':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
