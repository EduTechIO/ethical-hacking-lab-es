import os
import subprocess
import time
import secrets
import json
import string


partida = {"flags": []}

def limpiar():
    """ Limpia la pantalla de la terminal """
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_ip():
    """ Detecta la IP local para mostrarla en el menú """
    try:
        comando = "hostname -I | awk '{print $1}'"
        ip = subprocess.check_output(comando, shell=True).decode().strip()
        return ip if ip else "127.0.0.1"
    except Exception:
        return "No detectada"

def generar_flags(cantidad=3):
    """ Genera los tokens aleatorios (ej: aB123c456) """
    caracteres = string.ascii_letters + string.digits
    return [''.join(secrets.choice(caracteres) for _ in range(9)) for _ in range(cantidad)]

def mostrar_readme():
    """ Carga el README con less. Blindado contra cierres automáticos del sistema """
    limpiar()
    
    
    print("=================================================")
    print("              MANUAL DEL LABORATORIO             ")
    print("=================================================")
    print(" ► Usa las FLECHAS (Arriba/Abajo) para moverte.")
    print(" ► ATENCIÓN: Para salir, pulsa la letra 'Q'.")
    print("=================================================\n")
    input("Pulsa ENTER para abrir el documento...")
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_readme = os.path.join(directorio_actual, "README.md")
    
    if os.path.exists(ruta_readme):
        mensaje_pie = " [ ESTÁS EN EL MANUAL -> Usa las FLECHAS para leer | Pulsa 'Q' para SALIR ] "
        
        
        subprocess.run(["less", "-+e", "-+E", "-P", mensaje_pie, ruta_readme])
    else:
        limpiar()
        print("[!] Error: No se encuentra el archivo 'README.md'")
        input("Pulsa Enter para volver...")
        
def ejecutar_ansible(nivel, accion):
    global partida
    tag = f"nivel{nivel}_{accion}"
    num_flags = 4 if nivel == "3" else 3
    
    if accion == "deploy":
        partida["flags"] = generar_flags(num_flags)
        vars_dict = {f"flag{i+1}_val": f for i, f in enumerate(partida["flags"])}
        extra_vars = json.dumps(vars_dict)
        cmd = ["sudo", "ansible-playbook", "site.yml", "--tags", tag, "-e", extra_vars]
        print(f"\n[+] Preparando el escenario del Nivel {nivel}...")
    else:
        cmd = ["sudo", "ansible-playbook", "site.yml", "--tags", tag]
        print(f"\n[*] Limpiando el sistema... Por favor espera.")

    try:
       
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if accion == "deploy":
            print(f"[OK] Nivel {nivel} desplegado. ¡Buena suerte!")
    except subprocess.CalledProcessError:
        print(f"\n[!] Error crítico: No se pudo configurar el escenario.")
        input("Pulsa Enter para reintentar...")
    
    time.sleep(1.5)

def verificador_flags(nivel):
    limpiar()
    print("=== SISTEMA DE VALIDACIÓN ===\n")
    
    if not partida["flags"]:
        print("[!] No hay ningún nivel activo.")
        input("\nPulsa Enter...")
        return

    print("Introduce los códigos encontrados en el orden correcto.")
    print("Escribe 'exit' para cancelar.\n")

    for i, codigo_real in enumerate(partida["flags"], 1):
        while True:
            intento = input(f"Flag {i} >> ").strip()
            
            if intento.lower() == 'exit': return
            
            if intento == codigo_real:
                print("[+] ¡Correcto!\n")
                break
            else:
                print("[-] Código erróneo. Prueba de nuevo.")
    
    print(f"\n¡Nivel {nivel} superado con éxito!")
    input("\nPulsa Enter para volver al menú...")

def menu_principal():
    
    archivo_marcador = os.path.expanduser("~/.laboratorio_readme_visto")
    
    if not os.path.exists(archivo_marcador):
        mostrar_readme()
        try:
            with open(archivo_marcador, 'w') as f:
                f.write("visto")
        except Exception as e:
           
            print(f"\n[!] Aviso: No se pudo guardar el marcador en {archivo_marcador}")
            print(f"Error técnico: {e}")
            input("Pulsa Enter para continuar...")
    # ---------------------------------------------------------

    while True:
        limpiar()
        ip_actual = obtener_ip()
        print("=================================================")
        print("     ENTORNO CONFIGURABLE PARA HACKING ETICO     ")
        print(f"     IP DEL SERVIDOR: {ip_actual}")
        print("=================================================")
        print("1. Nivel Básico")
        print("2. Nivel Medio")
        print("3. Nivel Difícil")
        print("4. Ver README / Instrucciones")
        print("0. Salir")
        
        op = input("\nSelección >> ").strip()
        
        if op in ["1", "2", "3"]:
            ejecutar_ansible(op, "deploy")
            menu_gestion_nivel(op)
        elif op == "4":
            mostrar_readme()
        elif op == "0":
            print("Cerrando el laboratorio...")
            break
        else:
            print("Opción no reconocida.")
            time.sleep(1)

def menu_gestion_nivel(n):
    total = 4 if n == "3" else 3
    while True:
        limpiar()
        print(f"--- LABORATORIO: NIVEL {n} ---")
        print(f"IP OBJETIVO: {obtener_ip()} | FLAGS TOTALES: {total}")
        print("-------------------------------")
        print("1. Validar Flags encontradas")
        print("0. Terminar nivel y resetear")
        
        op = input("\nSelección >> ").strip()
        if op == "1":
            verificador_flags(n)
        elif op == "0":
            ejecutar_ansible(n, "reset")
            break

if __name__ == "__main__":
    menu_principal()