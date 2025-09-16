#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Requests module not installed. Installing now...")
    os.system("pip install requests")
    import requests

try:
    from colorama import Fore, Style, init
except ImportError:
    print("Colorama module not installed. Installing now...")
    os.system("pip install colorama")
    from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Tool information
TOOL_NAME = "Fazo3xtrator"
VERSION = "1.0.0"
AUTHOR = "fazotz"
DESCRIPTION = "Advanced Bug Bounty Report Generator"

# Banner
def banner():
    print(f"""{Fore.CYAN}
    ████████╗ █████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗████████╗██████╗  █████╗ ████████╗
    ╚══██╔══╝██╔══██╗╚══███╔╝██╔═══██╗██╔══██╗╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
       ██║   ███████║  ███╔╝ ██║   ██║██████╔╝ ╚███╔╝    ██║   ██████╔╝███████║   ██║   
       ██║   ██╔══██║ ███╔╝  ██║   ██║██╔══██╗ ██╔██╗    ██║   ██╔══██╗██╔══██║   ██║   
       ██║   ██║  ██║███████╗╚██████╔╝██║  ██║██╔╝ ██╗   ██║   ██║  ██║██║  ██║   ██║   
       ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
    {Style.RESET_ALL}""")
    print(f"{Fore.YELLOW}{TOOL_NAME} v{VERSION} | {DESCRIPTION}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Created by {AUTHOR}{Style.RESET_ALL}\n")

# Check for updates
def check_update():
    print(f"{Fore.CYAN}[*] Checking for updates...{Style.RESET_ALL}")
    try:
        # In a real scenario, you would fetch this from a remote server
        latest_version = "1.0.0"
        
        if VERSION < latest_version:
            print(f"{Fore.YELLOW}[!] New version available: {latest_version}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Run 'git pull' or download the latest version{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[*] You are using the latest version{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to check for updates: {str(e)}{Style.RESET_ALL}")

# Main menu
def main_menu():
    print(f"\n{Fore.CYAN}Main Menu:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[1] Create New Report")
    print(f"[2] View Report Templates")
    print(f"[3] Update Tool")
    print(f"[4] Help")
    print(f"[5] Exit{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.YELLOW}[?] Select an option: {Style.RESET_ALL}")
    return choice

# Report templates
def view_templates():
    templates = {
        "1": "HackerOne Template",
        "2": "Bugcrowd Template", 
        "3": "HackenProof Template",
        "4": "Generic Template"
    }
    
    print(f"\n{Fore.CYAN}Available Templates:{Style.RESET_ALL}")
    for key, value in templates.items():
        print(f"{Fore.GREEN}[{key}] {value}{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.YELLOW}[?] Select template to view (or 'back' to return): {Style.RESET_ALL}")
    
    if choice.lower() == 'back':
        return
    
    if choice in templates:
        template_file = f"templates/{templates[choice].lower().replace(' ', '_')}.json"
        if os.path.exists(template_file):
            with open(template_file, 'r') as f:
                template_data = json.load(f)
                print(f"\n{Fore.CYAN}Template: {templates[choice]}{Style.RESET_ALL}")
                print(json.dumps(template_data, indent=2))
        else:
            print(f"{Fore.RED}[!] Template file not found{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] Invalid selection{Style.RESET_ALL}")

