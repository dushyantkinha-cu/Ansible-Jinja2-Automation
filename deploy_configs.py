from sshInfo import load_devices
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

def push_config(task):
    device_info = task['device']
    config_file = task['file']
    host_ip = device_info['host']
    
    print(f"[{host_ip}] Initiating connection")
    try:
        net_connect = ConnectHandler(**device_info)
        net_connect.enable() 
        
        print(f"[{host_ip}] Connected! Pushing {config_file}")
        output = net_connect.send_config_from_file(config_file)
        net_connect.disconnect()
        print(f"[{host_ip}] Configuration successfully deployed and saved.")
        
    except Exception as e:
        print(f"[{host_ip}] ERROR: Failed to configure device. {e}")

def main():
    devices = load_devices("sshInfo.json")
    
    # This maps the devices using the keys from the JSON file
    deployments = [
        {'device': devices['R1'], 'file': 'R1_config.cfg'},
        {'device': devices['R2'], 'file': 'R2_config.cfg'},
        {'device': devices['R3'], 'file': 'R3_config.cfg'}
    ]
    
    print("Starting concurrent configuration deployment\n" + "-"*40)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(push_config, deployments)
        
    print("-" * 40 + "\nAll deployments finished!")

if __name__ == "__main__":
    main()