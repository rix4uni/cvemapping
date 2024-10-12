# Use almalinux:8-minimal as the base image
FROM almalinux:8.8-minimal

# Modify /etc/nsswitch.conf to change the hosts line as specified
RUN sed -i 's/hosts:\s*files dns myhostname/hosts:      dns [SUCCESS=continue] files/' /etc/nsswitch.conf

# Set the working directory (optional)
WORKDIR /app

# Add the script that will be executed
COPY cve-2023-4813 /app/cve-2023-4813

# Make the script executable
RUN chmod +x /app/cve-2023-4813

# Command to run the script using bash
CMD bash -c "/app/cve-2023-4813 example.org 10 2>&1"

