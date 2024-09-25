import re

# Regular expressions for IP addresses, common web crawlers, and advertisements
ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
crawler_pattern = re.compile(r'(googlebot|bingbot|slurp|duckduckbot|baiduspider|yandex|facebookexternalhit)', re.IGNORECASE)
ad_pattern = re.compile(r'(ads|doubleclick|adservice|adtech)', re.IGNORECASE)

def parse_log(file_path):
    filtered_logs = []
    unique_ips = set()

    with open(file_path, 'r') as log_file:
        for line in log_file:
            # Check for crawlers or ads
            if not crawler_pattern.search(line) and not ad_pattern.search(line):
                # Add the log line to the filtered logs
                filtered_logs.append(line)
                
                # Extract IP address from the log line
                match = ip_pattern.search(line)
                if match:
                    unique_ips.add(match.group())
    
    return filtered_logs, unique_ips

def write_filtered_log(filtered_logs, output_path):
    with open(output_path, 'w') as f:
        f.writelines(filtered_logs)

def write_unique_ips(unique_ips, output_path):
    with open(output_path, 'w') as f:
        for ip in unique_ips:
            f.write(f"{ip}\n")

if __name__ == "__main__":
    log_file_path = 'webserver.log'  # Input log file
    filtered_log_output = 'filtered_log.txt'  # Output filtered log file
    unique_ips_output = 'unique_ips.txt'  # Output unique IPs file

    # Parse the log file
    filtered_logs, unique_ips = parse_log(log_file_path)

    # Write the filtered logs to a file
    write_filtered_log(filtered_logs, filtered_log_output)

    # Write the unique IPs to a file
    write_unique_ips(unique_ips, unique_ips_output)

    print(f"Filtered log saved to: {filtered_log_output}")
    print(f"Unique IPs saved to: {unique_ips_output}")