# Create report
def create_report():
    print(f"\n{Fore.CYAN}[*] Creating New Report{Style.RESET_ALL}")
    
    # Select template
    templates = {
        "1": "hackerone",
        "2": "bugcrowd",
        "3": "hackenproof", 
        "4": "generic"
    }
    
    print(f"\n{Fore.CYAN}Select Template:{Style.RESET_ALL}")
    for key, value in templates.items():
        print(f"{Fore.GREEN}[{key}] {value.capitalize()}{Style.RESET_ALL}")
    
    template_choice = input(f"\n{Fore.YELLOW}[?] Select template: {Style.RESET_ALL}")
    
    if template_choice not in templates:
        print(f"{Fore.RED}[!] Invalid selection{Style.RESET_ALL}")
        return
    
    template_name = templates[template_choice]
    template_file = f"templates/{template_name}.json"
    
    if not os.path.exists(template_file):
        print(f"{Fore.RED}[!] Template file not found{Style.RESET_ALL}")
        return
    
    # Load template
    with open(template_file, 'r') as f:
        template = json.load(f)
    
    # Collect information
    report_data = {}
    print(f"\n{Fore.CYAN}[*] Please provide the following information:{Style.RESET_ALL}")
    
    for field in template["fields"]:
        if field["type"] == "text":
            value = input(f"{Fore.YELLOW}[?] {field['prompt']}: {Style.RESET_ALL}")
            report_data[field["name"]] = value
        elif field["type"] == "multiline":
            print(f"{Fore.YELLOW}[?] {field['prompt']} (enter 'END' on a new line to finish):{Style.RESET_ALL}")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            report_data[field["name"]] = "\n".join(lines)
    
    # Generate report
    report_content = template["template"]
    for key, value in report_data.items():
        placeholder = "{" + key + "}"
        report_content = report_content.replace(placeholder, value)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_content = report_content.replace("{timestamp}", timestamp)
    
    # Save report
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    filename = f"{reports_dir}/{template_name}_report_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(report_content)
    
    print(f"\n{Fore.GREEN}[+] Report generated successfully: {filename}{Style.RESET_ALL}")
    
    # Preview report
    preview = input(f"\n{Fore.YELLOW}[?] Preview report? (y/n): {Style.RESET_ALL}")
    if preview.lower() == 'y':
        print(f"\n{Fore.CYAN}Report Preview:{Style.RESET_ALL}")
        print("-" * 50)
        print(report_content)
        print("-" * 50)

# Update tool
def update_tool():
    print(f"\n{Fore.CYAN}[*] Updating Fazo3xtrator{Style.RESET_ALL}")
    
    # Check if it's a git repository
    if os.path.exists(".git"):
        print(f"{Fore.GREEN}[*] Updating from git repository...{Style.RESET_ALL}")
        os.system("git pull")
        print(f"{Fore.GREEN}[+] Update completed{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] Not a git repository. Manual update required.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Please download the latest version from the official repository.{Style.RESET_ALL}")

# Help section
def show_help():
    print(f"\n{Fore.CYAN}Fazo3xtrator Help:{Style.RESET_ALL}")
    print(f"""
{Fore.GREEN}Usage:{Style.RESET_ALL}
  This tool helps bug bounty hunters generate professional reports for various platforms.

{Fore.GREEN}Features:{Style.RESET_ALL}
  - Generate reports for HackerOne, Bugcrowd, HackenProof, and other platforms
  - Customizable templates
  - Cross-platform (Windows, Kali Linux, Termux)
  - Colorized output for better readability

{Fore.GREEN}Commands:{Style.RESET_ALL}
  [1] Create New Report: Generate a new bug bounty report
  [2] View Report Templates: Preview available report templates
  [3] Update Tool: Check for and install updates
  [4] Help: Show this help message
  [5] Exit: Exit the tool

{Fore.GREEN}Installation:{Style.RESET_ALL}
  See README.md for detailed installation instructions

{Fore.GREEN}Support:{Style.RESET_ALL}
  For issues and feature requests, please check the official repository.
    """)

