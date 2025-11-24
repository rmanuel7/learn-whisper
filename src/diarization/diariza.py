#!/var/lib/asterisk/diarization/bin/python
# -*- coding: utf-8 -*-

from pyannote.audio import Pipeline
import os
import sys
import logging
import traceback
import torch # ¡NUEVA IMPORTACIÓN!

# --- CONFIGURACIÓN ---
# Por favor, reemplaza "TU_TOKEN_AQUI" con tu token real de Hugging Face
HF_TOKEN = "TU_TOKEN_AQUI" 

# === CONFIGURACIÓN DE LOGGING ===
def setup_logging(audio_path):
    """Configura el sistema de logging para escribir en un archivo .log adyacente."""
    base_name = os.path.splitext(audio_path)[0]
    log_file = base_name + "_diarize.log"
    logger = logging.getLogger('pyannote_diarize')
    logger.setLevel(logging.DEBUG)

    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"--- Log de Pyannote iniciado. Archivo: {log_file} ---")
    except Exception as e:
        sys.stderr.write(f"FATAL AGI ERROR: No se pudo crear el archivo de log. Error: {e}\n")
        logger = None
    return logger

# === LÓGICA PRINCIPAL ===
if __name__ == "__main__":
    
    # 1. Chequeo de argumentos y logging
    if len(sys.argv) < 2:
        sys.stderr.write("FATAL AGI ERROR: Uso: diariza.py <archivo.wav>\n")
        sys.exit(1)

    audio = sys.argv[1].strip()
    rttm = audio.replace(".wav", ".rttm")
    logger = setup_logging(audio)
    
    # 2. **SOLUCIÓN CRUCIAL 1:** Cambiar el Directorio de Trabajo (CWD)
    try:
        safe_cwd = "/var/lib/asterisk"
        logger.info(f"CWD actual: {os.getcwd()}")
        os.chdir(safe_cwd)
        logger.info(f"CWD cambiado exitosamente a: {os.getcwd()}")
    except Exception as e:
        logger.critical(f"ERROR: No se pudo cambiar el CWD a {safe_cwd}. Error: {e}")
        sys.stderr.write("AGI ERROR: Fallo al cambiar CWD. Consulte el log.\n")
        sys.exit(1)

    # 3. Verificar CUDA
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Dispositivo detectado para la ejecución: {DEVICE}")
    if DEVICE.type == 'cpu':
        logger.warning("CUDA no disponible. Ejecutando en CPU (puede causar falta de memoria).")
    
    # 4. Cargar el pipeline (usando 'token' y 'device')
    pipeline = None
    try:
        logger.info(f"Cargando pipeline en {DEVICE}...")
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=HF_TOKEN
        )

        # send pipeline to GPU (when available)
        pipeline.to(torch.device("cuda"))

        logger.info(f"Pipeline cargado exitosamente en: {pipeline.device}")
    except Exception as e:
        logger.critical(f"ERROR CRÍTICO AL CARGAR EL PIPELINE: {e}")
        logger.critical(traceback.format_exc())
        sys.stderr.write(f"AGI ERROR: No se pudo cargar el modelo. Consulte el log para más detalles.\n")
        sys.exit(1)
        
    # 5. Ejecutar la diarización
    try:
        logger.info(f"Ejecutando la diarización en {audio}...")
        diar = pipeline(audio)
        logger.info("Diarización completada.")
    except Exception as e:
        logger.error(f"ERROR durante la ejecución de la diarización: {e}")
        logger.error(traceback.format_exc())
        
        # Guardar el error en el archivo de salida
        with open(rttm, "w") as f:
            f.write("ERROR durante la diarización:\n")
            f.write(str(e) + "\n")
            f.write(traceback.format_exc())
        
        sys.stderr.write("AGI ERROR: Fallo de ejecución de Pyannote. Consulte el log.\n")
        sys.exit(1)

    # 6. Guardar resultado RTTM y comunicar éxito
    try:
        with open(rttm, "w") as f:
            diar.speaker_diarization.write_rttm(f)
        logger.info(f"Resultado RTTM guardado exitosamente en: {rttm}")
        
        # Comunicar éxito a Asterisk
        print("SET VARIABLE DIARIZATION_STATUS \"SUCCESS\"")

        for segment, _, speaker in diar.itertracks(yield_label=True):
            print(f"SET VARIABLE {speaker}_SEGMENT_{segment.start:.2f} {segment.end:.2f}")

    except Exception as e:
        logger.error(f"ERROR al guardar el archivo RTTM o al comunicarse con Asterisk: {e}")
        sys.stderr.write(f"AGI ERROR: Fallo en el post-procesamiento. Consulte el log.\n")
        sys.exit(1)

    logger.info("--- Fin de Ejecución Exitosa ---")
    sys.exit(0)
