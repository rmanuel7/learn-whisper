# Nota personal

No soy un usuario avanzado de Linux; siempre he trabajado en Windows, pero por razones laborales ahora estoy utilizando **Ubuntu Server** junto con **Python**.
Normalmente programo en ASP.NET Core, y desde que empecé a trabajar en este entorno me he encontrado con un problema muy común: el error

> **"Permission denied (Errno 13)"**,

especialmente en **entornos virtuales**, instalar dependencias o ejecutar scripts dentro de carpetas del sistema.

Este documento resume las causas y los pasos que sigo para resolverlo cada vez que aparece.

> [!CAUTION]
> **Check the permissions.**  
> ERROR: Could not install packages due to an OSError: **[Errno 13] Permission denied**
> 
> ```bash
> user@server:~$ sudo ls -l /usr/local/bin
>     total 0
> 
> user@server:~$ sudo mkdir -p /usr/local/bin/whisper_daemon
> 
> user@server:~$ cd /usr/local/bin/whisper_daemon
> 
> user@server:/usr/local/bin/whisper_daemon$ python3 -m venv venv
>      Error: [Errno 13] Permission denied: '/usr/local/bin/whisper_daemon/venv'
> 
> user@server:/usr/local/bin/whisper_daemon$ sudo python3 -m venv venv
> 
> user@server:/usr/local/bin/whisper_daemon$ source venv/bin/activate
> 
> (venv) user@server:/usr/local/bin/whisper_daemon$ pip install pika
>     Collecting pika
>       Downloading pika-1.3.2-py3-none-any.whl.metadata (13 kB)
>     Downloading pika-1.3.2-py3-none-any.whl (155 kB)
>        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.4/155.4 kB 2.3 MB/s eta 0:00:00
>     Installing collected packages: pika
>     ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied: '/usr/local/bin/whisper_daemon/venv/lib/python3.12/site-packages/pika'
>     Check the permissions.
> 
> (venv) user@server:/usr/local/bin/whisper_daemon$ sudo pip install pika
>     sudo: pip: command not found
> ```


> [!TIP]
> 1. Desactiva el entorno actual
> 
> ```bash
> deactivate
> ```
> 
> 2. Elimina la carpeta del entorno virtual anterior `whisper_daemon`
> ```bash
> sudo rm -rf /usr/local/bin/whisper_daemon
> ```
> 
> 3. Crea la carpeta de tu proyecto
> 
> ```bash
> sudo mkdir -p /usr/local/bin/whisper_daemon
> ```
>
> 3.1 Asignar propiedad recursiva
>
> ```bash
> sudo chown -R whisperuser:daemon-data /usr/local/bin/whisper_daemon
> ```
> 
> 4. Cambiar la propiedad con sudo chown.
> 
> ```bash
> sudo chown administrador:daemon-data /usr/local/bin/whisper_daemon
> ```
> 
> 5. Navega a la carpeta de tu proyecto
> 
> ```bash
> cd /usr/local/bin/whisper_daemon
> ```
> 
> 6. Crea un nuevo venv utilizando el binario de Python
> 
> ```bash
> python3 -m venv venv
> ```
> 
> 7. Activa el nuevo entorno
> ```bash
> source venv/bin/activate
> ```
>
> 8. Instalar dependencias
>
> ```bash
> pip install pika
> ```
> 
> 9. Luego puedes devolverlo
> 
> ```bash
> sudo chown whisperuser:daemon-data /usr/local/bin/whisper_daemon
> ```
> 
