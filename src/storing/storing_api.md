# Storing API

Arquitectura de almacenamiento **On-Premise** estructurado para emular la funcionalidad de Azure Storage Containers para gestionar las subcarpetas que actuarán como "contenedores" de almacenamiento.

## Arquitectura

1.  **Backend ASP.NET Core:**
    *   Capa de abstracción para la gestión del almacenamiento, permitiendo que otros microservicios o aplicaciones cliente interactúen con el almacenamiento a través de una API estandarizada, desacoplando la lógica de la aplicación del sistema de archivos subyacente.
    *   Ofrece endpoints RESTful para realizar operaciones sobre los "contenedores" y "blobs" (archivos).
2.  **Sistema de Archivos Linux:**
    *   Utiliza directorios del sistema de archivos en `/var/www/auditorai/storage` para simular contenedores de almacenamiento.
    *   Las subcarpetas dentro de este directorio actúan como contenedores lógicos, lo que permite una organización clara y escalable de los datos.

<br/>

## Configuración de usuario y permisos

Crear un usuario con privilegios mínimos para que el servicio ASP.NET Core pueda acceder y gestionar el directorio de almacenamiento de forma segura, sin tener acceso a otras partes sensibles del sistema.

<br/>

> [!NOTE]
> **Nunca** deberías ejecutar servicios que no necesiten privilegios de root con el usuario `root`.  
> Una buena práctica de seguridad y de gestión de sistemas es crear un usuario y un grupo dedicados.

<br/>

La siguiente secuencia de comandos, ejecutada **una sola vez** en el servidor, garantiza que tu usuario de servicio (`auditoraidatamanager`) pueda ejecutar la aplicación y que tu usuario de despliegue (`deployer`) pueda escribir en la carpeta.

```coffeescript
# 1. Crear el grupo de servicio (auditorai-data)
sudo addgroup auditorai-data

# 2. Crear el usuario de bajo privilegio (auditoraidatamanager)
# Usamos --system y --no-create-home ya que es un usuario de servicio Kestrel
sudo adduser --system --no-create-home --shell "/bin/false" auditoraidatamanager

# 3. Añadir el usuario de servicio al grupo
sudo usermod --append --groups auditorai-data auditoraidatamanager

# 4. Añadir el usuario de despliegue al grupo (Asegúrate de que 'deployer' es el nombre correcto)
sudo usermod --append --groups auditorai-data deployer

# 5. Crear la carpeta raíz del almacenamiento
sudo mkdir --parents "/var/www/auditorai/storage"

# 6. Asignar la propiedad de la carpeta al usuario de servicio y al grupo de servicio
sudo chown --recursive auditoraidatamanager:auditorai-data "/var/www/auditorai/storage"

# 7. 🚨 CRÍTICO: Asignar permisos 775 para permitir la escritura del grupo
# Esto significa:
#   - Propietario (auditoraidatamanager): Lectura, Escritura, Ejecución (7)
#   - Grupo (auditorai-data): Lectura, Escritura, Ejecución (7) <- Clave para el despliegue
#   - Otros: Lectura, Ejecución (5)
sudo chmod --recursive 775 "/var/www/auditorai/storage"

# [Opcional] Paso 8: Activar el bit “setgid”
# Esto hace que todas las carpetas y archivos nuevos dentro de /var/www/auditorai/storage hereden el grupo auditorai-data
sudo chmod g+s "/var/www/auditorai/storage"
```

-----

### Resumen de los Problemas Resueltos con esta Configuración

Con esta configuración en el servidor, los siguientes problemas que experimentaste quedan resueltos:

