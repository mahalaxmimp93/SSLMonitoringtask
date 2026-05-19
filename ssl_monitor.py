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
