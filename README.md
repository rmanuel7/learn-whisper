# learn-whisper
Whisper- Instalación y configuración

<br/>

Verificar que **Ubuntu detecta correctamente tu tarjeta NVIDIA** y que **los drivers y CUDA** están instalados.

<br/>

> [!TIP]
> No necesitas hacerlo desde la **BIOS**, todo se hace desde Ubuntu.

<br/>

## 1. Ver qué GPU tienes

### Listar todo el hardware PCI que tiene la palabra "nvidia" en su descripción.

La mayoría de los dispositivos de hardware principales (tarjetas gráficas, tarjetas de red, controladores SATA, etc.) están conectados al PCI.

Ejecuta en la terminal:

```bash
lspci | grep -i nvidia
```

Esto te mostrará algo como:

```bash
user@server:~$ lspci | grep -i nvidia
01:00.0 VGA compatible controller: NVIDIA Corporation Device 2d04 (rev a1)
01:00.1 Audio device: NVIDIA Corporation Device 22eb (rev a1)
```

> [!NOTE]
>  Si aparece “NVIDIA Corporation …”, tu GPU está detectada por el sistema.


<br/>

## 2. Instalar los drivers oficiales de NVIDIA

### Verificar Controladores y Soporte de Ubuntu.

Identificar dispositivos (especialmente tarjetas gráficas) para los cuales hay controladores propietarios recomendados o disponibles en los repositorios de Ubuntu.  

Ubuntu suele detectar automáticamente la GPU, pero puedes instalar los drivers recomendados con:

```bash
sudo ubuntu-drivers devices
```

Verás una salida tipo:

```bash
user@server: $ ubuntu-drivers devices

udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
udevadm hwdb is deprecated. Use systemd-hwdb instead.
ERROR:root:aplay command not found
== /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
modalias : pci:v000010DEd00002D04sv00001462sd00005354bc03sc00i00
vendor   : NVIDIA Corporation
driver   : nvidia-driver-580-server-open - distro non-free
driver   : nvidia-driver-570-server-open - distro non-free
driver   : nvidia-driver-580-server - distro non-free
driver   : nvidia-driver-580 - distro non-free
driver   : nvidia-driver-570-open - distro non-free
driver   : nvidia-driver-570 - distro non-free
driver   : nvidia-driver-570-server - distro non-free
driver   : nvidia-driver-580-open - distro non-free recommended   ← ✅ recomendado
driver   : xserver-xorg-video-nouveau - distro free builtin
```

<br/>

## 3. Instalar el driver recomendado

Ejemplo si el recomendado es `nvidia-driver-580-open`:

```bash
sudo apt install -y nvidia-driver-580-open
sudo reboot
```

> [!NOTE]
> Si el comando `ubuntu-drivers devices` recomienda otro (como 535 o 560), cambia el número por el correcto.

<br/>

## 4. Verificar después del reinicio

Después de reiniciar el servidor:

```bash
sudo nvidia-smi
```

> [!NOTE]
> Si ves una salida como esta:
> 
> ```
> +-----------------------------------------------------------------------------------------+
> | NVIDIA-SMI 580.65.06              Driver Version: 580.65.06      CUDA Version: 13.0     | ← ✅ PyTorch
> +-----------------------------------------+------------------------+----------------------+
> | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
> | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
> |                                         |                        |               MIG M. |
> |=========================================+========================+======================|
> |   0  NVIDIA GeForce RTX 5060 Ti     Off |   00000000:01:00.0 Off |                  N/A |
> |  0%   29C    P8             10W /  180W |       2MiB /  16311MiB |      0%      Default |
> |                                         |                        |                  N/A |
> +-----------------------------------------+------------------------+----------------------+
> 
> +-----------------------------------------------------------------------------------------+
> | Processes:                                                                              |
> |  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
> |        ID   ID                                                               Usage      |
> |=========================================================================================|
> |  No running processes found                                                             |
> +-----------------------------------------------------------------------------------------+
> ```
>
> Tu GPU ya está completamente activa y lista para usar con PyTorch o Whisper.

<br/>
<br/>

## Preparar el entorno de Python

Vamos por partes:

<br/>

## [1.1 Usuario de Servicio Dedicado](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/2-3-1-configure-aspnet-core-application-start-automatically#create-a-new-user-to-run-your-application)

### 1.1.1 Crear el Usuario de Servicio

Crea el usuario `whisperuser`, sin directorio de inicio (`-M`) y sin shell de login (`-s /bin/false`) para mayor seguridad. Utilizaremos `adduser` para crear un usuario del sistema que no puede iniciar sesión directamente:

```bash
sudo adduser --system --no-create-home --shell /bin/false whisperuser
```

> [!NOTE]
> Este comando crea un usuario de sistema (`--system`) llamado `whisperuser` que es seguro porque no tiene un directorio de inicio personal (`--no-create-home`) y no puede ser utilizado para iniciar sesión (`--shell /bin/false`).

### 1.1.2 Asignar Permisos a la Carpeta del Proyecto

