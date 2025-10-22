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
> Usa `/usr/local/src` para los archivos `.gsm`, como indicaste. Asegúrate de que Asterisk tenga permisos de lectura/escritura (`sudo chown asterisk:asterisk /usr/local/src`).
> *   `sudo chmod +rw /path/to/`

<br/>

2.  **Crear el Agente Bridge:** Desarrolla un servicio ligero (en C\# .NET, por ejemplo, usando `RabbitMQ.Client` y una librería AMI para C\#) que escuche la cola de RabbitMQ.
3.  **Enviar Acción AMI:** Cuando el agente reciba un mensaje, inmediatamente envía una acción `Originate` al AMI, pasando las rutas de archivo como variables al `[audio-conversion-context]` que ya definiste en `extensions.conf`.


