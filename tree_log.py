import os
import re
import argparse
import colorama
from colorama import Fore, Style

def read_and_copy_log(file_path, output_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    if not os.path.isfile(file_path):
        print(f"Error: The path '{file_path}' is not a file.")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(output_path, 'w') as file:
        file.writelines(lines)

    print_colored_lines(lines, output_path)

def print_colored_lines(lines, output_path):
    colorama.init(autoreset=True)
    
    
    colors = {
        'GET': Fore.GREEN,      
        'POST': Fore.RED,       
        'http': Fore.RED,       
        'https': Fore.RED,      
        'ip': Fore.BLUE,        
        'path': Fore.YELLOW      
    }
    
   
    ip_color_mapping = {}
    
   
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    domain_pattern = re.compile(r'\b([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b')

    
    with open(output_path, 'w') as output_file:
        for line in lines:
            line = line.strip()
            

            ips_found = ip_pattern.findall(line)
            domains_found = domain_pattern.findall(line)


            for ip in ips_found:
                if ip not in ip_color_mapping:
                    ip_color_mapping[ip] = colors['ip']


            colored_line = line
            
            
            if '/' in line:
                colored_line = colored_line.replace('/', colors['path'] + '/' + Style.RESET_ALL)


            for keyword, color in colors.items():
                if keyword in ['http', 'https', 'GET', 'POST']:
                    colored_line = colored_line.replace(keyword, color + keyword + Style.RESET_ALL)

            
            for ip in ip_color_mapping.keys():
                colored_line = colored_line.replace(ip, ip_color_mapping[ip] + ip + Style.RESET_ALL)

            
            for domain in domains_found:
                colored_line = colored_line.replace(domain, Fore.MAGENTA + domain + Style.RESET_ALL)

            
            print(colored_line)
            print()  

          
            output_file.write(colored_line + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read a tree log file, copy its contents to a new file, and print with colored lines.')
    parser.add_argument('file_path', type=str, help='The path to the log file.')
    parser.add_argument('output_path', type=str, help='The path to the output log file.')

    args = parser.parse_args()
    read_and_copy_log(args.file_path, args.output_path)