El nuevo usuario necesita poder leer y ejecutar el código del servicio. Cambia el dueño del directorio de tu proyecto al nuevo usuario y grupo. Ajusta la ruta si es necesario.

```bash
sudo chown -R whisperuser:www-data /var/www/whisper-api
```

<br/>

## [1.2 Create a Python project](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
<!-- https://code.visualstudio.com/docs/python/python-tutorial -->
```bash
/var/www/whisper-api/
├── venv/                # entorno virtual
├── server_api.py        # punto de entrada de FastAPI
├── requirements.txt
└── app/                 # código fuente (routers, utils, etc.)
```

### Flujo de trabajo

#### Como `administrador` (tu usuario principal)

```bash
sudo mkdir -p /var/www/whisper-api
sudo chown -R administrador:www-data /var/www/whisper-api
cd /var/www/whisper-api
    python3 --version
python3 -m venv venv
source venv/bin/activate
    python3 -m pip install --upgrade pip
    pip --version
👉 pip install -r requirements.txt >> Mas adelante
deactivate
```

#### Dar permisos al usuario del servicio (`whisperuser`) para ejecución

```bash
sudo chown -R whisperuser:www-data /var/www/whisper-api
sudo chmod -R 750 /var/www/whisper-api
```

#### Systemd corre la API como `whisperuser`

```ini
User=whisperuser
Group=www-data
WorkingDirectory=/var/www/whisper-api
ExecStart=/var/www/whisper-api/venv/bin/uvicorn server_api:app --host 127.0.0.1 --port 8000
Restart=always
```

#### Si necesitas administración por FTP/SFTP, crea un usuario adicional

```bash
sudo adduser ftpuser
sudo usermod -a -G www-data ftpuser
sudo chown -R whisperuser:www-data /var/www/whisper-api
sudo chmod -R 775 /var/www/whisper-api
```

De esta forma:

* `ftpuser` puede conectarse y modificar archivos desde FTP/SFTP (gracias al grupo `www-data`).
* `whisperuser` sigue ejecutando el servicio.
* `administrador` conserva control total (root/sudo).

<br/>

### 1.2.1 `Creación` del entorno virtual

> [!NOTE]
> El directorio `/var/www/whisper-api` debe ser creado como **root** (o con `sudo`), luego asignado al usuario `whisperuser`.

Primero creas el **entorno virtual** dentro del proyecto. Desde el directorio `/var/www/whisper-api`:

```bash
cd /var/www/whisper-api
python3 -m venv venv
```

> [!NOTE]
> Esto crea el directorio `venv/` donde vivirán todas las dependencias y el intérprete aislado de Python.

### 1.2.2 `Activación` del entorno virtual

Antes de instalar dependencias o ejecutar la API, **activa el entorno**:

```bash
source venv/bin/activate
```

> [!NOTE]
> Tu terminal mostrará algo como `(venv)` al inicio de la línea.
> ```bash
> user@server:/var/www/whisper-api$ source venv/bin/activate
> ✅ (venv) user@server:/var/www/whisper-api$
> ```

<br/>

### 1.2.3 Instalación de dependencias dentro del entorno

#### [Instalar PyTorch compatible con CUDA 13.0](https://pytorch.org/get-started/locally)

> [!CAUTION]
> La versión de Python es 3.12, pero en el momento de esta interacción, los paquetes precompilados de [PyTorch](https://pytorch.org/get-started/locally/) (los wheels) para CUDA (como cu130) no son compatibles con Python 3.12.  
> 
> ```bash
> (venv) user@server:/var/www/whisper-api$ python3 --version
>     Python 3.12.3
> (venv) user@server:/var/www/whisper-api$ pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
>     Looking in indexes: https://download.pytorch.org/whl/cu130
>     ❌ ERROR: Could not find a version that satisfies the requirement torch (from versions: none)
>     ❌ ERROR: No matching distribution found for torch
> (venv) user@server:/var/www/whisper-api$
> ```

> [!TIP]
> PyTorch has introduced support for CUDA 13.0 in its nightly builds.  

Ejecuta esto en tu entorno (o globalmente si no usas `venv`):

```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu130
```

Luego prueba desde Python:

```css
(venv) user@server:/var/www/whisper-api$ python3
    Python 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.cuda.is_available())
    True
>>> print(torch.cuda.get_device_name(0))
    NVIDIA GeForce RTX 5060 Ti
>>>
```

<br/>

### [1.2.4 Instalar Whisper](https://github.com/openai/whisper)

#### Instalar dependencias

`ffmpeg` es obligatorio — Whisper lo usa para cargar y convertir los audios.

```bash
sudo apt install -y ffmpeg
```

#### Instalar la librería de audio a texto

```bash
pip install --upgrade openai-whisper
```

Y prueba una transcripción rápida:

```bash
whisper audio.mp3 --model small --device cuda
```

Deberías ver que usa la GPU (`cuda`) y el proceso será **muy rápido** comparado con CPU.
