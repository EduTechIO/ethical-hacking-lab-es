# 🛡️ Entorno Virtual de Hacking Ético Configurable

🇪🇸 Versión en español | [🇬🇧 English version](https://github.com/EduTechIO/ethical-hacking-lab-en)

---

# Guía del Entorno Configurable

Este entorno contiene tres escenarios de auditoría de seguridad configurados dinámicamente mediante Ansible. El objetivo es realizar el compromiso total de la máquina víctima desde un equipo externo (Kali Linux), simulando un entorno real de pentesting.

## 📥 Descarga

Debido a las limitaciones de tamaño de archivo de GitHub, la máquina virtual preconfigurada en formato OVA está alojada externamente:

**[⬇️ Descargar OVA (Google Drive)](https://drive.google.com/file/d/1PJM7DmvSJTQRu-ErZ3iab52o4sUHEXYm/view?usp=sharing)**

> Tamaño del archivo: ~3.3 GB | Formato: Open Virtualization Archive (.ova)

## Requisitos previos

- **Software de virtualización:** VirtualBox, VMware o cualquier hipervisor compatible.
- **Máquina víctima:** Ubuntu Server 24.04.4 LTS (mínimo 2 GB de RAM).
- **Máquina atacante:** Kali Linux o cualquier distribución de pentesting propia del usuario.
- **Red:** Ambas máquinas deben tener conectividad entre sí. Se necesita usar **adaptador puente (Bridge)**.
- **Ansible:** Está instalado localmente en la máquina víctima (Ubuntu Server), no se requiere instalación externa.


## Estructura del proyecto

```
Entorno_Configurable/
├── ansible.cfg                        # Configuración general de Ansible
├── inventory.ini                      # Inventario con la IP del servidor
├── site.yml                           # Playbook principal que orquesta los roles
├── gestor_entorno_configurable.py     # Script del menú de control de niveles
├── README.md                          # Este archivo
└── roles/
    ├── nivel_basico/tasks/
    │   └── main.yml                   # Tareas del Nivel 1 (Inicial)
    ├── nivel_medio/tasks/
    │   └── main.yml                   # Tareas del Nivel 2 (Media)
    └── nivel_dificil/tasks/
        └── main.yml                   # Tareas del Nivel 3 (Avanzada)
```


## Instalación y despliegue

1. Importar la máquina virtual del servidor (Ubuntu Server) en VirtualBox o VMware.
2. Configurar el adaptador de red en modo **puente (Bridge)** en ambas máquinas.
3. Iniciar la máquina víctima (Ubuntu Server). El proyecto ya se encuentra ubicado en `/home/sysadmin/Entorno_Configurable/`.
4. Verificar que ambas máquinas se ven entre sí (hacer ping desde Kali al servidor).
5. Lanzar el gestor de niveles (ver sección siguiente).

## Uso del gestor

Al arrancar el sistema, se inicia automáticamente el menú de control. Si se cierra o se necesita volver a abrir, ejecutar:

```bash
sudo python3 /home/sysadmin/Entorno_Configurable/gestor_entorno_configurable.py
```

### Funcionamiento:

1. **Carga de nivel:** Al elegir un nivel, Ansible configura los servicios (Apache, MariaDB, FTP, etc.) y aplica los permisos correspondientes de forma automática.
2. **Validación:** Las banderas encontradas deben introducirse en el apartado de "Verificar Flags" del menú para registrar el progreso.
3. **Limpieza:** Es necesario usar la opción de Reset al finalizar un nivel o antes de cambiar a otro para asegurar que no queden procesos o archivos residuales.

## Resumen de escenarios

| Nivel   | Dificultad | Áreas de auditoría                                          |
|---------|------------|-------------------------------------------------------------|
| Nivel 1 | Básica     | Enumeración de servicios de red y entornos restringidos.    |
| Nivel 2 | Media      | Seguridad en aplicaciones web y bases de datos.             |
| Nivel 3 | Avanzada   | Procesamiento de archivos y escalada de privilegios.        |

## 🎯 Catálogo de vulnerabilidades

| Nivel | Vulnerabilidad | Clasificación |
|---|---|---|
| Básico | Acceso FTP anónimo | CWE-284 |
| Básico | Credenciales en texto plano | CWE-256 |
| Básico | Shell restringida (rbash) | CWE-538 |
| Medio | Inyección SQL | CWE-89 / OWASP A03 |
| Medio | Hash MD5 inseguro | CWE-328 |
| Medio | Subida de ficheros sin validación (RCE) | CWE-434 |
| Difícil | Exposición de información vía robots.txt | CWE-200 |
| Difícil | Subida de ZIP malicioso | CWE-434 |
| Difícil | Escalada de privilegios vía sudo | CWE-269 |

## Credenciales por defecto

| Servicio              | Usuario    | Contraseña |
|-----------------------|------------|------------|
| Acceso al servidor    | sysadmin   | 1234       |

> **Nota de seguridad:** Estas credenciales son exclusivamente para el entorno de laboratorio. Nunca usar contraseñas débiles en sistemas reales.

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| VirtualBox | Virtualización |
| Ubuntu Server 24.04 LTS | Sistema operativo de la máquina víctima |
| Kali Linux | Máquina atacante (aportada por el usuario) |
| Ansible Core | Automatización de la configuración de escenarios |
| Python 3 | Gestor de niveles (solo librería estándar) |
| Apache, MariaDB, vsftpd, PHP | Servicios desplegados según el nivel |

## Notas importantes

- Cada nivel debe resetearse antes de cargar otro para evitar conflictos entre servicios.
- La máquina atacante (Kali) debe poder hacer ping a la IP del servidor antes de comenzar.
- Los detalles específicos de cada vulnerabilidad y los pasos para su resolución están documentados en la memoria técnica del proyecto.

## ⚠️ Aviso

Este laboratorio está diseñado exclusivamente con fines educativos, en entornos de red aislados y de confianza. No debe desplegarse en redes corporativas, compartidas o de producción.

## 👤 Autor

**Eduardo Roda Carrasco**
Grado en Ingeniería Informática — UCAM

---

*Este proyecto forma parte de mi Trabajo de Fin de Grado, "Desarrollo de un Entorno Virtual de Hacking Ético Configurable para la Formación en Seguridad de la Información".*