| Problema | Causa | Solución en la Configuración |
| :--- | :--- | :--- |
| **`tar: Cannot open: Permission denied`** | El usuario de despliegue (que ejecuta `tar` o `dotnet publish`) no podía escribir en la carpeta de destino. | El comando `chmod 775` da permisos de **Escritura** al grupo `auditorai-data`, al que pertenece el usuario `deployer`. |
| **`Access to the path '/etc/ssl/certs/...' is denied`** | El usuario de servicio (`auditoraidatamanager`) no podía leer el certificado SSL. | Al ser miembro del grupo `auditorai-data`, solo necesitas ejecutar `sudo chgrp auditorai-data /etc/ssl/certs/reincar.app.pfx` y `sudo chmod g+r /etc/ssl/certs/reincar.app.pfx` para darle permiso de lectura al grupo. |
| **`sudo: a password is required`** | El usuario de despliegue no podía usar `sudo` para comandos de limpieza o reinicio. | (Requiere un paso adicional) Configurar `sudoers` en el servidor para permitir `NOPASSWD` para los comandos `systemctl restart`. |

> [!NOTE]
> Una vez que te asegures de que todos los permisos de archivo están en su lugar, el *workflow* de despliegue debe funcionar de manera fluida.

<br/>

### Crear un grupo para la API de almacenamiento. 

Este grupo servirá para gestionar fácilmente los permisos sobre los directorios de almacenamiento. 

```coffeescript
sudo addgroup auditorai-data
```

### Crear un usuario de bajo privilegio para ejecutar el servicio. 

Este usuario será el propietario de los archivos y directorios gestionados por la API. 

```scss
sudo adduser --system --no-create-home --shell /bin/false auditoraidatamanager
```

> [!NOTE]
> *   `--system`: Crea un usuario de sistema, lo que indica que no es un usuario interactivo.
> *   `--no-create-home`: No crea un directorio de inicio, ya que el servicio no lo necesita.
> *   `--shell /bin/false`: No puede ser utilizado para iniciar sesión.

### Añadir el usuario al grupo `auditorai-data`. 

```scss
sudo usermod --append --groups auditorai-data auditoraidatamanager
```

### Añadir el usuario de despliegue al grupo `auditorai-data`.

```scss
sudo usermod --append --groups auditorai-data deployer
```

### Crear la carpeta raíz del almacenamiento.

Asegúrate de que la ruta coincida con la configuración de tu API.

```scss
sudo mkdir --parents /var/www/auditorai/storage
```

### Asignar la propiedad de la carpeta de forma recursiva.

El usuario y grupo `auditoraidatamanager:auditorai-data` tendrán control sobre el directorio de almacenamiento.

```scss
sudo chown --recursive auditoraidatamanager:auditorai-data /var/www/auditorai/storage
```

### [Opcional] Activar el bit `setgid`

Esto hace que todas las carpetas y archivos nuevos dentro de `/var/www/auditorai/storage` hereden el grupo `auditorai-data`

```scss
sudo chmod g+s "/var/www/auditorai/storage"
```

> [!NOTE]
> Nota la `s` en lugar de la `x` del grupo — eso indica que el **setgid** está activo.

<br/>

## Código del servicio

Aquí debe de ir el código completo y depurado, con la lógica de ASP.NET Core para la gestión del almacenamiento.

