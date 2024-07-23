#!/usr/bin/env python3

import socket
import sys
import getopt
import random
from scapy.all import sr1, IP, TCP

def find_open_port(ip, ports, timeout, verbose, protocol, scan_type, ignore):
    open_ports = []
    log_messages = []

    for port in ports:
        if scan_type == "SYN":
            pkt = IP(dst=ip)/TCP(dport=port, flags="S")
            resp = sr1(pkt, timeout=timeout, verbose=0)
            if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:  # SYN-ACK
                log_message = f"\033[92mSuccessfully found open port {port}\033[0m"
                log_messages.append(log_message)
                open_ports.append(port)
                if verbose:
                    print(f"\033[92mPort {port} is open (stealth scan)\033[0m")
                sr1(IP(dst=ip)/TCP(dport=port, flags="R"), timeout=timeout, verbose=0)  # Send RST
                if not ignore:
                    break
            else:
                log_message = f"Port {port} is closed (stealth scan)"
                log_messages.append(log_message)
                if verbose:
                    print(log_message)
        else:  # Full connection scan
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    log_message = f"\033[92mSuccessfully found open port {port}\033[0m"
                    log_messages.append(log_message)
                    open_ports.append(port)
                    if verbose:
                        print(f"\033[92mPort {port} is open (full scan)\033[0m")
                    if not ignore:
                        break
                else:
                    log_message = f"Port {port} is closed (full scan)"
                    log_messages.append(log_message)
                    if verbose:
                        print(log_message)
            except socket.error as e:
                log_message = f"Socket error on port {port} (full scan): {e}"
                log_messages.append(log_message)
                if verbose:
                    print(log_message)
        if not ignore and open_ports:
            break

    return open_ports, log_messages

def print_help():
    GREEN = '\033[92m'
    RESET = '\033[0m'
    help_message = f"""
Usage: fop [OPTIONS] [custom_server_ip_address]:[port_ranges]

Options:
  {GREEN}-h{RESET}, {GREEN}--help{RESET}             Show this help message and exit.
  {GREEN}-t{RESET}, {GREEN}--timeout <secs>{RESET}   Set the timeout duration in seconds. Default is 1 second.
  {GREEN}-o{RESET}, {GREEN}--output <file>{RESET}    Save the open port results to a specified file.
  {GREEN}-v{RESET}, {GREEN}--verbose{RESET}          Provide detailed output for each step.
  {GREEN}-i{RESET}, {GREEN}--ignore{RESET}           Continue scanning all ports even if an open port is found.
  {GREEN}-e{RESET}, {GREEN}--exclude <ports>{RESET}  Specify ports to exclude from the scan, comma-separated.
  {GREEN}-s{RESET}, {GREEN}--scan-type-syn{RESET}    Use stealth (SYN) scan.
  {GREEN}-p{RESET}, {GREEN}--protocol <TCP/UDP>{RESET} Specify the protocol for the port scan. Default is TCP.
"""
    print(help_message)

def parse_port_ranges(port_ranges_str):
    ranges = port_ranges_str.split(',')
    ports = set()
    for range_str in ranges:
        if '-' in range_str:
            start, end = map(int, range_str.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(range_str))
    return list(ports)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:o:vpe:i", ["help", "timeout=", "output=", "verbose", "protocol=", "exclude=", "scan-type-syn", "ignore"])
        ip_address = None
        timeout = 1
        output_file = None
        verbose = False
        protocol = "TCP"  # Default protocol
        exclude_ports = set()
        ignore = False
        scan_type = "FULL"  # Default scan type
        ports = []

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print_help()
                sys.exit(0)
            elif opt in ("-t", "--timeout"):
                timeout = float(arg)
                if timeout <= 0:
                    raise ValueError("Timeout must be greater than 0.")
            elif opt in ("-o", "--output"):
                output_file = arg
            elif opt in ("-v", "--verbose"):
                verbose = True
            elif opt in ("-i", "--ignore"):
                ignore = True
            elif opt in ("-e", "--exclude"):
                exclude_ports.update(map(int, arg.split(',')))
            elif opt in ("-s", "--scan-type-syn"):
                scan_type = "SYN"
            elif opt in ("-p", "--protocol"):
                protocol = arg.upper()
                if protocol not in ["TCP", "UDP"]:
                    raise ValueError("Protocol must be either TCP or UDP.")

        if len(args) != 1:
            print("Error: Invalid arguments.")
            print_help()
            sys.exit(1)

        ip_port_ranges = args[0].split(':')
        if len(ip_port_ranges) != 2:
            print("Error: Invalid IP and port range format.")
            print_help()
            sys.exit(1)
        
        ip_address = ip_port_ranges[0]
        port_ranges_str = ip_port_ranges[1]
        ports = parse_port_ranges(port_ranges_str)
        ports = [port for port in ports if port not in exclude_ports]

        open_ports, log_messages = find_open_port(ip_address, ports, timeout, verbose, protocol, scan_type, ignore)

        if open_ports:
            message = f"Successfully found open ports: {', '.join(map(str, open_ports))}"
        else:
            message = "No open ports found."

        print(message)
        if output_file:
            with open(output_file, 'w') as file:
                for log_message in log_messages:
                    file.write(f"{log_message}\n")
                file.write(f"\n{message}\n")

    except ValueError as e:
        print(f"Error: {e}")
        print_help()
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
