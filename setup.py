#!/usr/bin/env python3
"""
Script de configuración e instalación del proyecto de análisis de ventas.

Este script configura el entorno y instala las dependencias necesarias
para ejecutar el proyecto completo.

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import subprocess
import sys
import os
from pathlib import Path
import platform


def print_banner():
    """
    Imprimir banner del proyecto.
    """
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           CONFIGURACIÓN DEL PROYECTO                        ║
    ║              ANÁLISIS DE VENTAS                             ║
    ║                                                              ║
    ║  SQL Avanzado • Python para Datos • Buenas Prácticas        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """
    Verificar versión de Python.
    
    Returns:
        bool: True si la versión es compatible
    """
    print("🐍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Error: Se requiere Python 3.8 o superior. Versión actual: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True


def create_virtual_environment():
    """
    Crear entorno virtual.
    
    Returns:
        bool: True si se creó exitosamente
    """
    print("\n🔧 Creando entorno virtual...")
    
    venv_name = "venv"
    venv_path = Path(venv_name)
    
    if venv_path.exists():
        print(f"⚠️  El entorno virtual '{venv_name}' ya existe")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"✅ Entorno virtual creado: {venv_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False


def install_dependencies():
    """
    Instalar dependencias del proyecto.
    
    Returns:
        bool: True si se instalaron exitosamente
    """
    print("\n📦 Instalando dependencias...")
    
    requirements_file = "requirements.txt"
    if not Path(requirements_file).exists():
        print(f"❌ Archivo {requirements_file} no encontrado")
        return False
    
    try:
        # Determinar el comando de pip según el sistema operativo
        if platform.system() == "Windows":
            pip_cmd = ["venv\\Scripts\\pip", "install", "-r", requirements_file]
        else:
            pip_cmd = ["venv/bin/pip", "install", "-r", requirements_file]
        
        subprocess.run(pip_cmd, check=True)
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False


def create_directories():
    """
    Crear directorios necesarios.
    
    Returns:
        bool: True si se crearon exitosamente
    """
    print("\n📁 Creando estructura de directorios...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/final",
        "logs",
        "cache",
        "backups",
        "docs",
        "notebooks"
    ]
    
    try:
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Directorio creado: {directory}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando directorios: {e}")
        return False


def setup_git():
    """
    Configurar Git para el proyecto.
    
    Returns:
        bool: True si se configuró exitosamente
    """
    print("\n🔧 Configurando Git...")
    
    try:
        # Verificar si Git está instalado
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        
        # Inicializar repositorio Git si no existe
        if not Path(".git").exists():
            subprocess.run(["git", "init"], check=True)
            print("✅ Repositorio Git inicializado")
        
        # Agregar archivos al staging
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Archivos agregados al staging")
        
        # Hacer commit inicial
        subprocess.run(["git", "commit", "-m", "Initial commit: Project setup"], check=True)
        print("✅ Commit inicial realizado")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git no está configurado o no está disponible: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  Git no está instalado en el sistema")
        return False


def run_tests():
    """
    Ejecutar tests del proyecto.
    
    Returns:
        bool: True si los tests pasaron
    """
    print("\n🧪 Ejecutando tests...")
    
    try:
        # Determinar el comando de pytest según el sistema operativo
        if platform.system() == "Windows":
            pytest_cmd = ["venv\\Scripts\\pytest", "tests/", "-v"]
        else:
            pytest_cmd = ["venv/bin/pytest", "tests/", "-v"]
        
        result = subprocess.run(pytest_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests ejecutados exitosamente")
            return True
        else:
            print("⚠️  Algunos tests fallaron")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando tests: {e}")
        return False


def create_activation_script():
    """
    Crear script de activación del entorno virtual.
    """
    print("\n📝 Creando script de activación...")
    
    if platform.system() == "Windows":
        script_content = """@echo off
echo Activando entorno virtual...
call venv\\Scripts\\activate
echo Entorno virtual activado!
echo Para ejecutar el proyecto: python main.py
cmd /k
"""
        script_file = "activate.bat"
    else:
        script_content = """#!/bin/bash
echo "Activando entorno virtual..."
source venv/bin/activate
echo "Entorno virtual activado!"
echo "Para ejecutar el proyecto: python main.py"
"""
        script_file = "activate.sh"
        # Hacer el script ejecutable en Unix
        os.chmod(script_file, 0o755)
    
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Script de activación creado: {script_file}")


def print_next_steps():
    """
    Imprimir próximos pasos para el usuario.
    """
    print("\n" + "=" * 60)
    print("🎯 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 Próximos pasos:")
    print("")
    
    if platform.system() == "Windows":
        print("1. Activar entorno virtual:")
        print("   activate.bat")
        print("")
        print("2. Ejecutar el proyecto:")
        print("   python main.py")
        print("")
        print("3. Ejecutar tests:")
        print("   venv\\Scripts\\pytest tests\\ -v")
    else:
        print("1. Activar entorno virtual:")
        print("   source activate.sh")
        print("")
        print("2. Ejecutar el proyecto:")
        print("   python main.py")
        print("")
        print("3. Ejecutar tests:")
        print("   venv/bin/pytest tests/ -v")
    
    print("\n📚 Recursos adicionales:")
    print("   • README.md - Documentación del proyecto")
    print("   • requirements.txt - Lista de dependencias")
    print("   • tests/ - Tests unitarios")
    print("   • src/ - Código fuente del proyecto")
    print("")
    print("🔗 Enlaces útiles:")
    print("   • SQLBolt: https://sqlbolt.com/")
    print("   • Mode Analytics SQL: https://mode.com/sql-tutorial/")
    print("   • Effective Pandas: https://github.com/mattharrison/effective-pandas")
    print("   • PEP 8: https://www.python.org/dev/peps/pep-0008/")
    print("")
    print("🚀 ¡Listo para comenzar el análisis de datos!")
    print("=" * 60)


def main():
    """
    Función principal de configuración.
    """
    print_banner()
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_virtual_environment():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Crear directorios
    if not create_directories():
        sys.exit(1)
    
    # Configurar Git
    setup_git()
    
    # Crear script de activación
    create_activation_script()
    
    # Ejecutar tests (opcional)
    print("\n¿Deseas ejecutar los tests ahora? (s/n): ", end="")
    response = input().lower().strip()
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        run_tests()
    
    # Mostrar próximos pasos
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico durante la configuración: {str(e)}")
        sys.exit(1)
