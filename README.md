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
