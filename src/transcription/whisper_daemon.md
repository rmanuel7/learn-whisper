# Transcripcion

Un **servicio de *backend*** dedicado (el Daemon de Python con Whisper) que maneja las tareas pesadas de transcripción.  

Este es un proceso que se ejecuta de forma continua, "escuchando" en la cola de RabbitMQ para nuevos mensajes. Su única responsabilidad es procesar esos mensajes, transcribir el archivo y realizar cualquier otra tarea pesada.

## Arquitectura

La arquitectura se basará en el patrón de **Productor/Consumidor** y la **Comunicación Asíncrona**.

1.  **Productor (API ASP.NET Core):**
      * Recibe la solicitud del cliente (archivo de audio).
      * Guarda el archivo de audio.
      * Envía un **mensaje** (que contiene la ruta del archivo o un identificador) a la cola de RabbitMQ.
      * Responde inmediatamente al cliente con un **ID de Tarea** y el estado "En proceso".
2.  **Cola de Mensajes (RabbitMQ):**
      * Actúa como un *buffer* y garantiza la entrega del mensaje.
3.  **Consumidor (Daemon de Python con Whisper):**
      * Escucha la cola de RabbitMQ.
      * Al recibir un mensaje, carga el audio, realiza la **transcripción con Whisper**.
      * Guarda el resultado
      * Envía a una cola el **ID de Tarea** para que la API lo recupere o para que otro servicio lo procese.

<br/>

## Configurar los permisos y usuario

Una buena práctica de seguridad y de gestión de sistemas crear un usuario y un grupo dedicados para ejecutar tus scripts de daemon. 

<br/>

> [!NOTE]
> **Nunca** deberías ejecutar servicios que no necesiten privilegios de root con el usuario `root`.

<br/>

Primero, necesitamos configurar el sistema creando el usuario de bajo privilegio y el entorno de trabajo para el script `rabbitmq_consumer_test.py`.

### Crear un grupo.

```sh
sudo addgroup daemon-data
```

### Crea el usuario `whisperuser`.

```sh
sudo adduser --system --no-create-home --shell /bin/false whisperuser
```

> [!NOTE]
> `--system`: Crea un usuario de sistema, no un usuario interactivo.  
> `--no-create-home`: No crea un directorio de inicio, ya que el daemon no lo necesita.  
> `--shell /bin/false`: No puede ser utilizado para iniciar sesión.

### Añadir el usuario al grupo:

```sh
sudo usermod -a -G daemon-data whisperuser
```

### Crea la carpeta de tu proyecto

```sh
sudo mkdir -p /usr/local/bin/whisper_daemon
```

> [!NOTE]
> Asegúrate de que tus scripts estén en `/usr/local/bin` y sean ejecutables.  
> `/usr/local/bin` parece ser el lugar convencional y este directorio debería estar vacío en una instalación nueva.

### Asignar propiedad de la carpata de forma recursiva

```sh
sudo chown -R whisperuser:daemon-data /usr/local/bin/whisper_daemon
```

<br/>

## Código del Daemon

Aquí debe de ir el código completo y depurado, con la lógica robusta de `pika` para conectarse a RabbitMQ, recibir el mensaje y coordinar la transcripción con Whisper.

### Cambiar la propiedad temporalmente con `sudo chown`.

```sh
sudo chown administrador:daemon-data /usr/local/bin/whisper_daemon
```

### Navega a la carpeta de tu proyecto

```sh
cd /usr/local/bin/whisper_daemon
```

### Crea un nuevo venv utilizando el binario de Python

```sh
python3 -m venv venv
```

### Activa el nuevo entorno

```sh
source venv/bin/activate
```

### Instalar dependencias

```sh
pip install pika
```

### Devolver la propiedad de la carpeta al usuario

```sh
sudo chown whisperuser:daemon-data /usr/local/bin/whisper_daemon
```

<br/>

## Configurar el servicio con `systemd`

### Definición del Servicio `systemd`.

Debes crear un archivo de unidad de servicio llamado `whisper_daemon.service` en el directorio `/etc/systemd/system/`.

```sh
sudo vim /etc/systemd/system/whisper_daemon.service
```

**Archivo:** `/etc/systemd/system/whisper_daemon.service`

```ini
[Unit]
# Descripción legible del servicio
Description=Whisper RabbitMQ Consumer Daemon
# Asegura que el servicio se inicie DESPUÉS de que la red y RabbitMQ estén disponibles
After=network.target rabbitmq-server.service

[Service]
# USUARIO CLAVE: Ejecuta el proceso con el usuario de bajo privilegio
User=whisperuser
Group=whisperuser

# Directorio de trabajo
WorkingDirectory=/usr/local/bin/whisper_daemon

# Comando para EJECUTAR el servicio
# Apunta al intérprete Python dentro del entorno virtual para usar las dependencias aisladas.
ExecStart=/usr/local/bin/whisper_daemon/venv/bin/python rabbitmq_consumer_test.py

# Tipo de proceso
Type=simple

# Opciones de robustez: Reinicia el servicio automáticamente si falla, con una pausa de 5 segundos.
Restart=always
RestartSec=5

# Redirecciona la salida estándar y de error al registro de systemd (journalctl)
StandardOutput=journal
StandardError=journal

[Install]
# Indica que este servicio debe iniciarse cuando el sistema esté completamente multiusuario (arranque)
WantedBy=multi-user.target
```

### Habilita y arranca el servicio:

```sh
sudo systemctl daemon-reload
sudo systemctl enable whisper_daemon.service
sudo systemctl start whisper_daemon.service
```

### Verifica el estado del servicio para asegurarte de que está funcionando correctamente con el usuario correcto:

```sh
sudo systemctl status whisper_daemon.service
```




