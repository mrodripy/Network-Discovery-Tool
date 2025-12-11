# scanner.py - Ejemplo de módulo mejorado
import concurrent.futures
import socket
import subprocess
import platform
from ipaddress import IPv4Network
from typing import List, Dict

class NetworkScanner:
    def __init__(self, timeout: int = 2):
        self.timeout = timeout
        self.active_hosts = []

    def ping_host(self, ip: str) -> bool:
        """Realiza un ping a un host. Cross-platform y con manejo de errores."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-W', str(self.timeout), ip]
        try:
            output = subprocess.run(command, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, timeout=self.timeout + 1)
            return output.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False

    def resolve_hostname(self, ip: str) -> str:
        """Intenta resolver el nombre de host de una IP."""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except (socket.herror, socket.gaierror):
            return "N/A"

    def scan_network(self, network_cidr: str) -> List[Dict]:
        """Escanea un rango de red y retorna lista de hosts activos."""
        network = IPv4Network(network_cidr, strict=False)
        hosts_data = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {executor.submit(self.ping_host, str(ip)): ip for ip in network.hosts()}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                is_active = future.result()
                if is_active:
                    hostname = self.resolve_hostname(str(ip))
                    hosts_data.append({"ip": str(ip), "hostname": hostname, "status": "Active"})
        
        self.active_hosts = hosts_data
        return hosts_data
