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
> **Nunca** deberías ejecutar servicios que no necesiten privilegios de root con el usuario `root`. Una buena práctica de seguridad y de gestión de sistemas crear un usuario y un grupo dedicados.

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

<br/>

## Código del servicio

Aquí debe de ir el código completo y depurado, con la lógica de ASP.NET Core para la gestión del almacenamiento.

> [!NOTE]
> [Codigo](https://github.com/PatternLib/reincar-auditorai)

<br/>

## Install .NET Core

- The first command is a `wget` command. `wget` is a non-interactive network downloader.
  ```bash
  wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
  ```

- In the second command, `dpkg` is the package manager for Debian and Ubuntu. This command adds the Microsoft package signing key to the list of trusted keys, and then adds the package repository.
  ```bash
  sudo dpkg -i packages-microsoft-prod.deb
  ```

- The **ASP.NET Core Runtime** allows you to run apps that were made with .NET that didn't provide the runtime.
  ```bash
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
Environment=ASPNETCORE_URLS=http://+:5103
# Habilita el log estándar de Systemd
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

> [!IMPORTANT]
> #### Prerrequisito en el Servidor Ubuntu
> Debes tener configurado un servicio `systemd` en tu servidor Ubuntu

> [!NOTE]
> Después de crear este archivo, lo habilitarías con `sudo systemctl enable storing-api.service`.

<br/>

## Apache Config

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

    # Redirige todo el tráfico a la aplicación Kestrel en el puerto SEGURO 5101
    ProxyPass / https://127.0.0.1:5103/
    ProxyPassReverse / https://127.0.0.1:5103/

    # Agrega el encabezado "X-Forwarded-Proto: https"
    RequestHeader set X-Forwarded-Proto "https"
    
    # Esto es crucial para manejar la comunicación de Kestrel con https
    SSLProxyEngine On
</VirtualHost>
```

