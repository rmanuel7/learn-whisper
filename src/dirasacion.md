# Speaker diarization

## [pyannote speaker diarization toolkit](https://github.com/pyannote/pyannote-audio?tab=readme-ov-file)

`pyannote.audio` is an open-source toolkit written in Python for speaker diarization. Based on PyTorch machine learning framework, it comes with state-of-the-art pretrained models and pipelines, that can be further finetuned to your own data for even better performance.

# ✅ **1. Para usar Pyannote de forma segura, limpia y estable:**

Debes:

### **A. Crear un entorno virtual (venv)**

Ejemplo:

```bash
mkdir /opt/diarizacion
cd /opt/diarizacion
python3 -m venv env
```

### **B. Activar e instalar pyannote.audio dentro del venv**

```bash
source env/bin/activate
pip install pyannote.audio
```

Ahora Pyannote está completamente aislado dentro de:

```
/opt/diarizacion/env/
```

Nada del sistema se toca.

---

# ✅ **2. Para ejecutar tu script usando ese venv**

Dentro de tu script Python (por ejemplo `diariza.py`), debes usar el **shebang apuntando al Python del venv**, así:

```
#!/opt/diarizacion/env/bin/python
```

Ese *python* es el que ya tiene instalados:

* pyannote
* pytorch
* torchaudio
* dependencias varias

---

# 🧠 ¿Qué implica esto?

* ✔ Tu script siempre usará el Python correcto
* ✔ Funciona incluso sin activar el venv
* ✔ Evitas conflictos con el Python del sistema
* ✔ Garantizas que pyannote.audio está disponible
* ✔ Puedes ejecutar el script con:

```
./diariza.py audio.wav
```

o

```
python diariza.py audio.wav
```

---

# 🧩 Ejemplo completo

Supongamos que tu proyecto está aquí:

```
/opt/diarizador/
```

Estructura:

```
/opt/diarizador/env        <-- entorno virtual
/opt/diarizador/diariza.py <-- script
```

Tu script deberia iniciar así:

```python
#!/opt/diarizador/env/bin/python

from pyannote.audio import Pipeline
import os

HF_TOKEN = os.getenv("HF_TOKEN")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)

# apply the pipeline to an audio file
diarization = pipeline("audio.wav")

# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

```

Luego marcas el script como ejecutable:

```bash
chmod +x diariza.py
```

Y lo ejecutas:

```bash
./diariza.py mi_audio.wav
```

---

> [!IMPORTANT]
> 1. Make sure [`ffmpeg`](https://ffmpeg.org/) is installed on your machine (needed by [`torchcodec`](https://docs.pytorch.org/torchcodec/) audio decoding library)
> 2. Install with [`uv`](https://docs.astral.sh/uv/)`add pyannote.audio` (recommended) or `pip install pyannote.audio`
> 3. Accept [`pyannote/speaker-diarization-community-1`](https://hf.co/pyannote/speaker-diarization-community-1) user conditions
> 4. Create Huggingface access token at [`hf.co/settings/tokens`](https://hf.co/settings/tokens)
