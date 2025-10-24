# Audio Convert

Un consumidor de colas RabbitMQ recibe mensajes (ej. rutas de archivos a convertir), se conecta a AMI de Asterisk vía una librería, y ejecuta el comando `Originate` para correr el contexto de dialplan. 

> [!NOTE]
> ### Esto hace la ejecución asíncrona:
> Envías un mensaje a una cola, y un worker lo procesa.

## Arquitectura

*   **Conectarse a RabbitMQ** (Consumidor).
*   **Recibir el mensaje** (con las rutas `.gsm` y `.wav`).
*   **Comunicarse con Asterisk** usando el **Manager Interface (AMI)**.

> [!NOTE]
> #### El AMI es la API de control de Asterisk.
> Es la forma estándar y programática de iniciar acciones, como ejecutar un Dialplan, sin usar la línea de comandos (`-rx`).

<br/>

### El Agente Bridge

El agente realizará la acción clave de ejecutar el contexto del Dialplan:

| Tarea del Agente | Implementación AMI |
| :--- | :--- |
| **Recibir Tarea** | Lee el mensaje JSON de la cola de RabbitMQ. |
| **Lanzar Dialplan** | Envía una acción `Originate` (similar al comando CLI que usaste antes) al AMI de Asterisk. |

El comando AMI que enviaría el agente sería:

```
Action: Originate
Channel: Local/s@audio-conversion-context
Context: audio-conversion-context
Exten: s
Priority: 1
Application: Dialplan_Convert
Data: /ruta/a/entrada.gsm,/ruta/a/salida.wav
Variable: ARG1=/ruta/a/entrada.gsm,ARG2=/ruta/a/salida.wav
```

### Ventajas de este Enfoque

  * **Desacoplamiento:** El proceso de conversión es asíncrono y escalable. Puedes tener múltiples agentes escuchando la cola y múltiples *workers* de Asterisk procesando llamadas AMI.
  * **Velocidad:** Lenguajes como Go o Node.js son muy rápidos y eficientes para tareas de E/S (como la conexión de red con RabbitMQ y Asterisk).
  * **Independencia:** No dependes de Python. Puedes usar librerías de RabbitMQ nativas de C\# (.NET) para tu agente.

-----

## Implementación

Este patrón es el **estándar de la industria** para integrar Asterisk con sistemas de colas de mensajes escalables.

### [Habilitar AMI en Asterisk](https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/AMI-v2-Specification/)

*   Crear un usuario y una contraseña específicos que tu Agente Bridge usará para autenticarse y enviar comandos a Asterisk.

*   Asegúrate de que `manager.conf` esté configurado para permitir conexiones AMI desde la máquina del agente.

<small>**Archivo**:`/etc/asterisk/manager.conf`</small>

```ini
; /etc/asterisk/manager.conf

[general]
enabled = yes
port = 5038
bindaddr = 0.0.0.0 ; Escucha en todas las interfaces

; -----------------------------------------------------
; Usuario para el Agente de Conversión (Agente Bridge)
; -----------------------------------------------------
[auditorai]
secret = tu_password_secreto
read = all
write = all
```

> [!NOTE]
> #### Recarga Asterisk
> *   **1. Terminal Ubuntu**
>     ```
>     asterisk -rx "manager reload"
>     ```
>     
> *   **2. Entra a la CLI de Asterisk**
>     ```
>     sudo asterisk -rvvv
>     ```
>
>     ```
>     *CLI> manager reload
>     ```
>     **Output**: Manager registered user 'conversion_agent'

<br/>

### [Dialplan contexts](https://docs.asterisk.org/Configuration/Dialplan/Contexts-Extensions-and-Priorities/#dialplan-contexts)

#### [Creating Dialplan Extensions](https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Creating-Dialplan-Extensions/)

