# Network Discovery Tool 🔍

Una herramienta rápida y eficiente para descubrir hosts activos en tu red local.

## Características

- ✅ Escaneo paralelo de múltiples hosts
- ✅ Detección de hosts activos mediante ping
- ✅ Resolución de hostnames
- ✅ Reporte detallado
- ✅ Cross-platform (Linux, macOS, Windows)
- 
## 📁 Project Structure
```
network_discovery_tool/
│
├── network_discovery_tool/   # Paquete principal (modular)
│   ├── __init__.py
│   ├── scanner.py           # Lógica principal de escaneo
│   ├── utils.py             # Funciones auxiliares (ej. cálculo de subred)
│   └── output.py            # Manejo de diferentes formatos de reporte
│
├── tests/                   # Pruebas automatizadas
│   └── test_scanner.py
│
├── docs/                    # Documentación
├── README.md                # Documento principal MEJORADO
├── requirements.txt
├── setup.py                 # Para instalación como paquete PyPI
└── main.py                  # Punto de entrada CLI (delgado)
```
## Instalación

```bash  
# Clonar repositorio  
git clone https://github.com/tu-usuario/network-discovery-tool.git  
cd network-discovery-tool  

# Crear entorno virtual  
python3 -m venv venv  
source venv/bin/activate  # En Windows: venv\Scripts\activate  

# Instalar dependencias  
pip install -r requirements.txt  
