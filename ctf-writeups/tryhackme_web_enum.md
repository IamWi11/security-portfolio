# Target: Web Enumeration Lab (TryHackMe)

## Objective
Identify exposed services and sensitive information through web enumeration techniques.

## Scope
Single web application hosted in a controlled lab environment.

## Methodology
- Reconnaissance
- Web enumeration
- Vulnerability identification
- Reporting

## Tools Used
- Nmap
- Gobuster
- Nikto
- Burp Suite

## Reconnaissance
Performed port scan and identified an HTTP service running on port 80.

## Enumeration
Enumerated directories and discovered an unprotected administrative path.
Reviewed page source and identified hardcoded credentials.

## Exploitation
Used discovered credentials to access restricted functionality.

## Findings
- Exposed administrative interface
- Hardcoded credentials in client-side code
- Lack of authentication controls

## Remediation
- Remove credentials from source code
- Enforce authentication on administrative paths
- Apply least privilege to web services

## Lessons Learned
Demonstrated how improper web configuration and poor credential handling can expose sensitive system functionality.