# Main function
def main():
    banner()
    check_update()
    
    while True:
        try:
            choice = main_menu()
            
            if choice == '1':
                create_report()
            elif choice == '2':
                view_templates()
            elif choice == '3':
                update_tool()
            elif choice == '4':
                show_help()
            elif choice == '5':
                print(f"\n{Fore.GREEN}[+] Thank you for using Fazo3xtrator!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Operation cancelled by user{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}[!] An error occurred: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Create default templates if they don't exist
    default_templates = {
        "hackerone.json": {
            "name": "HackerOne Report Template",
            "fields": [
                {
                    "name": "title",
                    "type": "text",
                    "prompt": "Vulnerability Title"
                },
                {
                    "name": "severity",
                    "type": "text", 
                    "prompt": "Severity Level (Critical/High/Medium/Low)"
                },
                {
                    "name": "url",
                    "type": "text",
                    "prompt": "Vulnerable URL"
                },
                {
                    "name": "description",
                    "type": "multiline",
                    "prompt": "Vulnerability Description"
                },
                {
                    "name": "steps",
                    "type": "multiline", 
                    "prompt": "Steps to Reproduce"
                },
                {
                    "name": "impact",
                    "type": "multiline",
                    "prompt": "Impact of the Vulnerability"
                },
                {
                    "name": "remediation",
                    "type": "multiline",
                    "prompt": "Suggested Remediation"
                }
            ],
            "template": """HackerOne Vulnerability Report

Title: {title}
Severity: {severity}
Date: {timestamp}
Reporter: [Your Name]

Vulnerable URL: {url}

## Description
{description}

## Steps to Reproduce
{steps}

## Impact
{impact}

## Suggested Remediation
{remediation}

## References
[Add any references here]"""
        },
        "hackenproof.json": {
            "name": "HackenProof Report Template",
            "fields": [
                {
                    "name": "title",
                    "type": "text",
                    "prompt": "Vulnerability Title"
                },
                {
                    "name": "severity", 
                    "type": "text",
                    "prompt": "Severity Level"
                },
                {
                    "name": "target",
                    "type": "text",
                    "prompt": "Target Name/URL"
                },
                {
                    "name": "description",
                    "type": "multiline",
                    "prompt": "Vulnerability Description"
                },
                {
                    "name": "proof",
                    "type": "multiline",
                    "prompt": "Proof of Concept"
                },
                {
                    "name": "impact",
                    "type": "multiline",
                    "prompt": "Impact Analysis"
                },
                {
                    "name": "fix",
                    "type": "multiline",
                    "prompt": "Suggested Fix"
                }
            ],
            "template": """HackenProof Bug Bounty Report

# {title}

**Severity:** {severity}
**Target:** {target}
**Date:** {timestamp}

## Description
{description}

## Proof of Concept
{proof}

## Impact
{impact}

## Suggested Fix
{fix}

## Additional Information
[Add any additional information here]"""
        },
        "generic.json": {
            "name": "Generic Report Template",
            "fields": [
                {
                    "name": "title",
                    "type": "text",
                    "prompt": "Vulnerability Title"
                },
                {
                    "name": "severity",
                    "type": "text",
                    "prompt": "Severity Level"
                },
                {
                    "name": "target",
                    "type": "text",
                    "prompt": "Target URL/Application"
                },
                {
                    "name": "description",
                    "type": "multiline",
                    "prompt": "Vulnerability Description"
                },
                {
                    "name": "steps",
                    "type": "multiline",
                    "prompt": "Steps to Reproduce"
                },
                {
                    "name": "evidence",
                    "type": "multiline",
                    "prompt": "Evidence/Screenshots"
                },
                {
                    "name": "impact",
                    "type": "multiline",
                    "prompt": "Impact Analysis"
                },
                {
                    "name": "remediation",
                    "type": "multiline",
                    "prompt": "Remediation Steps"
                }
            ],
            "template": """Bug Bounty Report

# {title}

**Report Date:** {timestamp}
**Severity:** {severity}
**Target:** {target}

## Vulnerability Description
{description}

## Steps to Reproduce
{steps}

## Evidence
{evidence}

## Impact
{impact}

## Remediation Steps
{remediation}

## Additional Notes
[Add any additional notes here]"""
        }
    }
    
    for filename, template in default_templates.items():
        template_path = os.path.join("templates", filename)
        if not os.path.exists(template_path):
            with open(template_path, 'w') as f:
                json.dump(template, f, indent=2)
    
    main()
