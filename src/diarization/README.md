# Speaker diarization

## [pyannote speaker diarization toolkit](https://github.com/pyannote/pyannote-audio?tab=readme-ov-file)

`pyannote.audio` is an open-source toolkit written in Python for speaker diarization. Based on PyTorch machine learning framework, it comes with state-of-the-art pretrained models and pipelines, that can be further finetuned to your own data for even better performance.

## Implementación de Diarización con Pyannote + Asterisk

Este documento describe el proceso completo para instalar Python, configurar un entorno virtual para Pyannote, preparar el sistema para ejecutar diarización de voz con GPU y utilizar el script `diariza.py` como AGI dentro de Asterisk.


### Verificar versión de Python y pip

```coffeescript
python3 --version
python3 -m pip --version
pip --version
```

> [!NOTE]
> Si `pip` no está instalado, instalarlo:
> 
> ```coffeescript
> sudo apt install python3-pip -y
> ```


### Verificar módulo `venv`

```coffeescript
python3 -m venv -h
python3 -m venv --version
```

> [!NOTE]
> Si no está instalado:
> 
> ```coffeescript
> sudo apt install python3.12-venv
> ```


### Instalar FFmpeg (requerido para Pyannote)

```coffeescript
sudo apt install -y ffmpeg
```


### Crear directorio para diarización (usuario asterisk)

```coffeescript
sudo -u asterisk mkdir -p "/var/lib/asterisk/diarization"
```


### Crear entorno virtual para Pyannote (como usuario asterisk)

```coffeescript
sudo -u asterisk python3 -m venv "/var/lib/asterisk/diarization"
```

Actualizar `pip`:

```coffeescript
sudo -u asterisk bash -c "source /var/lib/asterisk/diarization/bin/activate && pip install --upgrade pip"
```

Instalar Pyannote:

```coffeescript
sudo -u asterisk bash -c "source /var/lib/asterisk/diarization/bin/activate && pip install pyannote.audio"
```


### Probar que CUDA está disponible

Activar entorno:

```coffeescript
source "/var/lib/asterisk/diarization/bin/activate"
```

Ejecutar:

```coffeescript
python3 -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

Salida esperada:

```
True
NVIDIA GeForce RTX 5060 Ti
```

Salir del entorno virtaul

```coffeescript
deactivate
```


### Copiar o crear el script AGI `diariza.py`

```coffeescript
sudo -u asterisk vim "/var/lib/asterisk/agi-bin/diariza.py"
```

> [!NOTE]
> Dentro de tu script Python (por ejemplo `diariza.py`), debes usar el **shebang apuntando al Python del venv**, así:
> 
> ```
> #!/opt/diarizacion/env/bin/python
> ```
> 
> Ese *python* es el que ya tiene instalados:
> 
> * pyannote
> * pytorch
> * torchaudio
> * dependencias varias


Dar permisos de ejecución:

```coffeescript
sudo chmod +x "/var/lib/asterisk/agi-bin/diariza.py"
```


### Uso desde la consola de Asterisk

Puedes probar un originate:

```coffeescript
channel originate Local/test@diarization extension test@diarization
```

---

### Resultado generado

Tras la ejecución, se deben generar archivos junto al WAV:

* `archivo.rttm`
* `archivo.json`
* `archivo_diarize.log`

---

> [!IMPORTANT]
> 1. Make sure [`ffmpeg`](https://ffmpeg.org/) is installed on your machine (needed by [`torchcodec`](https://docs.pytorch.org/torchcodec/) audio decoding library)
> 2. Install with [`uv`](https://docs.astral.sh/uv/)`add pyannote.audio` (recommended) or `pip install pyannote.audio`
> 3. Accept [`pyannote/speaker-diarization-community-1`](https://hf.co/pyannote/speaker-diarization-community-1) user conditions
> 4. Create Huggingface access token at [`hf.co/settings/tokens`](https://hf.co/settings/tokens)