> [!NOTE]
> [Codigo](https://github.com/PatternLib/reincar-auditorai)

<br/>

## Install .NET Core

<small>[Install .NET Core](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/1-3-install-dotnet-core-linux#install-net-core)</small>  
<small>[Install .NET SDK or .NET Runtime on Ubuntu](https://learn.microsoft.com/en-us/dotnet/core/install/linux-ubuntu-install?tabs=dotnet8&pivots=os-linux-ubuntu-2404)</small>

### Install the SDK

The .NET SDK allows you to develop apps with .NET. If you install the .NET SDK, you don't need to install the corresponding runtime. To install the .NET SDK, run the following commands:

```sh
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-8.0
```

### Install the runtime

The ASP.NET Core Runtime allows you to run apps that were made with .NET that didn't provide the runtime. The following commands install the ASP.NET Core Runtime, which is the most compatible runtime for .NET. In your terminal, run the following commands:

```sh
sudo apt-get update && \
  sudo apt-get install -y aspnetcore-runtime-8.0
```

> [!TIP]
> .NET Core packages are named in the format of {**product**}-{**type**}-{**version**}

<br/>

## Configurar el servicio con `systemd`

`systemd` se puede utilizar para crear un archivo de servicio para iniciar y monitorear la aplicación web subyacente. `systemd` es un sistema de inicio que proporciona muchas funciones potentes para iniciar, detener y administrar procesos.

<small>[Sample service file for ASP.NET Core applications](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/2-3-configure-aspnet-core-application-start-automatically#sample-service-file-for-aspnet-core-applications)</small>  
<small>[Create the service file](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/linux-nginx?view=aspnetcore-9.0&tabs=linux-ubuntu#create-the-service-file)</small>

### Definición del Servicio `systemd`.

Debes crear un archivo de unidad de servicio llamado `auditorai-storingapi.service` en el directorio `/etc/systemd/system/`.

```sh
sudo vim /etc/systemd/system/auditorai-storingapi.service
```

**Archivo:** `/etc/systemd/system/auditorai-storingapi.service`

```ini
# /etc/systemd/system/auditorai-storingapi.service
# sudo systemctl enable auditorai-storingapi.service
# sudo systemctl start auditorai-storingapi.service
# sudo systemctl daemon-reload

[Unit]
Description=AuditorAI Storing .NET Web API Service
# Asegura que se espere a que la red esté activa
After=network.target

[Service]
# Ruta donde se encuentra el ejecutable .NET
WorkingDirectory=/var/www/auditorai/storage
# El comando para iniciar la aplicación. 'dotnet' debe estar instalado.
# El ejecutable principal es el nombre de la DLL (por defecto: NombreProyecto.dll)
ExecStart=/usr/bin/dotnet /var/www/auditorai/storage/Reincar.AuditorAI.Services.Storing.API.dll
# Reiniciar el servicio siempre que se detenga
Restart=always
# Reiniciar después de un breve retraso
RestartSec=10
# Señal que se envía cuando presionas Ctrl+C en la terminal
KillSignal=SIGINT
# Esto asegura que los archivos se creen como rw-rw-r-- en lugar de rw-r--r--.
UMask=0002
# Etiqueta asignada a todos los mensajes que el servicio envía al sistema de registro (syslog)
SyslogIdentifier=auditorai-storage
# Usuario y grupo bajo los cuales se ejecutará la API (debe tener permisos en /var/www/auditorai/storage)
User=auditoraidatamanager
Group=auditorai-data
# Variables de entorno opcionales (por ejemplo, dónde escuchar Kestrel)
Environment=ASPNETCORE_ENVIRONMENT=Production
# Silenciar la salida de mensajes de bienvenida y telemetría de las herramientas de la interfaz de línea de comandos (CLI) de .NET
Environment=DOTNET_NOLOGO=true
# Kestrel debe escuchar en localhost:5000 (o el puerto que configures)
Environment=ASPNETCORE_URLS=http://0.0.0.0:5103;https://0.0.0.0:7103
Environment=Kestrel__Certificates__Default__Path=/etc/ssl/certs/reincar.app.pfx
Environment=Kestrel__Certificates__Default__Password={__password__}
# Habilita el log estándar de Systemd
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

> [!IMPORTANT]
> #### Prerrequisito en el Servidor Ubuntu
> Debes tener configurado un servicio `systemd` en tu servidor Ubuntu
> #### Configurar la `UMask` del servicio `systemd`
> Esto asegura que los archivos se creen como `rw-rw-r--` en lugar de `rw-r--r--`.


Agrega lo siguiente:

[Service]
UMask=0002

> [!NOTE]
> Después de crear este archivo, lo habilitarías con `sudo systemctl enable storing-api.service`.

<br/>

## Apache Config

### [Update and upgrade packages](https://learn.microsoft.com/en-us/windows/wsl/setup/environment#update-and-upgrade-packages)

We recommend that you regularly update and upgrade your packages using the preferred package manager for the distribution. For Ubuntu or Debian, use the command:

```coffeescript
sudo apt update && sudo apt upgrade
```

### [Upgrade the package manager database](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/1-2-linux-special-directories-users-package-managers#upgrade-the-package-manager-database)

#### To update the package database on Ubuntu

```coffeescript
sudo apt update
```

> [!NOTE]
> *   The update command **doesn't actually upgrade** any of the installed software packages.
> *   Instead, it updates the package database.

#### To upgrade any of the installed software packages on Ubuntu

```coffeescript
sudo apt upgrade
```

### [Install the package](https://ubuntu.com/tutorials/install-and-configure-apache#1-overview)
 
To install Apache, install the latest meta-package apache2 by running:

```coffeescript
sudo apt update
sudo apt install apache2
```

### [Configure Apache2 for HTTPS](https://documentation.ubuntu.com/server/how-to/web-services/use-apache2-modules/#configure-apache2-for-https)

The `mod_ssl` module adds an important feature to the Apache2 server - the ability to encrypt communications.

```coffeescript
sudo a2enmod ssl
```

Restart the service to enable the new settings:

```coffeescript
sudo systemctl restart apache2.service
```

### [Enable Reverse Proxy on Apache2](https://www.digitalocean.com/community/tutorials/how-to-use-apache-http-server-as-reverse-proxy-using-mod_proxy-extension)

To enable these four modules

```coffeescript
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod headers
sudo a2enmod rewrite
```

### [Setting up the VirtualHost Configuration File](https://ubuntu.com/tutorials/install-and-configure-apache#4-setting-up-the-virtualhost-configuration-file)

To configurate the server proxy funcionality

**Archivo:** `/etc/apache2/sites-available/auditorai-storingapi.conf`

```yml
# /etc/apache2/sites-available/auditorai-storingapi.conf
# Habilita el Virtual Host: sudo a2ensite auditorai-storingapi.conf
# Reinicia Apache: sudo systemctl restart apache2

<VirtualHost *:80>
    ServerName auditoraidata.reincar.app
    # Ya no se necesita ProxyPass aquí, solo la redirección
    
    # Redirección HTTP a HTTPS
    Redirect permanent / https://auditoraidata.reincar.app/

    ErrorLog ${APACHE_LOG_DIR}/auditoraidata-error.log
    CustomLog ${APACHE_LOG_DIR}/auditoraidata-access.log combined
</VirtualHost>

<VirtualHost *:443>
    # Subdominio
    ServerName auditoraidata.reincar.app
    
    # Directorio de logs
    ErrorLog ${APACHE_LOG_DIR}/auditoraidata-ssl-error.log
    CustomLog ${APACHE_LOG_DIR}/auditoraidata-ssl-access.log combined

    # CONFIGURACIÓN SSL
    SSLEngine On
    # RUTA A TUS ARCHIVOS DE CERTIFICADO (AJUSTA ESTAS RUTAS)
    SSLCertificateFile /etc/ssl/certs/reincar.app.crt
    SSLCertificateKeyFile /etc/ssl/certs/reincar.app.key

    # CONFIGURACIÓN DEL PROXY
    
    # Habilita el reenvío de encabezados para el host
    ProxyPreserveHost On

    # Redirige todo el tráfico a la aplicación Kestrel en el puerto SEGURO 7103
    ProxyPass / https://127.0.0.1:7103/
    ProxyPassReverse / https://127.0.0.1:7103/

    # Agrega el encabezado "X-Forwarded-Proto: https"
    RequestHeader set X-Forwarded-Proto "https"
    
    # Esto es crucial para manejar la comunicación de Kestrel con https
    SSLProxyEngine On
</VirtualHost>
```
