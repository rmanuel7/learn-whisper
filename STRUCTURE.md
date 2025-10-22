# [Estructura del servidor Ubuntu](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/1-2-linux-special-directories-users-package-managers#linux-special-directories)

Documentar de forma legible la estructura del proyecto y los cambios importantes.

```py
💻 Servidor Ubuntu /
├── 📂 bin/              # Comandos esenciales del sistema
├── 📂 etc/              # Archivos de configuración
│   ├── 📂 systemd/
│   │   └── 📂 system/
│   │       └── 📄 whisper_daemon.service
│   ├── 📂 apache2/
│   │   └── 📂 sites-available/
│   │       └── 📄 whisper.reincar.app.conf
│   ├── 📂 rabbitmq/
│   │   └── 📄 rabbitmq.conf
│   └── 📂 ssh/
├── 📂 home/             # Directorios de los usuarios
│   ├── 📂 deployer/     # Usuario dedicado para despliegue
│   │   └── 📂 .ssh/
│   │       ├── 📄 authorized_keys
│   │       ├── 📄 id_ed25519
│   │       ├── 📄 id_ed25519.pub
│   │       └── 📄 known_hosts
│   ├── 📂 manager/       # Tu usuario
│   │   ├── 📂 .ssh/
│   │   │   ├── 📄 authorized_keys
│   │   │   ├── 📄 id_rsa
│   │   │   ├── 📄 id_rsa.pub
│   │   │   └── 📄 known_hosts
│   │   └── 📄 setup-rabbitmq.sh # Instalador de RabbitMQ
├── 📂 usr/
│   ├── 📂 local/
│   │   └── 📂 bin/
│   │       └── 📁 whisper_daemon/  # Servicio de transcripcion
│   │           ├── 📂 venv/              # entorno virtual
│   │           └── 📄 whisper_daemon.py  # punto de entrada
├── 📂 var/              # Archivos de datos variables
│   ├── 📂 www/           # Archivos del servidor web (Apache)
│   │   └── 📂 html/
│   │       └── 📁 whisper_api/
│   └── 📄 log/           # Archivos de registro del sistema
└── 📂 ...               # Otros directorios del sistema (boot, usr, media, etc.)
```

> [!NOTE]
> * `/var/lib/`. Este es un directorio estándar de Linux para **datos de aplicaciones y servicios**.
