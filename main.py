#!/usr/bin/env python3  
"""  
Network Discovery Tool v1.0  
Escanea tu red local y descubre hosts activos  
Autor: [Tu nombre]  
Fecha: 2025  
"""  

import subprocess  
import ipaddress  
import sys  
import time  
from concurrent.futures import ThreadPoolExecutor, as_completed  
from colorama import Fore, Style, init  

# Inicializar colorama para soporte de colores  
init(autoreset=True)  

class NetworkDiscovery:  
    """Clase para descubrir dispositivos en la red"""  
    
    def __init__(self, timeout=2):  
        """  
        Inicializar scanner  
        
        Args:  
            timeout (int): Tiempo máximo de espera por ping (segundos)  
        """  
        self.timeout = timeout  
        self.active_hosts = []  
        self.scanned_count = 0  
        self.start_time = None  
    
    def ping_host(self, host):  
        """  
        Verificar si un host está activo usando ping  
        
        Args:  
            host (str): Dirección IP a verificar  
            
        Returns:  
            bool: True si el host responde, False en caso contrario  
        """  
        try:  
            # Comando ping diferente según el SO  
            if sys.platform == "win32":  
                cmd = f"ping -n 1 -w {self.timeout * 1000} {host}"  
            else:  # Linux/Mac  
                cmd = f"ping -c 1 -W {self.timeout} {host}"  
            
            result = subprocess.run(  
                cmd,  
                shell=True,  
                capture_output=True,  
                timeout=self.timeout + 1  
            )  
            
            self.scanned_count += 1  
            return result.returncode == 0  
            
        except subprocess.TimeoutExpired:  
            self.scanned_count += 1  
            return False  
        except Exception as e:  
            print(f"{Fore.RED}[!] Error con {host}: {e}")  
            return False  
    
    def validate_network(self, network_str):  
        """  
        Validar que el formato de red sea correcto  
        
        Args:  
            network_str (str): Red en formato CIDR (ej: 192.168.1.0/24)  
            
        Returns:  
            ipaddress.IPv4Network o None  
        """  
        try:  
            network = ipaddress.ip_network(network_str, strict=False)  
            return network  
        except ValueError:  
            return None  
    
    def scan_network(self, network_str, max_workers=50):  
        """  
        Escanear toda una red y encontrar hosts activos  
        
        Args:  
            network_str (str): Red a escanear (ej: 192.168.1.0/24)  
            max_workers (int): Número de threads simultáneos  
            
        Returns:  
            list: Lista de IPs activas  
        """  
        # Validar red  
        network = self.validate_network(network_str)  
        if not network:  
            print(f"{Fore.RED}[!] Error: Formato de red inválido: {network_str}")  
            print(f"{Fore.YELLOW}    Usa formato CIDR: 192.168.1.0/24")  
            return []  
        
        print(f"\n{Fore.CYAN}[*] Iniciando escaneo de: {network}")  
        print(f"{Fore.CYAN}[*] Total de IPs a verificar: {network.num_addresses}")  
        print(f"{Fore.CYAN}[*] Workers (threads): {max_workers}\n")  
        
        self.start_time = time.time()  
        self.scanned_count = 0  
        
        # Obtener lista de hosts  
        hosts = list(network.hosts())  
        
        # Si la red es muy pequeña, incluir broadcast  
        if network.num_addresses <= 4:  
            hosts = list(network)  
        
        # Usar ThreadPoolExecutor para paralelizar  
        with ThreadPoolExecutor(max_workers=max_workers) as executor:  
            # Mapear cada host con su tarea  
            futures = {  
                executor.submit(self.ping_host, host): host   
                for host in hosts  
            }  
            
            # Procesar resultados conforme se completan para mostrar dos par
            for future in as_completed(futures):  
                host = futures[future]  
                try:  
                    is_active = future.result()  
                    if is_active:  
                        self.active_hosts.append(str(host))  
                        print(f"{Fore.GREEN}[+] ACTIVO: {host}")  
                except Exception as e:  
                    print(f"{Fore.RED}[!] Error procesando {host}: {e}")  
        
        return sorted(self.active_hosts)  
    
    def get_hostname(self, ip):  
        """  
        Intentar obtener hostname de una IP  
        
        Args:  
            ip (str): Dirección IP  
            
        Returns:  
            str: Hostname o "N/A"  
        """  
        try:  
            import socket  
            hostname = socket.gethostbyaddr(ip)[0]  
            return hostname  
        except:  
            return "N/A"  
    
    def generate_report(self):  
        """  
        Generar reporte final del escaneo  
        
        Returns:  
            str: Reporte formateado  
        """  
        elapsed_time = time.time() - self.start_time  
        
        report = f"""  
{Fore.CYAN}  
╔════════════════════════════════════════════════════════════╗  
║           NETWORK DISCOVERY REPORT                         ║  
╚════════════════════════════════════════════════════════════╝  

{Fore.WHITE}Hosts Activos: {Fore.GREEN}{len(self.active_hosts)}{Fore.WHITE}  
Hosts Escaneados: {Fore.YELLOW}{self.scanned_count}{Fore.WHITE}  
Tiempo Total: {Fore.YELLOW}{elapsed_time:.2f}s{Fore.WHITE}  
Velocidad: {Fore.YELLOW}{self.scanned_count/elapsed_time:.0f}
"""
        return report
# ==============================================================================
# BLOQUE DE EJECUCIÓN PRINCIPAL (AÑADIR ESTO AL FINAL DEL ARCHIVO)
# ==============================================================================
if __name__ == "__main__":
    
    # 1. Validar que se provea el argumento de red
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Uso: python3 {sys.argv[0]} <red_en_cidr>{Style.RESET_ALL}")
        print(f"Ejemplo: python3 {sys.argv[0]} 192.168.100.0/24")
        sys.exit(1)
        
    network_to_scan = sys.argv[1]
    
    # 2. Inicializar la clase
    scanner = NetworkDiscovery()
    
    # 3. Ejecutar el escaneo
    print(f"\n{Fore.CYAN}=====================================================")
    active_hosts = scanner.scan_network(network_to_scan)
    print(f"{Fore.CYAN}====================================================={Style.RESET_ALL}\n")
    
    # 4. Generar e IMPRIMIR el reporte (Las dos líneas que faltaban)
    final_report = scanner.generate_report()
    print(final_report) 

    # 5. Imprimir detalle de hosts activos con hostname
    if active_hosts:
        print(f"\n{Fore.CYAN}--- DETALLE DE HOSTS ACTIVOS ---{Style.RESET_ALL}")
        for host in active_hosts:
            # Obtiene el hostname
            hostname = scanner.get_hostname(host) 
            print(f"{Fore.GREEN}[+] {host} ({hostname}){Style.RESET_ALL}")
