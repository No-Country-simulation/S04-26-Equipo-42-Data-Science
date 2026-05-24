"""
ConversaAI Dashboard - Punto de entrada desde la raíz
Ejecutar con: python app.py
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Cambiar al directorio donde está el dashboard original
    dashboard_dir = Path(__file__).parent / "data_engineering" / "dashboard"
    dashboard_app = dashboard_dir / "app.py"
    
    if not dashboard_app.exists():
        print(f"❌ Error: No se encontró {dashboard_app}")
        print("Asegúrate de estar en la raíz del proyecto")
        return
    
    print("🚀 Iniciando ConversaAI Dashboard...")
    print(f"📁 Dashboard: {dashboard_app}")
    
    # Cambiar al directorio del dashboard para que las rutas relativas funcionen
    os.chdir(dashboard_dir)
    
    # Ejecutar streamlit con el mismo Python del entorno actual
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Dashboard detenido")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()