Any sections in the dialplan beneath those two sections (`[general]` and `[globals]`) is known as a [context](https://docs.asterisk.org/Configuration/Dialplan/Contexts-Extensions-and-Priorities). 

##### Configurar un dialplan para conversión

Edita el archivo de dialplan `/etc/asterisk/extensions.conf` para **agregar un contexto** que convierta el audio:

```ini
; /etc/asterisk/extensions.conf

[convert-audio]
; Estas variables ${ARG1} y ${ARG2} son pasadas por la acción AMI Originate.
; En AMI, las pasaremos como "Variable: ARG1=/ruta.gsm,ARG2=/ruta.wav"

exten => convert,1,Answer() ; Contesta o activa el canal local para ejecutar la acción
same => n,NoOp(Iniciando conversion de ${ARG1} a ${ARG2}) ; Mensaje de log
same => n,Set(GSM_FILE=${ARG1}) ; Almacena la ruta del archivo GSM
same => n,Set(WAV_FILE=${ARG2}) ; Almacena la ruta del archivo WAV

same => n,Set(FILE=${GSM_FILE})
same => n,Set(DESTFILE=${WAV_FILE})
same => n,Convert(${FILE},${DESTFILE}) ; Ejecuta la transcodificación

same => n,NoOp(Conversion de audio finalizada.)
same => n,Hangup() ; Cuelga o cerrar el canal local después de ejecutar la acción
```

> [!IMPORTANT]
> #### Recarga Asterisk
> En la CLI de Asterisk, ejecuta `dialplan reload` para que los cambios surtan efecto.
> #### Módulo `Convert`
> En versiones recientes de Asterisk (como 20.x), el soporte para `app_convert` puede estar deprecado o no incluido por defecto.
> *   Verifica que `app_convert` esté habilitado en `menuselect` (`make menuselect` -> `Applications`).
> #### Formatos soportados
> Confirma que `format_gsm` y `format_wav` estén habilitados en `menuselect` para evitar errores de compatibilidad.
> #### Ubicación de archivos
> *   Usa `/var/local/auditorai/` para los archivos `.gsm` y `.wav`.
> *   Asegúrate de que Asterisk tenga permisos de lectura/escritura (`sudo chown asterisk:asterisk /var/local/auditorai/`).
> *   `sudo chmod +rw /var/local/auditorai/`

<br/>

### [Using Python AMI to ejecutar el contexto de conversión de dialplan](https://pypi.org/project/asterisk-ami/)

Asterisk no tiene soporte nativo directo para RabbitMQ en el dialplan, pero puedes integrar ambos mediante **Asterisk AMI (Asterisk Manager Interface)** o **ARI (Asterisk REST Interface)** con un proxy o middleware **que use RabbitMQ** para encolar tareas.

#### Implementación en Python (usando pika para RabbitMQ y pyst2 para AMI):

*   Instala dependencias: `pip install pika asterisk.ami`.

*   Productor (envía tarea a la cola): Crea `main.py` como un proxy **que use RabbitMQ** para encolar tareas:

```py
    def on_convert_request(self, event):
        """Callback cuando llega un mensaje RabbitMQ."""
        gsm_path = event.get("gsm_path")
        wav_path = event.get("wav_path")

        self.trace.conversion_requested(gsm_path, wav_path)

        try:
            client = self.connect_ami()
            self.trace.conversion_started(gsm_path, wav_path)

            action = SimpleAction(
                'Originate',
                Channel='Local/convert@convert-audio',
                Context='convert-audio',
                Exten='convert',
                Priority=1,
                CallerID='AudioConverter',
                Variable=f'ARG1={gsm_path},ARG2={wav_path}'
            )

            response = client.send_action(action, timeout=10)
            self.trace.conversion_successful(gsm_path, wav_path, response.response)

            client.logoff()

        except Exception as ex:
            self.trace.conversion_failed(gsm_path, wav_path, ex)
```

<br/>

### Configuration Files

This location `audetcdir => /etc/auditorai` is used to store and read AuditorAI configuration files.

**Archivo:** `/etc/auditorai/transcoding.conf`

```ini
[RabbitMQ]
HostName  = localhost
QueueName = Asterisk.Transcoding

[AsteriskAMI]
Addr   = 127.0.0.1
Port   = 5038
User   = auditorai
Secret = "Tu6...JYL"

[Logging]
MinimumLevel = CRITICAL # DEBUG | INFO | WARNING | ERROR | CRITICAL

[GitHub]
RepoOwner   = "PatternLib"
RepoName    = "reincar-auditorai"
GitHubToken = "github_pat_11BI...MAmOm3fXlb"
```


<br/>

## Configuración de usuario y permisos

Crear un usuario con privilegios mínimos para que el servicio ASP.NET Core pueda acceder y gestionar el directorio de almacenamiento de forma segura, sin tener acceso a otras partes sensibles del sistema.

<br/>

> [!NOTE]
> **Nunca** deberías ejecutar servicios que no necesiten privilegios de root con el usuario `root`.  
> Una buena práctica de seguridad y de gestión de sistemas es crear un usuario y un grupo dedicados.

<br/>

La siguiente secuencia de comandos, ejecutada **una sola vez** en el servidor, garantiza que tu **usuario de servicio** pueda ejecutar la aplicación y que tu **usuario de despliegue** pueda escribir en la carpeta.

```coffeescript
# 1. Crear el grupo de servicio, solo sino esta definido
sudo addgroup "reincar-auditorai"

# 2. Crear el usuario de bajo privilegio
# Usamos --system y --no-create-home ya que es un usuario de servicio
# 2.1. Este usuario será para ejecutar el servicio proxy **que use RabbitMQ** para encolar tareas. 
sudo adduser --system --no-create-home --shell "/bin/false" auditorai-audio

# 2.2. Este usuario será el propietario de los archivos y directorios de almacenamiento. 
sudo adduser --system --no-create-home --shell "/bin/false" auditorai-data

# 3. Añadir los usuario relacionados con el servicio al grupo (Asegúrate que sean los nombres correctos)
sudo usermod --append --groups "reincar-auditorai" "auditorai-audio"

sudo usermod --append --groups "reincar-auditorai" "auditorai-data"

sudo usermod --append --groups "reincar-auditorai" "asterisk"

sudo usermod --append --groups "reincar-auditorai" "auditorai-deploy"

# 4 Crea la carpeta
# 4.1 Carpeta del proyecto
sudo mkdir --parents "/usr/local/bin/auditorai/transcoding"

# 4.2. Carpeta raíz del almacenamiento, solo sino existen
sudo mkdir --parents "/var/local/auditorai/gsm"

sudo mkdir --parents "/var/local/auditorai/wav"

sudo mkdir --parents "/var/local/auditorai/transcription"

sudo mkdir --parents "/var/local/auditorai/completions"

# 5. Asignar la propiedad de la carpeta
# 5.1. Carpeta de del servicio al usuario de servicio y al grupo de servicio
sudo chown --recursive "auditorai-audio:reincar-auditorai" "/usr/local/bin/auditorai/transcoding"

# 5.1. Carpeta de almacenamiento al usuario de almacenamiento y al grupo de almacenamiento.
sudo chown --recursive "auditorai-data:reincar-auditorai" "/var/local/auditorai/"

# 6. 🚨 CRÍTICO: Asignar permisos 775 para permitir la escritura del grupo
# Esto significa:
#   - Propietario: Lectura, Escritura, Ejecución (7)
#   - Grupo (auditorai-data): Lectura, Escritura, Ejecución (7) <- Clave para el despliegue
#   - Otros: Lectura, Ejecución (5)
sudo chmod --recursive 775 "/usr/local/bin/auditorai/transcoding" # Propietario (auditorai-audio)

sudo chmod --recursive 775 "/var/local/auditorai/"                # Propietario (auditorai-data)

# [Opcional] Paso 7: Activar el bit 'setgid'
# Esto hace que todas las carpetas y archivos nuevos dentro de `/var/local/auditorai/` hereden el grupo `reincar-auditorai`
sudo chmod g+s "/var/local/auditorai/"
```

> [!TIP]
> Una vez que te asegures de que todos los permisos de archivo están en su lugar, el *workflow* de despliegue debe funcionar de manera fluida.

> [!NOTE]
> *   `--system`: Crea un usuario de sistema, lo que indica que no es un usuario interactivo.
> *   `--no-create-home`: No crea un directorio de inicio, ya que el servicio no lo necesita.
> *   `--shell /bin/false`: No puede ser utilizado para iniciar sesión.

> [!NOTE]
> *   Asegúrate de que los audios estén en `/var/local/auditorai/` y tenga permisos de lectura/escritura.
> *   `/var/local/` parece ser el lugar convencional y este directorio debería estar vacío en una instalación nueva.

> [!NOTE]
> *   Asegúrate de que tus scripts estén en `/usr/local/bin` y sean ejecutables.
> *   `/usr/local/bin` parece ser el lugar convencional y este directorio debería estar vacío en una instalación nueva.

> [!NOTE]
> Nota la `s` en lugar de la `x` del grupo — eso indica que el **setgid** está activo.
> *   `sudo chmod g+s "/var/local/auditorai/"`

<br/>

## Configurar el servicio con `systemd`

### Definición del Servicio `systemd`.

Debes crear un archivo de unidad de servicio llamado `auditorai-transcodingpy.service` en el directorio `/etc/systemd/system/`.

```sh
sudo vim /etc/systemd/system/auditorai-transcodingpy.service
```

**Archivo:** `/etc/systemd/system/auditorai-transcodingpy.service`

```ini
[Unit]
# Descripción legible del servicio
Description=Python Audio Transcoding (RabbitMQ + Asterisk AMI)
# Asegura que el servicio se inicie DESPUÉS de que la red y RabbitMQ estén disponibles
After=network.target rabbitmq-server.service asterisk.service

[Service]
# Usuario y grupo bajo los cuales se ejecutará el proceso
User=auditorai-audio
Group=reincar-auditorai

# Esto asegura que los archivos se creen como rw-rw-r-- en lugar de rw-r--r--.
UMask=0002

# Directorio de trabajo
WorkingDirectory=/usr/local/bin/auditorai/transcoding

# Comando para EJECUTAR el servicio
# Apunta al intérprete Python dentro del entorno virtual para usar las dependencias aisladas.
ExecStart=/usr/local/bin/auditorai/transcoding/venv/bin/python main.py

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

> [!IMPORTANT]
> #### Prerrequisito en el Servidor Ubuntu
> Debes tener configurado un servicio `systemd` en tu servidor Ubuntu
> #### Configurar la `UMask` del servicio `systemd`
> Esto asegura que los archivos se creen como `rw-rw-r--` en lugar de `rw-r--r--`.


### Habilita y arranca el servicio:

```sh
sudo systemctl daemon-reload
sudo systemctl enable auditorai-transcodingpy.service
sudo systemctl start auditorai-transcodingpy.service
```

### Verifica el estado del servicio para asegurarte de que está funcionando correctamente con el usuario correcto:

```sh
sudo systemctl status auditorai-transcodingpy.service

sudo journalctl -fu auditorai-transcodingpy.service
```



