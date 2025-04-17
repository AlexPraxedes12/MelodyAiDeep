import librosa
import crepe
import numpy as np
from pydub import AudioSegment

# Escalas musicales predefinidas
MUSICAL_SCALES = {
    "C_major": ["C", "D", "E", "F", "G", "A", "B"],
    "A_minor": ["A", "B", "C", "D", "E", "F", "G"],
}

def correct_pitch(
    input_path: str,
    intensity: str,
    scale: str,
    keep_vibrato: bool
) -> str:
    # Cargar audio
    y, sr = librosa.load(input_path, sr=16000)
    
    # Detectar pitch con CREPE
    time, frequency, confidence, _ = crepe.predict(y, sr, viterbi=True)
    
    # Ajustar pitch según escala e intensidad
    target_notes = MUSICAL_SCALES[scale]
    y_corrected = apply_scale_correction(y, sr, frequency, target_notes, intensity)
    
    # Mantener vibrato si está activado
    if keep_vibrato:
        y_corrected = apply_vibrato(y, y_corrected)
    
    # Guardar resultado
    output_path = "temp_audio/corrected.wav"
    librosa.output.write_wav(output_path, y_corrected, sr)
    return output_path