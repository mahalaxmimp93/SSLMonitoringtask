Automated SSL Certificate Monitoring & Renewal Validation System
Overview:This project automatically monitors SSL/TLS certificates of websites, validates expiry dates, checks renewal status and sends alerts before expiration
What is SSL Certificate?
    An SSL (Secure Sockets Layer) certificate is a digital certificate that authenticates a website's identity and enables an encrypted       connection between a web server and a browser. It is required to secure sensitive data (like passwords or credit cards), build            customer trust with a padlock icon, and enable HTTPS, which is necessary for SEO and browser security compliance. 
Every HTTPS website has SSL certificate.
    Example:
    •	google.com 
    •	github.com 
    •	amazon.com 
   Certificates have:
    •	Start date 
    •	Expiry date 
This project checks expiry date automatically

1. Project Objective
The main goal is to:
    •	Checks SSL certificate expiry of websites 
    •	Calculates remaining days 
    •	Shows warning if expiry is near 
    •	Runs automatically every day 
    •	Sends alert if certificate is expiring

2. Real-Time Industry Problem
Many outages happen because:
    •	SSL certificates expire unexpectedly 
    •	Incorrect intermediate certificates are configured 
    •	Teams forget manual renewal dates 
Example:
    •	E-commerce websites become inaccessible 
    •	API integrations fail 
    •	Browsers show “Connection Not Secure” 
    •	Customers lose trust 
This automation solves that problem proactively.	

3.Project Architecture:
      Website
        ↓
   Python Script
        ↓
  Checks SSL Expiry
        ↓
    Prints Result
        ↓
  Cron Runs Daily
        ↓
Alert Sent if Expiring

4. Technology Used:
Tool	                  Why Needed
Linux	               Run automation
Python	          Write monitoring script
OpenSSL	           Read certificate
Cron	             Schedule automation
Git	                Store project
AWS EC2	            Host project

5. Steps involved in automation 
STEP 1 — Create Linux Server
Create Ubuntu server in Amazon Web Services.
Recommended:
•	Ubuntu 22.04 
•	t2.micro 
•	8 GB storage 
________________________________________
STEP 2 — Connect to Server
From terminal:
ssh -i mykey.pem ubuntu@public-ip
________________________________________
STEP 3 — Install Required Packages
Run:
sudo apt update

sudo apt install python3 -y
sudo apt install openssl -y

Verify:
python3 –version- Python 3.14.4
openssl version-OpenSSL 3.5.5 27 Jan 2026 (Library: OpenSSL 3.5.5 27 Jan 2026)

________________________________________
STEP 4 — Check SSL Manually
Run:
echo | openssl s_client -connect google.com:443 \
-servername google.com 2>/dev/null \
| openssl x509 -noout -dates
Output:
notBefore=Apr 20 08:35:05 2026 GMT
notAfter=Jul 13 08:35:04 2026 GMT
Important
notAfter = expiry date
________________________________________
STEP 5 — Create Project Folder
mkdir ssl-monitor-project
cd ssl-monitor-project
________________________________________
STEP 6 — Add Multiple Websites
Create:vi domains.txt
Add:
google.com
github.com
amazon.com
________________________________________
STEP 7 — Create Python Script to moniter SSL certificates and warning if expiry date is near
Create file:
vi ssl_monitor.py

write Python Script.
import ssl
import socket
from datetime import datetime
# Read domains from file
with open("domains.txt") as file:
    domains = file.readlines()
# Loop through each domain
for domain in domains:
    hostname = domain.strip()
    context = ssl.create_default_context()
    try:
        # Connect to website
        with socket.create_connection((hostname, 443)) as sock:
            # Wrap socket with SSL
            with context.wrap_socket(
                sock,
                server_hostname=hostname
            ) as ssock:

                # Get certificate
                cert = ssock.getpeercert()
        # Get expiry date
        expiry_date = cert['notAfter']
        # Convert string date to datetime
        expiry_datetime = datetime.strptime(
            expiry_date,
            '%b %d %H:%M:%S %Y %Z'
        )
        # Calculate remaining days
        remaining_days = (
            expiry_datetime - datetime.utcnow()
        ).days
        # Alert conditions
        if remaining_days < 15:
            print(
                f"CRITICAL ALERT: "
                f"{hostname} certificate expires "
                f"in {remaining_days} days"
            )
        elif remaining_days < 30:
            print(
                f"WARNING: "
                f"{hostname} certificate expires "
                f"in {remaining_days} days"
            )
        else:
            print(
                f"OK: "
                f"{hostname} certificate is healthy "
                f"({remaining_days} days left)"
            )
    except Exception as e:
        print(
            f"ERROR checking {hostname}: {e}"
        )
________________________________________
Run this script:
python3 ssl_monitor.py

Output: OK: google.com certificate is healthy (54 days left)
OK: github.com certificate is healthy (75 days left)
OK: amazon.com certificate is healthy (183 days left)
________________________________________
STEP 8 — Automate Using Cron
Open cron:
crontab -e
Select Nano option 

Add:
0 8 * * * /usr/bin/python3 /home/ubuntu/ssl-monitor-project/ssl_monitor.py
Meaning:
Every day at 8 AM
run SSL monitoring automatically
________________________________________
STEP 9 — Store Output in Log File
Update cron:
0 8 * * * /usr/bin/python3 /home/ubuntu/ssl-monitor-project/ssl_monitor.py >> /home/ubuntu/ssl.log

Check logs:
cat /home/ubuntu/ssl.log
________________________________________
STEP 10— Push Project to GitHub
Create repository in GitHub.
Initialize git:
git init

Add files:
git add .

Commit:
git commit -m "SSL monitoring project"

Push:
git remote add origin https://github.com/mahalaxmimp93/SSLMonitoringtask.git

git push -u origin main
