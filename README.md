# Hybrid Network Automation: Python & Ansible for Cisco IOS

This repository contains a hybrid network automation workflow that combines the data manipulation strengths of Python with the template-rendering capabilities of Ansible. By translating a simple CSV requirement file into fully deployed Cisco IOS configurations, this project demonstrates practical Infrastructure as Code (IaC) principles for scalable network provisioning.

## Features

* **Data-Driven Variable Generation:** Uses a Python script to parse a CSV file (`config_reqs.csv`), automatically calculating subnet masks and OSPF wildcard bits using the `ipaddress` module, and formatting them into Ansible-ready YAML variables.
* **Template-Based Configuration:** Leverages Ansible and Jinja2 (`lab7.j2`) to render device-specific configurations, including Interface IP addressing, GigabitEthernet duplex/speed settings, and OSPF routing processes.
* **Concurrent Deployment:** Utilizes Python's `ThreadPoolExecutor` alongside `netmiko` to push the generated configuration files to multiple routers simultaneously, drastically reducing deployment time.
* **Modular Architecture:** Separates device inventory (`sshInfo.json`), configuration logic (Ansible roles), and deployment execution into distinct, maintainable components.

## File Structure

* **`generate_vars.py`**: Reads `config_reqs.csv` and generates the structured YAML variable file (`roles/router/vars/main.yml`) required by Ansible.
* **`site.yml` & `roles/router/tasks/main.yml`**: The Ansible playbook and role tasks that process the variables through the Jinja2 template to generate local `.cfg` files.
* **`roles/router/templates/lab7.j2`**: The Jinja2 template defining the Cisco IOS CLI syntax for interfaces and OSPF networks.
* **`deploy_configs.py`**: A multi-threaded Python script that connects to the routers via SSH (using `netmiko`) and applies the generated `.cfg` files.
* **`sshInfo.py` & `sshInfo.json`**: Manages the device inventory, IP addresses, and SSH authentication credentials.

## Prerequisites

* Python 3.x
* Ansible
* Python Packages: `netmiko`, `pyyaml`
* Network reachability to the target Cisco IOS devices.

## Usage Workflow

**Step 1: Define Network Requirements**
Populate `config_reqs.csv` with your target hostnames, IPs, subnets, interface details, and OSPF areas.

**Step 2: Generate Ansible Variables**
Execute the Python script to translate the CSV data into YAML format:
```bash
python generate_vars.py
```

**Step 3: Render Configurations**
Run the Ansible playbook to generate the individual router configuration files (e.g., `R1_config.cfg`) via Jinja2:
```bash
ansible-playbook site.yml
```

**Step 4: Deploy Configurations**
Push the generated configurations to the target devices concurrently:
```bash
python deploy_configs.py
```
