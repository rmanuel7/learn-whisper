# NVIDIA System Management Interface

Es una tabla de la salida del comando **`nvidia-smi`** (NVIDIA System Management Interface), que es esencial para **monitorear el estado** de las tarjetas gráficas NVIDIA.

> [!NOTE]
> Es una herramienta muy poderosa, pero su formato puede ser un poco denso.
>
> ```
> +-----------------------------------------------------------------------------------------+
> | NVIDIA-SMI 580.65.06              Driver Version: 580.65.06      CUDA Version: 13.0     |
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

<br/>

Aquí tienes una descripción detallada y más comprensible de cada sección y valor que muestra tu salida.

<br/>

## Análisis Detallado de `nvidia-smi`

La salida se divide en dos secciones principales: **Información del Sistema y la GPU** y **Procesos en Ejecución**.

### 1. Información de la Tarjeta Gráfica y Software

Esta sección te da una visión general del sistema y los detalles en tiempo real de tu GPU.

| Campo | Valor en tu tabla | Significado |
| :--- | :--- | :--- |
| **`NVIDIA-SMI`** | `580.65.06` | La **versión del software de utilidad** de administración de NVIDIA que estás usando. |
| **`Driver Version`** | `580.65.06` | La **versión del controlador** de NVIDIA que está instalado y activo en tu sistema operativo. |
| **`CUDA Version`** | `13.0` | La **versión de CUDA** (Compute Unified Device Architecture) soportada por este controlador. CUDA es la plataforma de computación paralela de NVIDIA, vital para el *deep learning* y el cálculo intensivo. |

<br/>

### 2. Estado de la GPU (NVIDIA GeForce RTX 5060 Ti)

Esta subsección muestra métricas vitales de rendimiento y salud de la tarjeta gráfica en el momento de la consulta.

#### Identificación y Configuración

| Columna | Valor en tu tabla | Significado |
| :--- | :--- | :--- |
| **`GPU`** | `0` | El **índice de la tarjeta gráfica**. Si tuvieras varias, se numerarían (0, 1, 2, etc.). |
| **`Name`** | `NVIDIA GeForce RTX 5060 Ti` | El **modelo exacto** de tu tarjeta gráfica. |
| **`Persistence-M`** | `Off` | **Modo de Persistencia.** Indica si el controlador se mantiene cargado constantemente. `Off` significa que el controlador se carga y descarga según sea necesario (típico en sistemas de escritorio). |
| **`Bus-Id`** | `00000000:01:00.0` | La **dirección del bus PCI** donde está conectada la GPU. Útil para diagnósticos de bajo nivel. |
| **`Disp.A`** | `Off` | **Display Active.** Indica si la GPU está siendo utilizada actualmente para **mostrar gráficos** en un monitor. `Off` sugiere que no está en uso activo para el escritorio/entorno gráfico. |
| **`Volatile Uncorr. ECC`** | `N/A` | **Errores ECC Volátiles No Corregidos.** Muestra la cuenta de errores de memoria (ECC). `N/A` (No Aplicable) es común en tarjetas de consumo (como las RTX), ya que no suelen soportar ECC. |

#### Métricas en Tiempo Real (Filas 2 y 3)

| Columna | Valor en tu tabla | Significado |
| :--- | :--- | :--- |
| **`Fan`** | `0%` | **Velocidad del ventilador** de la GPU, expresada como porcentaje de su capacidad máxima. `0%` es normal si la tarjeta está fría (29C). |
| **`Temp`** | `29C` | **Temperatura actual** del chip de la GPU en grados Celsius. ¡Tu tarjeta está muy fría! |
| **`Perf`** | `P8` | **Nivel de Rendimiento** (Performance State). `P8` es un estado de muy baja potencia y bajo rendimiento, ideal cuando la GPU está inactiva. `P0` sería el estado de máximo rendimiento. |
| **`Pwr:Usage/Cap`** | `10W / 180W` | **Consumo de Energía.** `10W` es lo que está consumiendo ahora; `180W` es el límite de potencia (capacidad) de la tarjeta. |
| **`Memory-Usage`** | `2MiB / 16311MiB` | **Uso de Memoria de Video (VRAM).** Está usando solo **2 MiB** de los **16311 MiB** (aproximadamente 16 GB) disponibles. Esto indica que la tarjeta está prácticamente inactiva. |
| **`GPU-Util`** | `0%` | **Utilización de la GPU.** El porcentaje de tiempo que el núcleo del procesador gráfico está activamente realizando tareas. **`0%`** indica que no está ejecutando ninguna carga de trabajo (cálculo o renderizado). |
| **`Compute M.`** | `Default` | **Modo de Cálculo.** Indica si la GPU está configurada para cargas de trabajo de cálculo intensivo (normalmente `Default` en sistemas de escritorio). |
| **`MIG M.`** | `N/A` | **Modo de Instancia de GPU Múltiple.** `N/A` indica que no se está utilizando la tecnología MIG, que permite dividir físicamente una sola GPU en varias instancias para tareas específicas (principalmente en GPU de centro de datos). |

<br/>

### 3. Procesos en Ejecución

Esta sección es crucial para saber **qué programas** están utilizando la memoria de tu GPU.

| Columna | Significado |
| :--- | :--- |
| **`Processes`** | El título de la sección que lista todos los procesos activos en la GPU. |
| **`GPU ID`** | El índice de la tarjeta gráfica que está usando el proceso. |
| **`PID`** | El **ID de Proceso** del programa que se está ejecutando (útil para terminar el proceso con el comando `kill <PID>`). |
| **`Type`** | El tipo de carga de trabajo (`G` para gráfico, `C` para cómputo/cálculo). |
| **`Process name`** | El **nombre del ejecutable** del programa. |
| **`GPU Memory Usage`** | La **cantidad de VRAM** que está consumiendo ese proceso específico. |
| **`No running processes found`** | En este caso, **no hay ninguna aplicación** (como un juego, un software de modelado 3D o un script de Machine Learning) que esté utilizando activamente la GPU en este momento. |

En resumen, tu tarjeta **NVIDIA GeForce RTX 5060 Ti** está instalada, tiene los controladores actualizados (versión **580.65.06**), tiene **16 GB de VRAM**, y actualmente está **inactiva** (`0%` de uso, `29C` de temperatura).
