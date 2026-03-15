import csv
import yaml
import ipaddress

def main():
    # This variable will hold the structured data before writing to the YAML file
    routers = {}

    # This reads the CSV file
    with open('config_reqs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hostname = row['Hostname']
            
            # If a dictionary for this router does not exist, initialize it
            if hostname not in routers:
                routers[hostname] = {
                    'hostname': hostname,
                    'ospf_process': row['OSPF Process ID'],
                    'interfaces': []
                }

            # This parses the IP address & subnet using the ipaddress module
            ip_interface = ipaddress.IPv4Interface(row['IP/Subnet'])
            
            # This builds the interface dictionary
            intf = {
                'type': row['Interface Type'],
                'name': row['Interface Name'],
                'ip': str(ip_interface.ip),
                'mask': str(ip_interface.netmask),
                'ospf_enabled': row['OSPF Enabled'].strip().lower() == 'yes',
                'ospf_network': str(ip_interface.network.network_address),
                'ospf_wildcard': str(ip_interface.network.hostmask),
                'ospf_area': row['OSPF Area']
            }
            
            # This adds the interfaces to the router's list
            routers[hostname]['interfaces'].append(intf)

    # This formats the data into a structure that Ansible expects
    yaml_data = {'lab7Config': list(routers.values())}

    # This writes the output directly into the Ansible /Roles/Router/Vars directory
    output_path = 'roles/router/vars/main.yml'
    with open(output_path, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=False)

    print(f"Success! Variables generated and saved to {output_path}")

if __name__ == "__main__":
    main()